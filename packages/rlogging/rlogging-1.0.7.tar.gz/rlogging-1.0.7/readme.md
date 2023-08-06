# rlogging

Specific logging settings for a python application

## Usage

```
pip install rlogging
```

### Python

```bash

```

### Django

```bash
# settings.py

INSTALLED_APPS = [
    ...
    'rlogging.integration.django',
    ...
]

MIDDLEWARE = [
    ...
    'rlogging.integration.django.middleware.LoggingMiddleware',
    ...
]

LOGGING = generate_logging_dict(LOGS_DIR, MIN_LOGGING_LEVEL)
```

### FastAPI

```bash

```

### aiogram

```bash

```

