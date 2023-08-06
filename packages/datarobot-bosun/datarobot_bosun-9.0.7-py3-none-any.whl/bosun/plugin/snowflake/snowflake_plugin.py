#  ---------------------------------------------------------------------------------
#  Copyright (c) 2022 DataRobot, Inc. and its affiliates. All rights reserved.
#  Last updated 2023.
#
#  DataRobot, Inc. Confidential.
#  This is proprietary source code of DataRobot, Inc. and its affiliates.
#
#  This file and its contents are subject to DataRobot Tool and Utility Agreement.
#  For details, see
#  https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.
#  ---------------------------------------------------------------------------------
import os
import textwrap
from typing import Optional
from typing import Union

import snowflake.connector
from bosun.plugin.action_status import ActionStatus
from bosun.plugin.action_status import ActionStatusInfo
from bosun.plugin.bosun_plugin_base import BosunPluginBase
from bosun.plugin.constants import DeploymentState
from bosun.plugin.deployment_info import DeploymentInfo
from bosun.plugin.pe_info import PEInfo
from bosun.plugin.snowflake.snowflake_plugin_config import SnowflakePluginConfig
from snowflake.connector import DatabaseError
from snowflake.connector import ProgrammingError


class SnowflakePlugin(BosunPluginBase):
    EMPTY_MODEL_LOCATION = "<No Location>"

    def __init__(self, plugin_config, private_config_file, pe_info, dry_run):
        super().__init__(plugin_config, private_config_file, pe_info, dry_run)
        self._private_config_file = private_config_file
        self._pe_info = PEInfo(pe_info) if pe_info else None
        self._conn = None

    def get_config(
        self, deployment: Optional[Union[DeploymentInfo, str]] = None
    ) -> SnowflakePluginConfig:
        self._logger.info("Snowflake plugin config file: {}".format(self._private_config_file))
        config = SnowflakePluginConfig.read_config(
            self._pe_info, self._private_config_file, deployment
        )
        config.validate_config()
        return config

    def _snowflake_connect(self):
        if self._conn is None:
            config = self.get_config()

            connection_properties = {
                "account": config.account,
                "warehouse": config.warehouse,
                "database": config.database,
                "schema": config.schema,
            }

            if config.auth_type == "oauth":
                connection_properties["authenticator"] = config.auth_type
                connection_properties["token"] = config.oauth_token
            else:
                # user credentials auth is for testing purposes only
                connection_properties["user"] = config.user
                connection_properties["password"] = config.password

            self._conn = snowflake.connector.connect(**connection_properties)

    def _execute_query(self, query, fetch_all=True):
        self._snowflake_connect()
        cur = self._conn.cursor()
        try:
            cur.execute(query)
            result = cur.fetchall() if fetch_all else cur.sfqid
        finally:
            cur.close()

        return result

    def deployment_list(self):
        self._logger.info("Getting the list of running deployments")
        config = self.get_config()

        try:
            get_all_deployed_udfs = (
                "SHOW USER FUNCTIONS LIKE '{udf_function_prefix}_%' IN {db}.{schema}"
            ).format(
                udf_function_prefix=config.udf_function_prefix,
                db=config.database,
                schema=config.schema,
            )

            last_query_id = self._execute_query(get_all_deployed_udfs, fetch_all=False)
            filter_udf_by_prediction_env_id = (
                "SELECT \"name\", \"description\" FROM TABLE(RESULT_SCAN('{last_query_id}')) "
                "WHERE \"description\" = '{prediction_env_id}'".format(
                    prediction_env_id=config.prediction_environment_id, last_query_id=last_query_id
                )
            )

            deployment_udfs = self._execute_query(filter_udf_by_prediction_env_id)
        except (DatabaseError, ProgrammingError) as e:
            self._logger.error(e)
            return ActionStatusInfo(ActionStatus.ERROR, msg=str(e))

        if deployment_udfs is not None and len(deployment_udfs) > 0:
            status_msg = "Number of scoring code UDFs deployed: {}".format(len(deployment_udfs))
        else:
            status_msg = "No scoring code UDFs deployed"

        self._logger.info(status_msg)
        self._logger.info("Deployed Scoring Code UDFs: " + str(deployment_udfs))

        deployments_map = {}
        deployment_ready = ActionStatusInfo(ActionStatus.OK, state=DeploymentState.READY).__dict__

        for udf_name, _ in deployment_udfs:
            # UDF name structure: <udf_name_prefix>_<deployment_id>
            deployment_id = udf_name.split("_")[-1].lower()
            # A UDF in Snowflake either exists or doesn't, so if it's there, then it is ready
            deployments_map[deployment_id] = deployment_ready

        self._logger.info("Deployments: " + str(deployments_map))
        return ActionStatusInfo(ActionStatus.OK, msg=status_msg, data=deployments_map)

    def deployment_start(self, deployment: dict):
        di = DeploymentInfo(deployment)
        config = self.get_config(di)

        if di.model_artifact == self.EMPTY_MODEL_LOCATION:
            return ActionStatusInfo(
                ActionStatus.ERROR,
                "Model must be pulled from DataRobot deployment, before pushing it to Snowflake.",
            )

        self._logger.info("Starting deployment {}".format(di.id))
        udf_scoring_jar = os.path.basename(di.model_artifact)

        try:
            self._logger.info(
                "Uploading model artifact: %s, size: %s",
                udf_scoring_jar,
                os.path.getsize(di.model_artifact),
            )
            upload_jar_query = "PUT 'file://{jar_file}' '@~/jars/' AUTO_COMPRESS=FALSE".format(
                jar_file=di.model_artifact
            )
            self._execute_query(upload_jar_query)
            self._logger.info("Scoring Code JAR uploaded")

            self._logger.info("Creating an Scoring Code function %s", config.udf_function_name)

            if di.is_prediction_explanations_supported:
                self._logger.info(
                    "Prediction Explanations enabled for %s", config.udf_function_name
                )

            create_udf_query = textwrap.dedent(
                """
             CREATE OR REPLACE FUNCTION {udf_function_name}({udf_params})
                RETURNS {udf_return_type}
                LANGUAGE JAVA
                IMPORTS=('@~/jars/{udf_scoring_jar}')
                HANDLER='{udf_scoring_handler}'
                COMMENT='{prediction_env_id}'"""
            ).format(
                udf_function_name=config.udf_function_name,
                udf_params=config.udf_scoring_method_params,
                udf_return_type=config.udf_return_type,
                udf_scoring_jar=udf_scoring_jar,
                udf_scoring_handler=config.udf_scoring_handler,
                prediction_env_id=config.prediction_environment_id,
            )
            self._execute_query(create_udf_query)
            self._logger.info("Scoring Code function is created.")

        except (DatabaseError, ProgrammingError) as e:
            self._logger.error(e)
            return ActionStatusInfo(ActionStatus.ERROR, msg=str(e))

        self._logger.info("Scoring Code UDF deployed successfully.")
        return ActionStatusInfo(ActionStatus.OK, state=DeploymentState.READY)

    def deployment_stop(self, deployment: dict):
        deployment_id = deployment["id"]
        config = self.get_config(deployment_id)
        self._logger.info("Stopping deployment %s", deployment_id)
        self._logger.info("Deleting Scoring Code UDF: %s", config.udf_function_name)
        query = "DROP FUNCTION IF EXISTS {udf_name} (OBJECT)".format(
            udf_name=config.udf_function_name
        )
        try:
            self._execute_query(query, fetch_all=False)
        except (DatabaseError, ProgrammingError) as e:
            self._logger.error(e)
            return ActionStatusInfo(ActionStatus.ERROR, msg=str(e))

        self._logger.info("Scoring Code UDF removed")
        return ActionStatusInfo(ActionStatus.OK, state=DeploymentState.STOPPED)

    def deployment_replace_model(self, deployment: dict):
        di = DeploymentInfo(deployment)
        self._logger.info("Replacing model for deployment: {}".format(di.id))
        return self.deployment_start(deployment)

    def pe_status(self):
        try:
            self._execute_query("SELECT 1")
            status = ActionStatus.OK
            status_msg = "Snowflake connection successful"
        except (DatabaseError, ProgrammingError):
            status = ActionStatus.ERROR
            status_msg = "Failed to connect to Snowflake"
            self._logger.error(status_msg, exc_info=True)

        self._logger.info(status_msg)
        return ActionStatusInfo(status=status, msg=status_msg)

    def deployment_status(self, deployment: dict):
        di = DeploymentInfo(deployment)
        config = self.get_config(di)
        self._logger.info("Getting status for deployment: {}".format(di.id))
        check_udf_function_deployed = "SHOW USER FUNCTIONS LIKE '{udf_name}'".format(
            udf_name=config.udf_function_name
        )

        try:
            udf_functions_deployed = self._execute_query(check_udf_function_deployed)
        except (DatabaseError, ProgrammingError) as e:
            self._logger.error(e)
            return ActionStatusInfo(ActionStatus.ERROR, msg=str(e))

        if udf_functions_deployed is not None and len(udf_functions_deployed) >= 1:
            return ActionStatusInfo(ActionStatus.OK, state=DeploymentState.READY)
        else:
            return ActionStatusInfo(ActionStatus.UNKNOWN, state=DeploymentState.STOPPED)

    def plugin_start(self):
        self._logger.info("Snowflake plugin_start called")
        self._snowflake_connect()
        return ActionStatusInfo(ActionStatus.OK)

    def plugin_stop(self):
        self._logger.info("Snowflake plugin_stop called")
        if self._conn is not None:
            self._conn.close()
        return ActionStatusInfo(ActionStatus.OK)
