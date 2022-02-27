import logging.handlers
import os
from logging import LogRecord


_LOGLEVEL_MAPPING = {
    'CRITICAL': 50,
    'ERROR': 40,
    'WARNING': 30,
    'INFO': 20,
    'DEBUG': 10,
    'NOTSET': 0
}


class FilterOnlyInfo(logging.Filter):
    def filter(self, record: LogRecord) -> bool:
        return record.levelname == 'INFO'


class FilterLessThanError(logging.Filter):
    def filter(self, record: LogRecord) -> bool:
        return record.levelno < _LOGLEVEL_MAPPING['ERROR']


def initialize_logs():
    curr_dir = os.path.join(os.getcwd(), 'logs')
    logging_config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'simple_fmt': {
                'format': '%(asctime)s - [%(levelname)s]: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
                # 'use_colors': True
            },
            'error_fmt': {
                'format': "%(asctime)s - [%(levelname)s] %(funcName)s() L%(lineno)-4d : %(message)s "
                          "| call_trace=%(pathname)s",
                'datefmt': '%Y-%m-%d %H:%M:%S',
                # 'use_colors': True
            },
            'access_fmt': {
                '()': 'uvicorn.logging.AccessFormatter',
                'format': '%(asctime)s [%(levelname)s]: %(client_addr)s - "%(request_line)s" %(status_code)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
                # 'use_colors': True
            },
            "default_uvicorn": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
                "use_colors": None,
            },
        },
        'handlers': {
            'internalFile': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'simple_fmt',
                'filename': os.path.join(curr_dir, "internal.log"),
                'level': 'INFO',
                'maxBytes': 10485760,
                'backupCount': 2,
                'filters': ['less_than_error']
            },
            'accessFile': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': "INFO",
                'formatter': 'access_fmt',
                'filename': os.path.join(curr_dir, "access.log"),
                'maxBytes': 10485760,
                'backupCount': 3,
                'filters': ['only_info']
            },
            'std_console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default_uvicorn',
                'stream': "ext://sys.stdout",
            },

            'errorFile': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'error_fmt',
                'filename': os.path.join(curr_dir, "errors.log"),
                'maxBytes': 10485760,
                'backupCount': 10,
                'level': 'WARNING'
            },
            "error_console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
                'formatter': 'error_fmt',
                'level': 'INFO'
            }
        },
        'loggers': {
            'uvicorn': {
                'level': 'INFO',
                'handlers': ['std_console', 'internalFile'],
            },
            'uvicorn.error': {
                'level': 'INFO',
                'handlers': ['errorFile', "error_console"],
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["accessFile"],
                'propagate': False
            },
        },

        'filters': {
            'only_info': {
                '()': FilterOnlyInfo
            },
            'less_than_error': {
                '()': FilterLessThanError
            }
        }
    }
    return logging_config
