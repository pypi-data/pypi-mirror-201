from matter_observability.config import Config

LOGGING_CONFIG = {
    "version": 1,
    "filters": {"request_id": {"()": "matter_observability.fastapi.request_id.RequestIdLogFilter"}},
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s] [%(request_id)s] [%(filename)s:%(funcName)s:%(lineno)s] - %(message)s"
        },
        "no_request_id": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s] [%(filename)s:%(funcName)s:%(lineno)s] - %(message)s"
        },
    },
    "handlers": {
        "default": {
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr,
            "filters": ["request_id"],
        },
        "no_request_id": {
            "formatter": "no_request_id",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {
        "root": {
            "handlers": ["default"],
            "level": Config.SERVER_LOG_LEVEL.upper(),
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["no_request_id"],
            "level": Config.SERVER_LOG_LEVEL.upper(),
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": Config.SERVER_LOG_LEVEL.upper(),
            "propagate": False,
        },
        "sqs-consumer": {
            "handlers": ["default"],
            "level": Config.SERVER_LOG_LEVEL.upper(),
            "propagate": False,
        },
    },
}
