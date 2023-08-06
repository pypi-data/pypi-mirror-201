# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cjdb', 'cjdb.modules', 'cjdb.resources', 'cjdb.test']

package_data = \
{'': ['*'], 'cjdb.test': ['files/*', 'files/cjfiles/*', 'inputs/*']}

install_requires = \
['GeoAlchemy>=0.7.2,<0.8.0',
 'numpy>=1.24.2,<2.0.0',
 'pyproj>=3.5.0,<4.0.0',
 'requests>=2.28.2,<3.0.0',
 'shapely>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'cjdb',
    'version': '1.0.0',
    'description': 'Import city.json files to postgreSQL',
    'long_description': '# cjdb\n[![MIT badge](https://img.shields.io/pypi/l/cjdb)](LICENSE) &nbsp; [![PyPI](https://img.shields.io/pypi/v/cjdb)](https://pypi.org/project/cjdb)\n\nCJDB is a tool for enabling CityJSON integration with a PostgreSQL database.\n\nAuthors: Cynthia Cai, Lan Yan, Yitong Xia, Chris Poon, Siebren Meines, Leon Powalka\n\n## Table of Contents  \n### [1. Data model](#model)\n### [2. Installation & running](#install)\n### [3. Local development](#local)\n### [4. Local CLI development](#cli)\n---\n## 1. Data model <a name="model"></a>\nFor the underlying data model see [model/README.md](model/README.md)\n\nBased on this model, there are 2 software components available:\n\n### cj2pgsql\nSee [cj2pgsql/README.md](cj2pgsql/README.md)\n\n## 2. Installation & running <a name="install"></a>\n### Using pip\n\nIt is recommended to install it in an isolated environment, because of fragile external library dependencies for CQL filter parsing.\n\n```\npip install cjdb\n```\n\n\n### Using the repository code\nAnother option is to clone the repository and build the CLI from the code.\nFrom repository root, run:\n```\npip3 install build wheel\npython3 -m build\n```\n\nThen install the .whl file with pip:\n```\npip3 install dist/*.whl --force-reinstall\n```\n\n### Using docker\nBuild:\n```\ndocker build -t cjdb:latest .\n```\n\nRun: **cj2pgsql**\n```\ndocker run --rm -it cjdb cj2pgsql --help\n```\n\nTo import some files, the `-v` option is needed to mount our local file directory in the container.\n```\ndocker run -v {MYDIRECTORY}:/data --rm -it --network=host cjdb cj2pgsql -H localhost -U postgres -d postgres -W postgres /data/5870_ext.jsonl \n```\n\nFor instructions on running the software check specific READMEs.\n\n\n## 3. Local development <a name="local"></a>\nMake sure pipenv is installed:\n```\npip install pipenv\n```\nCreate the environment:\n```\npipenv install\n```\n\n## 4. Local CLI development <a name="cli"></a>\n---\nTo build the CLI app (so that it can be called as a command line tool from anywhere):\n\n\n1. Sync the pipenv requirements with the setup.py file:\n```\npipenv run pipenv-setup sync\n```\n\n2. Create a venv just for testing the CLI build.\n\n**Note**: This is not the pipenv/development environment.\n```\nvirtualenv venv\n```\n3. Activate environment (note: this is not the pipenv environment. This is a separate environment just to test the CLI build)\n```\n. venv/bin/activate\n\n```\n\n4. Build the CLI:\n```\npython setup.py develop\n```\n\n5. The cj2pgsql importer should now work as a command inside this environment:\n```\ncj2pgsql --help\n```\n',
    'author': 'Gina Stavropoulou',
    'author_email': 'ginastavropoulou@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
