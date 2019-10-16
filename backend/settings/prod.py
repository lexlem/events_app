""" Production Settings """

import os
import dj_database_url
from .dev import *

DEBUG = False
ALLOWED_HOSTS = ["*"]
BACKEND_SCHEME = "https"
BACKEND_DOMAIN = "example.com"
BACKEND_URL = "%s://%s" % (BACKEND_SCHEME, BACKEND_DOMAIN)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "gunicorn": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": "/home/example_user/example/debug.log",
            "maxBytes": 1024 * 1024 * 100,
        }
    },
    "loggers": {
        "gunicorn.errors": {
            "level": "DEBUG",
            "handlers": ["gunicorn"],
            "propagate": True,
        },
        "django": {
            "handlers": ["gunicorn"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        },
    },
}
