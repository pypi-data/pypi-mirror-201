# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['seaplane',
 'seaplane.api',
 'seaplane.logging',
 'seaplane.model',
 'seaplane.model.compute',
 'seaplane.model.locks',
 'seaplane.model.metadata',
 'seaplane.model.restrict',
 'seaplane.model.sql',
 'seaplane.util']

package_data = \
{'': ['*']}

install_requires = \
['attrs==21.4.0',
 'certifi==2022.6.15',
 'charset-normalizer==2.1.0',
 'idna==3.3',
 'iniconfig==1.1.1',
 'packaging==21.3',
 'pluggy==1.0.0',
 'py==1.11.0',
 'pyparsing==3.0.9',
 'requests-mock>=1.9.3,<2.0.0',
 'requests==2.28.1',
 'returns>=0.19.0,<0.20.0',
 'simplejson>=3.17.6,<4.0.0',
 'tomli==2.0.1',
 'types-requests>=2.28.0,<3.0.0',
 'types-simplejson>=3.17.7,<4.0.0',
 'urllib3==1.26.9']

setup_kwargs = {
    'name': 'seaplane',
    'version': '0.2.3',
    'description': 'Seaplane Python SDK',
    'long_description': '# Seaplane Python SDK\n[![PyPI](https://badge.fury.io/py/seaplane.svg)](https://badge.fury.io/py/seaplane)\n[![Python](https://img.shields.io/pypi/pyversions/seaplane.svg?style=plastic)](https://badge.fury.io/py/seaplane)\n\nSimple Python library to manage your resources at seaplane.\n\n## What is Seaplane?\n\nSeaplane is the global platform for building and scaling your application stack\nwithout the complexity of managing cloud infrastructure.\n\nIt serves as a reference application for how our APIs can be utilized.\n\nNot sure where to go to quickly run a workload on Seaplane? See our [Getting\nStarted] guide.\n\nTo build and test this software yourself, see the CONTRIBUTING document that is a peer to this one.\n\n## Installation\n\n```shell\npip install seaplane\n```\n\n## Configure your API KEY\n\n* Set `SEAPLANE_API_KEY` environment variable.\n* Use `config` object in order to set the api key.\n\n```python\nfrom seaplane import sea\n\nsea.config.set_api_key("your_api_key")\n```\n\n## License\n\nLicensed under the Apache License, Version 2.0, [LICENSE]. Copyright 2022 Seaplane IO, Inc.\n\n[//]: # (Links)\n\n[Seaplane]: https://seaplane.io/\n[CLI]: https://github.com/seaplane-io/seaplane/tree/main/seaplane-cli\n[SDK]: https://github.com/seaplane-io/seaplane/tree/main/seaplane\n[Getting Started]: https://github.com/seaplane-io/seaplane/blob/main/seaplane-sdk/python/docs/quickstart.md\n[CONTRIBUTING]: https://github.com/seaplane-io/seaplane/tree/main/seaplane-sdk/python/CONTRIBUTIONS.md\n[LICENSE]: https://github.com/seaplane-io/seaplane/blob/main/LICENSE\n',
    'author': 'Seaplane IO, Inc.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/seaplane-io/seaplane/tree/main/seaplane-sdk/python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
