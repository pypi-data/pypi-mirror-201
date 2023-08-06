from logging import config


class FSLogger:
    log_config = {
        "version": 1,
        "root": {"handlers": ["console"], "level": "INFO"},
        "handlers": {"console": {"formatter": "std_out", "class": "logging.StreamHandler", "level": "INFO"}},
        "formatters": {
            "std_out": {
                "format": "%(asctime)s : %(levelname)s : %(module)s : %(message)s",
                "datefmt": "%d-%m-%Y %I:%M:%S",
            }
        },
    }

    config.dictConfig(log_config)
