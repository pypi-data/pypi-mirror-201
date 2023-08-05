# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncio_zabbix_sender']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asyncio-zabbix-sender',
    'version': '0.1.0',
    'description': 'Asyncio implementation of the Zabbix Sender protocol',
    'long_description': '# Zabbix sender\nDependency free implementation of the Zabbix Sender protocol using asyncio.\n\nKey features:\n- **Full specification** implemented compared to other Zabbix sender implementations\n- **Compression** is enabled as default\n- **Asynchronous** implementation allows the program to continue while waiting for a response from Zabbix\n\n## Installation\nThe package can be found on PyPI and installed using pip:\n```commandline\npip install zabbix-sender-asyncio\n```\n\n## Usage\n\n```python\nimport datetime\nfrom asyncio_zabbix_sender import ZabbixSender, Measurements, Measurement\n\nsender = ZabbixSender("example.com")\n\nmeasurements = Measurements()\nmeasurements.add_measurement(Measurement(\n    "vm-game-server", "cheat[doom]", "idkfa", datetime.datetime.utcnow()\n))\n\nawait sender.send(measurements)\n```\n\n\n## Road map\nThe following improvements are planned (not necessary in order):\n\n- Logging\n- Encryption between the sender and Zabbix\n- More documentation\n',
    'author': 'Martin Storgaard Dieu',
    'author_email': 'martin@storgaarddieu.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mastdi/asyncio-zabbix-sender',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
