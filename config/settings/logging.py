"""Settings for logging configuration."""
from config.django.base import BASE_DIR

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "loggers": {
        "django.utils.autoreload": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "ERROR",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "debug.log",
            "formatter": "verbose",
            "level": "INFO",
            "mode": "a",
            "maxBytes": 10485760,  # 10 MB
            "backupCount": 5,  # Keep 5 backup files
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}
