# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['playground',
 'playground.core',
 'playground.core.configs',
 'playground.core.data',
 'playground.core.expcache',
 'playground.core.s3_source',
 'playground.core.tracking']

package_data = \
{'': ['*']}

install_requires = \
['boto3==1.21.0',
 'diskcache>=5.4.0,<6.0.0',
 'joblib',
 'loguru>=0.6.0,<0.7.0',
 'mlflow-skinny>=1.28.0,<2.0.0',
 'pandas',
 'polars',
 'pyarrow',
 'pygit2>=1.10.0,<2.0.0',
 's3fs',
 'scipy>=1.9.1,<2.0.0',
 'typer[all]>=0.6.1,<0.7.0']

setup_kwargs = {
    'name': 'sbm-exp-sdk',
    'version': '0.3.0',
    'description': 'playground',
    'long_description': 'None',
    'author': 'mikhail.marin',
    'author_email': 'mikhail.marin@sbermarket.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
