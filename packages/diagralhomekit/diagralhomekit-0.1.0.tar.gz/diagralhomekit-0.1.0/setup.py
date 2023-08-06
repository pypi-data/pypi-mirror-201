# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diagralhomekit']

package_data = \
{'': ['*']}

install_requires = \
['HAP-python>=4.6.0,<5.0.0',
 'base36>=0.1.1,<0.2.0',
 'pyqrcode>=1.2.1,<2.0.0',
 'python-logging-loki>=0.3.1,<0.4.0',
 'requests>=2.28.2,<3.0.0',
 'sentry-sdk>=1.18.0,<2.0.0']

entry_points = \
{'console_scripts': ['diagral-homekit = diagralhomekit.main:main']}

setup_kwargs = {
    'name': 'diagralhomekit',
    'version': '0.1.0',
    'description': 'Apple HomeKit integration for Diagral alarm systems',
    'long_description': "DiagralHomekit\n==============\n\nAllow to control your Diagral alarm systems through Homekit.\n\n.. image:: https://pyup.io/repos/github/d9pouces/DiagralHomekit/shield.svg\n     :target: https://pyup.io/repos/github/d9pouces/DiagralHomekit/\n     :alt: Updates\n\n\nFirst, you need to create a configuration file `~/.diagralhomekit/config.ini` with connection details for all Diagral systems.\n\n```ini\n[system:Home]\nname=[an explicit name for this system]\nlogin=[email address of the Diagral account]\npassword=[password for the Diagral account]\nimap_login=[IMAP login for the email address receiving alarm alerts]\nimap_password=[IMAP password]\nimap_hostname=[IMAP server]\nimap_port=[IMAP port]\nimap_use_tls=[true/1/on if you use SSL for the IMAP connection]\nmaster_code=[a Diagral master code, able to arm or disarm the alarm]\nsystem_id=[system id — see below]\ntransmitter_id=[transmitter id — see below]\ncentral_id=[central id — see below]\n\n```\n`system_id`, `transmitter_id` and `central_id` can be retrieved with the following command, that prepares a configuration file:\n\n```bash\npython3 -m diagralhomekit -C ~/.diagralhomekit --create-config 'diagral@account.com:password'\n```\n\nThen you can run the daemon for the first time:\n\n```python3 -m diagralhomekit -p 6666 -C ~/.diagralhomekit -v 2```\n\nYou can send logs to [Loki](https://grafana.com/oss/loki/) with `--loki-url=https://username:password@my.loki.server/loki/api/v1/push`.\nYou can also send alerts to [Sentry](https://sentry.io/) with `--sentry-dsn=my_sentry_dsn`.\n\n**As many sensitive data must be stored in this configuration file, so you should create a dedicated email address and Diagral account.**\n",
    'author': 'd9pouces',
    'author_email': 'github@19pouces.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
