import logging
import logging.config


def setup_logging():
    logging_configuration = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': "[%(asctime)s] [%(levelname)s] %(module)s - %(message)s"
            },
        },
        'handlers': {
            'file_handler': {
                'class': 'logging.FileHandler',
                'filename': 'app.log',
                'level': 'DEBUG',
                'formatter': 'simple',
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['file_handler'],
        },
    }

    logging.config.dictConfig(logging_configuration)
