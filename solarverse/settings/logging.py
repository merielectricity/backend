<<<<<<< HEAD
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
=======
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
>>>>>>> 12942d85125a16abc021dbab49c0f43f3200a538
}