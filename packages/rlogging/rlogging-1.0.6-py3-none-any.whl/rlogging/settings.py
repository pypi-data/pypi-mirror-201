from pathlib import Path


def generate_logging_dict(logs_dir: Path | str, min_log_level: str) -> dict:
    """Генерация конфигурации логирования

    Args:
        logs_dir (Path | str): Корневая папка для логов
        min_log_level (str): Минимальный уровень логирования

    Returns:
        dict: Конфигурация логирования

    """

    logs_dir = Path(logs_dir)
    logs_dir.parent.mkdir(parents=True, exist_ok=True)

    return {
        'version': 1,
        'filters': {'warning': {'()': 'rlogging.filters.WarningFilter'}},
        'formatters': {
            'text': {'()': 'rlogging.formatters.RsFormatter'},
            'elk': {'()': 'rlogging.formatters.ElkFormatter'},
        },
        'handlers': {
            'django_file': {
                'class': 'rlogging.handlers.DailyFileHandler',
                'filename': logs_dir / 'django.log',
                'formatter': 'elk',
            },
            'app_file': {
                'class': 'rlogging.handlers.DailyFileHandler',
                'filename': logs_dir / 'app.log',
                'formatter': 'elk',
            },
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'text',
            },
            'error': {
                'class': 'logging.StreamHandler',
                'formatter': 'text',
                'level': 'WARNING',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['django_file', 'error'],
                'level': min_log_level,
                'propagate': False,
            },
        },
        'root': {
            'handlers': ['app_file', 'console'],
            'level': min_log_level,
            'propagate': False,
        },
    }
