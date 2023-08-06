# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiva',
 'aiva.core',
 'aiva.core.assistants',
 'aiva.core.assistants.classes',
 'aiva.core.chatbots',
 'aiva.core.chatbots.classes',
 'aiva.core.exceptions',
 'aiva.core.types',
 'aiva.core.utils',
 'aiva.core.utils.classes',
 'aiva.core.utils.enums',
 'aiva.core.utils.mixins']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.27.2,<0.28.0', 'tiktoken>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'aiva-core',
    'version': '0.1.0',
    'description': 'A repository for AIVA, the AI Virtual Assistant written in Python.',
    'long_description': '# aiva-core\nA repository for AIVA, the AI Virtual Assistant written in Python.\n',
    'author': "Sean O'Leary",
    'author_email': 'seamicole@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
