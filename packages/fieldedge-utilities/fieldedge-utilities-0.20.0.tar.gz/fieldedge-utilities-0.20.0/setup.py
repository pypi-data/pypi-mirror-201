# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fieldedge_utilities', 'fieldedge_utilities.microservice']

package_data = \
{'': ['*']}

install_requires = \
['ifaddr>=0.1.7,<0.2.0',
 'paho-mqtt>=1.6.1,<2.0.0',
 'pyserial>=3.5,<4.0',
 'python-dotenv>=0.19.1,<0.20.0']

setup_kwargs = {
    'name': 'fieldedge-utilities',
    'version': '0.20.0',
    'description': 'Utilities package for the FieldEdge project.',
    'long_description': '# Inmarsat FieldEdge Utilities\n\nInmarsat FieldEdge project supports *Internet of Things* (**IoT**) using\nsatellite communications technology.\n\nThis library available on **PyPI** provides:\n\n* A common **`logger`** format and wrapping file facility.\n* A repeating **`timer`** utility (thread) that can be started, stopped,\nrestarted, and interval changed.\n* A simplified **`mqtt`** client that automatically (re)onnects\n(by default to a local `fieldedge-broker`).\n* Helper functions for managing files and **`path`** on different OS.\n* An interface for the FieldEdge **`hostpipe`** service for sending host\ncommands from a Docker container, with request/result captured in a logfile.\n* Helper functions **`ip_interfaces`** for finding and validating IP interfaces\nand addresses/subnets.\n* A defined set of common **`ip_protocols`** used for packet analysis and\nsatellite data traffic optimisation.\n* Helpers for **`class_properties`** to expose public properties of classes\nfor MQTT transport between microservices, converting between PEP and JSON style.\n(replaced by `microservice.properties`)\n* Helpers for managing **`serial`** ports on a host system.\n* Utilities for converting **`timestamp`**s between unix and ISO 8601\n* Classes useful for implementing **`microservice`**s based on MQTT\ninter-service communications and task workflows:\n    * **`properties`** manipulation and conversion between JSON and PEP style,\n    and derived from classes or instances.\n    * **`interservice`** communications tasks and searchable queue.\n    * **`propertycache`** concept for caching frequently referenced object\n    properties where the query may take time.\n    * **`microservice`** classes for abstraction and proxy operations\n\n[Docmentation](https://inmarsat-enterprise.github.io/fieldedge-utilities/)\n',
    'author': 'geoffbrucepayne',
    'author_email': 'geoff.bruce-payne@inmarsat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/inmarsat-enterprise/fieldedge-utilities',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
