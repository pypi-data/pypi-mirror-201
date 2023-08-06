# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rlogging',
 'rlogging.integration',
 'rlogging.integration.aiogram',
 'rlogging.integration.django',
 'rlogging.integration.fastapi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rlogging',
    'version': '1.0.7',
    'description': '',
    'long_description': "# rlogging\n\nSpecific logging settings for a python application\n\n## Usage\n\n```\npip install rlogging\n```\n\n### Python\n\n```bash\n\n```\n\n### Django\n\n```bash\n# settings.py\n\nINSTALLED_APPS = [\n    ...\n    'rlogging.integration.django',\n    ...\n]\n\nMIDDLEWARE = [\n    ...\n    'rlogging.integration.django.middleware.LoggingMiddleware',\n    ...\n]\n\nLOGGING = generate_logging_dict(LOGS_DIR, MIN_LOGGING_LEVEL)\n```\n\n### FastAPI\n\n```bash\n\n```\n\n### aiogram\n\n```bash\n\n```\n\n",
    'author': 'irocshers',
    'author_email': 'develop.iam@rocshers.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
