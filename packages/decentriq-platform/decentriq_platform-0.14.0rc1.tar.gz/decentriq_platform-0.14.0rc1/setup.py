# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decentriq_platform',
 'decentriq_platform.container',
 'decentriq_platform.container.proto',
 'decentriq_platform.proto',
 'decentriq_platform.s3_sink',
 'decentriq_platform.s3_sink.proto',
 'decentriq_platform.sql',
 'decentriq_platform.sql.proto']

package_data = \
{'': ['*']}

install_requires = \
['asn1crypto>=1.5.1,<2.0.0',
 'cbor2>=5.4.6,<6.0.0',
 'certifi>=2022.12.7,<2023.0.0',
 'certvalidator>=0.11.1,<0.12.0',
 'chily>=0.7.0,<0.8.0',
 'cryptography>=39.0.1,<40.0.0',
 'ecdsa>=0.18.0,<0.19.0',
 'oscrypto>=1.3.0,<2.0.0',
 'pem>=21.2.0,<22.0.0',
 'protobuf==4.21.9',
 'requests>=2.28.1,<3.0.0',
 'sgx-ias-structs>=0.1.8,<0.2.0',
 'sqloxide>=0.1.26,<0.2.0',
 'typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'decentriq-platform',
    'version': '0.14.0rc1',
    'description': 'Python client library for the Decentriq platform',
    'long_description': "# Decentriq - Python SDK\n\nThe Decentriq Python SDK exposes the [Decentriq platform](platform.decentriq.com)'s functionality via easy-to-use programming constructs and, as such, allows\nusers to interact with the platform in a programmatic way.\n\nReleases of this library are hosted on [https://pypi.org/project/decentriq-platform/](pypi) and can be installed via the Python package manager `pip`.\n\nPlease refer to the [official documentation](https://docs.decentriq.com/python) for tutorials on how to install and use the\nDecentriq Python SDK, as well as for detailed API documentation.\n",
    'author': 'decentriq',
    'author_email': 'opensource@decentriq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/decentriq/decentriq-platform',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
