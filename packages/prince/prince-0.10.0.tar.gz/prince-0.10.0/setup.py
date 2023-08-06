# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prince']

package_data = \
{'': ['*'], 'prince': ['datasets/*']}

install_requires = \
['altair>=4.2.2,<5.0.0', 'pandas>=1.4.1,<2.0.0', 'scikit-learn>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'prince',
    'version': '0.10.0',
    'description': 'Factor analysis in Python: PCA, CA, MCA, MFA, FAMD, GPA',
    'long_description': 'None',
    'author': 'Max Halford',
    'author_email': 'maxhalford25@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
