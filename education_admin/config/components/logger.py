
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
      'simple': {
          'format': '{levelname} | {asctime} | {message}',
          'style': '{',
      }
    },
    'handlers': {
        'info_handler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'log/info.log',
            'formatter': 'simple'
        },
        'error_handler': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'log/errors.log',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'root': {
            'handlers': ['info_handler', 'error_handler'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

