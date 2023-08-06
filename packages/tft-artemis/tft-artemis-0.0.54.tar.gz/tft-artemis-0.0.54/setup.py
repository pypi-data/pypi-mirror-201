# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tft',
 'tft.artemis',
 'tft.artemis.api',
 'tft.artemis.drivers',
 'tft.artemis.scripts',
 'tft.artemis.tasks']

package_data = \
{'': ['*'], 'tft.artemis': ['schema/*', 'schema/drivers/*']}

install_requires = \
['Pint',
 'alembic',
 'click',
 'dramatiq[rabbitmq]',
 'gluetool',
 'gunicorn',
 'jinja2-ansible-filters',
 'jq',
 'jsonschema',
 'molten',
 'periodiq',
 'prometheus-client>=0.12.0,<0.13.0',
 'psycopg2',
 'pyinstrument',
 'redis',
 'sentry-sdk',
 'sqlalchemy-utils',
 'sqlalchemy>=1.4,<1.4.23',
 'stackprinter',
 'typing-extensions']

extras_require = \
{'full': ['awscli>=1.27.24,<2.0.0',
          'azure-cli',
          'beaker-client',
          'python-openstackclient']}

entry_points = \
{'console_scripts': ['artemis-api-server = tft.artemis.api:main',
                     'artemis-db-init-content = '
                     'tft.artemis.scripts.init_db_content:cmd_root',
                     'artemis-dispatcher = tft.artemis.dispatcher:main',
                     'artemis-scheduler = '
                     'tft.artemis.scripts.scheduler:cmd_root',
                     'artemis-worker = tft.artemis.scripts.worker:cmd_root']}

setup_kwargs = {
    'name': 'tft-artemis',
    'version': '0.0.54',
    'description': 'Artemis is a machine provisioning service. Its goal is to provision a machine - using a set of preconfigured providers as backends - which would satisfy the given hardware and software requirements.',
    'long_description': None,
    'author': 'Milos Prchlik',
    'author_email': 'mprchlik@redhat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<3.10.0',
}


setup(**setup_kwargs)
