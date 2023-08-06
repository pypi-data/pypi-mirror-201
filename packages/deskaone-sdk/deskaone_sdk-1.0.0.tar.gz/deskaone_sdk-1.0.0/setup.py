# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['deskaone_sdk',
 'deskaone_sdk.Client',
 'deskaone_sdk.Database',
 'deskaone_sdk.Exceptions',
 'deskaone_sdk.Internal',
 'deskaone_sdk.Utils']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.1.1,<3.0.0',
 'colorama>=0.4.6,<0.5.0',
 'flask>=2.2.3,<3.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'install-jdk>=0.3.0,<0.4.0',
 'psycopg2>=2.9.5,<3.0.0',
 'pycryptodome>=3.17,<4.0',
 'pysocks>=1.7.1,<2.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'random-user-agent>=1.0.1,<2.0.0',
 'requests[socks]>=2.28.2,<3.0.0',
 'sqlalchemy==1.4.29']

setup_kwargs = {
    'name': 'deskaone-sdk',
    'version': '1.0.0',
    'description': '',
    'long_description': 'DesKaOne SDK',
    'author': 'Antoni Oktha Fernandes',
    'author_email': '37358597+DesKaOne@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
