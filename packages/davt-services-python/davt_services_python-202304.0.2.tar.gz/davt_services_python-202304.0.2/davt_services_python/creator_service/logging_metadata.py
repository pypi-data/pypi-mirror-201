"""Module to log warning, debug, error and info messages based on project metadata
"""
import sys
import os

import davt_services_python.developer_service.environment_logging as davt_env_log

class LoggingMetaData:
    """
    Class to log warning, debug, error and info messages based on project metadata
    """

    @staticmethod
    def log_debug(config: dict, message):
        """ Log debug message. """
        project_id = config["project_id"]
        environment = config["environment"]
        project_id_env = f"{project_id}_{environment}"
        project_id_env = project_id_env.upper()
        instrumentation_key = config["davt_python_app_insights_key"]
        obj_log_core = davt_env_log.EnvironmentLogging()
        obj_log_core.log_debug(project_id_env, message, instrumentation_key)

    @staticmethod
    def log_warning(config: dict, message):
        """ Log warning message. """
        obj_env_log = davt_env_log.EnvironmentLogging()
        project_id = config["project_id"]
        environment = config["environment"]
        project_id_env = f"{project_id}_{environment}"
        project_id_env = project_id_env.upper()
        instrumentation_key = config["davt_python_app_insights_key"]
        obj_env_log.log_warning(project_id_env, message, instrumentation_key)

    @staticmethod
    def log_info(config, message):
        """ Log info message. """
        obj_env_log = davt_env_log.EnvironmentLogging()
        project_id = config["project_id"]
        environment = config["environment"]
        project_id_env = f"{project_id}_{environment}"
        project_id_env = project_id_env.upper()
        instrumentation_key = config["davt_python_app_insights_key"]
        obj_env_log.log_info(project_id_env, message, instrumentation_key)

    @staticmethod
    def log_error(config, message):
        """ Log debug message. """
        obj_env_log = davt_env_log.EnvironmentLogging()
        project_id = config["project_id"]
        environment = config["environment"]
        project_id_env = f"{project_id}_{environment}"
        project_id_env = project_id_env.upper()
        instrumentation_key = config["davt_python_app_insights_key"]
        obj_env_log.log_error(project_id_env, message, instrumentation_key)
