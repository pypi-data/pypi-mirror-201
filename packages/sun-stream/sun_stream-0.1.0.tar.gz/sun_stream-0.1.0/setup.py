# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sun_stream']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2,<3']

setup_kwargs = {
    'name': 'sun-stream',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Sun Stream\n\nCreating a stream of sun rises and sun sets, that only yields at the time of those events.\n',
    'author': 'PowerSnail',
    'author_email': 'hj@powersnail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
