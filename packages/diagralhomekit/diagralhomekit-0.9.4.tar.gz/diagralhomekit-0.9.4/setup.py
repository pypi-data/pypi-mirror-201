# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diagralhomekit']

package_data = \
{'': ['*']}

install_requires = \
['HAP-python>=4.6.0,<5.0.0',
 'base36>=0.1.1,<0.2.0',
 'meteofrance-api>=1.2.0,<2.0.0',
 'nut2>=2.1.1,<3.0.0',
 'pyqrcode>=1.2.1,<2.0.0',
 'python-logging-loki>=0.3.1,<0.4.0',
 'requests>=2.28.2,<3.0.0',
 'sentry-sdk>=1.18.0,<2.0.0']

entry_points = \
{'console_scripts': ['diagral-homekit = diagralhomekit.main:main']}

setup_kwargs = {
    'name': 'diagralhomekit',
    'version': '0.9.4',
    'description': 'Apple HomeKit integration for Diagral alarm systems',
    'long_description': "DiagralHomekit\n==============\n\n[![PyPI version](https://badge.fury.io/py/diagralhomekit.svg)](https://badge.fury.io/py/diagralhomekit)\n\nAllow to control your Diagral alarm systems through Apple Homekit.\n\n\nFirst, you need to create a configuration file `~/.diagralhomekit/config.ini` with connection details for all Diagral systems.\n\n```ini\n[diagral:Home]\nname=[an explicit name for this system]\nlogin=[email address of the Diagral account]\npassword=[password for the Diagral account]\nimap_login=[IMAP login for the email address receiving alarm alerts]\nimap_password=[IMAP password]\nimap_hostname=[IMAP server]\nimap_port=[IMAP port]\nimap_use_tls=[true/1/on if you use SSL for the IMAP connection]\nmaster_code=[a Diagral master code, able to arm or disarm the alarm]\nsystem_id=[system id — see below]\ntransmitter_id=[transmitter id — see below]\ncentral_id=[central id — see below]\n\n```\n`system_id`, `transmitter_id` and `central_id` can be retrieved with the following command, that prepares a configuration file:\n\n```bash\npython3 -m diagralhomekit --config-dir ~/.diagralhomekit --create-config 'diagral@account.com:password'\n```\n\nThen you can run the script:\n\n```bash\npython3 -m diagralhomekit --port 6666 --config-dir ~/.diagralhomekit -v 2\n```\nOn the first launch, a QR code is displayed and can be scanned in Homekit, like any Homekit-compatible device.\n\n\nYou can send logs to [Loki](https://grafana.com/oss/loki/) with `--loki-url=https://username:password@my.loki.server/loki/api/v1/push`.\nYou can also send alerts to [Sentry](https://sentry.io/) with `--sentry-dsn=my_sentry_dsn`.\n\nEverything can be configured by environment variables instead of arguments:\n\n```bash\nDIAGRAL_PORT=6666\nDIAGRAL_CONFIG=/etc/diagralhomekit\nDIAGRAL_SENTRY_DSN=https://sentry_dsn@sentry.io/42\nDIAGRAL_LOKI_URL=https://username:password@my.loki.server/loki/api/v1/push\nDIAGRAL_VERBOSITY=1\n```\n\n\n**As many sensitive data must be stored in this configuration file, so you should create a dedicated email address and Diagral account.**\n\n\nPlex sensor\n-----------\n\nA presence can be detected when a specified Plex player is playing something:\n```ini\n[plex:appletv_web]\nserver_token=[authentication token]\nserver_url=[url of your Plex server]\nplayer_name=[Displayed name for the player]\nplayer_device=None,\nplayer_product=[Product name of the targeted player]\nplayer_title=[Title of the targeted player]\nplayer_address=[IP address of the targeted player]\n```\nOnly one of the last four properties is required to match with the targeted player.\nTo get actual property values, you can use `curl`:\n\n```bash\ncurl -H Accept:application/json -H X-Plex-Token:[authentication token] [url of your Plex server]/status/sessions\n```\n\nHTTP monitoring\n---------------\n\nYou can monitor some websites, as air purifier sensors (no Homekit sensor is available for HTTP monitoring…):\n```ini\n[internet:website]\nurl=[url to check]\nname=[Displayed name]\n```\n\nWeather monitoring\n------------------\n\nYou can monitor weather, and emulate a presence when it will rain in the next 10 minutes:\n\n```ini\n[meteofrance:paris]\nname=Paris\nlatitude=48.866667\nlongitude=2.333333\ncountry=FR\nregion=Île-de-France\n```\n\nUPS monitoring\n--------------\n\nUPS can also be monitoring, as soon as NUT is locally installed (standard UPS monitoring server on Linux.\n```\n[ups:home]\nname=eaton650\n```\n",
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
