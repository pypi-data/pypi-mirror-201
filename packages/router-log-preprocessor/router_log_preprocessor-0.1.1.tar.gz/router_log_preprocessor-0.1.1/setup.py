# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['router_log_preprocessor',
 'router_log_preprocessor.domain',
 'router_log_preprocessor.hooks',
 'router_log_preprocessor.hooks.zabbix',
 'router_log_preprocessor.log_server',
 'router_log_preprocessor.preprocessors',
 'router_log_preprocessor.util']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.6.2,<4.0.0',
 'asyncio-zabbix-sender>=0.1.1,<0.2.0',
 'macaddress>=2.0.2,<3.0.0',
 'pydantic[dotenv]>=1.10.4,<2.0.0']

entry_points = \
{'console_scripts': ['router-log-preprocessor = '
                     'router_log_preprocessor.__main__:main']}

setup_kwargs = {
    'name': 'router-log-preprocessor',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Router Log Preprocessor\n![router-log-preprocessor](https://user-images.githubusercontent.com/105678820/228938795-66dbd955-813b-4fb3-a559-4f3a41f55bb9.png)\n\n> Garbage in, garbage out\n>\n> &mdash; <cite>George Fuechsel</cite>\n\nPreprocessors upcycle garbage input data into well-structured data to ensure reliable and accurate event handling in third-party systems such as Zabbix.\nBy parsing and filtering the input log data, the preprocessor helps to ensure that only high-quality data are sent for further analysis and alerting.\nThis helps to minimize false positives and ensure that network administrators receive reliable and actionable alerts about potential security threats or other issues.\n\n\nKey features:\n- **Wireless LAN Controller event** log entries are parsed to tangible enumerations\n- **DNSMASQ DHCP** log entries are parsed to catch which IP a given client is assigned to\n- **Zabbix** templates are included to ensure that the logs are can lead to actionable alerts\n- **Extendable** preprocessors and hooks to ensure future reliable information to network administrators\n\n## Installation\n```console\n$ pip install router-log-preprocessor\n```\n\nIf needed it can also be installed from sources.\nRequires [Poetry 1.3.2](https://python-poetry.org/).\n```console\n$ git pull https://github.com/mastdi/router-log-preprocessor.git\n$ cd router-log-preprocessor\n$ poetry install\n```\n',
    'author': 'Martin Storgaard Dieu',
    'author_email': 'martin@storgaarddieu.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mastdi/router-log-preprocessor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
