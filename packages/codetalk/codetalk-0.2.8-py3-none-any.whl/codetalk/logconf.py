import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/codetalk.log',
            'maxBytes': 10485760,  # 10 MB
            'backupCount': 5,
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
