# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['abml']

package_data = \
{'': ['*']}

install_requires = \
['pyaml>=21.10.1,<22.0.0']

setup_kwargs = {
    'name': 'abml',
    'version': '0.1.4',
    'description': '',
    'long_description': '',
    'author': 'DavidNaizheZhou',
    'author_email': '70525024+DavidNaizheZhou@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==2.7.15',
}


setup(**setup_kwargs)
