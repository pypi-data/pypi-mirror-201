# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sun_stream']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2,<3']

extras_require = \
{'docs': ['mkdocs>=1.4.2,<2.0.0', 'mkdocstrings[python]>=0.20.0,<0.21.0']}

setup_kwargs = {
    'name': 'sun-stream',
    'version': '0.1.1',
    'description': 'Creating a stream of sun rises and sun sets, that only yields at the time of those events.',
    'long_description': '# Sun Stream\n\nCreating a stream of sun rises and sun sets, that only yields at the time of those events.\n',
    'author': 'PowerSnail',
    'author_email': 'hj@powersnail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/PowerSnail/sun_stream',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
