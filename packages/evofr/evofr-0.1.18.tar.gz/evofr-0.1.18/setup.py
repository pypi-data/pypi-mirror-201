# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['evofr',
 'evofr.data',
 'evofr.infer',
 'evofr.models',
 'evofr.models.renewal_model',
 'evofr.models.renewal_model.basis_functions',
 'evofr.plotting',
 'evofr.posterior']

package_data = \
{'': ['*']}

install_requires = \
['blackjax>=0.9.6,<0.10.0',
 'jax>=0.3.13,<0.4.0',
 'jaxlib>=0.3.10,<0.4.0',
 'numpy>=1.22.4,<2.0.0',
 'numpyro>=0.9.2,<0.10.0',
 'pandas>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'evofr',
    'version': '0.1.18',
    'description': 'Tools for evolutionary forecasting.',
    'long_description': 'None',
    'author': 'marlinfiggins',
    'author_email': 'marlinfiggins@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
