# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gen_markdown', 'gen_markdown.test']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gen-markdown',
    'version': '0.0.1',
    'description': '',
    'long_description': '# gen-markdown\nPure python library for generating markdown files\n',
    'author': 'Jordan Paoletti',
    'author_email': 'jordanspaoletti@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
