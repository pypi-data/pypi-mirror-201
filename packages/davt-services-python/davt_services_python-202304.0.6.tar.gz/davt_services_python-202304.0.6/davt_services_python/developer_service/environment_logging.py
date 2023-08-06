""" Module for python logging for developer_service with minimal dependencies. """

from opencensus.ext.azure.log_exporter import AzureLogHandler
import sys  # don't remove required for error handling
import os
import logging
import logging.config

# Import from sibling directory ..\developer_service
OS_NAME = os.name

sys.path.append("..")
if OS_NAME.lower() == "nt":
    print("windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..\\..")))
    env_path = os.path.dirname(os.path.abspath(sys.executable + "\\.."))
    env_share_path = env_path + "\\share"
    sys.path.append(os.path.dirname(os.path.abspath(sys.executable + "\\..\\share")))
    ERROR_LOG_FILENAME = env_share_path + "\\.davt_python_services_errors.log"
else:
    print("non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))
    env_path = os.path.dirname(os.path.abspath(sys.executable + "/.."))
    env_share_path = env_path + "/share"
    sys.path.append(os.path.dirname(os.path.abspath(sys.executable + "/../share")))
    ERROR_LOG_FILENAME = env_share_path + "/.davt_python_services_errors.log"

FOLDER_EXISTS = os.path.exists(env_share_path)
if not FOLDER_EXISTS:
    # Create a new directory because it does not exist
    os.makedirs(env_share_path)


print(f"Log files stored at ERROR_LOG_FILENAME:{ERROR_LOG_FILENAME}")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s:%(name)s:%(process)d:%(lineno)d " "%(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "%(message)s",
        },
    },
    "handlers": {
        "logfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "filename": ERROR_LOG_FILENAME,
            "formatter": "default",
            "backupCount": 2,
        },
        "verbose_output": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "tryceratops": {
            "level": "INFO",
            "handlers": [
                "verbose_output",
            ],
        },
    },
    "root": {"level": "DEBUG", "handlers": ["logfile"]},
    "ddt_ops_dev": {"level": "DEBUG", "handlers": ["logfile"]},
    "ndsp_pertussis_dev": {"level": "DEBUG", "handlers": ["logfile"]}
}

class EnvironmentLogging:
    """ EnvironmentLogging class with minimal dependencies for the developer service.
    - This class is used to perform file and directory operations.
    """

    @staticmethod
    def log_debug(project_id_env, message, instrumentation_key) -> str:
        """ Log debug message. """

        logging.config.dictConfig(LOGGING_CONFIG)
        logger = logging.getLogger(project_id_env)
        logger.addHandler(AzureLogHandler(
            connection_string=f'InstrumentationKey={instrumentation_key}')
        )
        logger.debug(message)

        return "Success"

    @staticmethod
    def log_info(project_id_env, message, instrumentation_key) -> str:
        """ Log info message. """

        logging.config.dictConfig(LOGGING_CONFIG)
        logger = logging.getLogger(project_id_env)
        logger.addHandler(AzureLogHandler(
            connection_string=f'InstrumentationKey={instrumentation_key}')
        )

        logger.info(message)

        return "Success"

    @staticmethod
    def log_warning(project_id_env, message, instrumentation_key) -> str:
        """ Log warning message. """

        logging.config.dictConfig(LOGGING_CONFIG)
        logger = logging.getLogger(project_id_env)
        logger.addHandler(AzureLogHandler(
            connection_string=f'InstrumentationKey={instrumentation_key}')
        )
        logger.warning(message)

        return "Success"

    @staticmethod
    def log_error(project_id_env, message, instrumentation_key) -> str:
        """ Log error message. """

        logging.config.dictConfig(LOGGING_CONFIG)
        logger = logging.getLogger(project_id_env)
        logger.addHandler(AzureLogHandler(
            connection_string=f'InstrumentationKey={instrumentation_key}')
        )
        logger.error(message)

        return "Success"
