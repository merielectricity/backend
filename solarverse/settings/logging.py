LOGGING = {
    'version': 1,
    'loggers': {
        'django' : {
            'handlers': ['file'],
            'level': 'DEBUG'
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': './logs/debug.log',
            'formatter': 'simpleRe'
        }
    },
    'formatters': {
        'simpleRe': {
            'format': '{levelname} {message}',
            'style': '{'
        }
    }
}