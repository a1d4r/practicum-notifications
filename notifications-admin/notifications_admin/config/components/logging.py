LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
        "request_id": {"()": "request_id.logging.RequestIdFilter"},
    },
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        },
        "json": {
            "format": '{ "time": "%(asctime)s", "level": "%(levelname)s", "request_id": "%(request_id)s", "message": "%(message)s" }',
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "debug-console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "filters": ["require_debug_true", "request_id"],
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "./logs/nginx/json-logs.json",
            "filters": ["request_id"],
            "formatter": "json",
        },
    },
    "loggers": {
        "django.db.backends": {"level": "DEBUG", "handlers": ["debug-console"], "propagate": False},
        "django": {"handlers": ["file"], "level": "DEBUG", "propagate": True},
    },
}
