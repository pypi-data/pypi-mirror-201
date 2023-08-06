# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cjdb',
 'cjdb.model',
 'cjdb.model.sqlalchemy_models',
 'cjdb.modules',
 'cjdb.resources']

package_data = \
{'': ['*']}

install_requires = \
['geoalchemy2>=0.13.1,<0.14.0',
 'numpy>=1.24.2,<2.0.0',
 'psycopg2-binary>=2.9.6,<3.0.0',
 'pyproj>=3.5.0,<4.0.0',
 'requests>=2.28.2,<3.0.0',
 'shapely>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['cjdb = cjdb.main:main']}

setup_kwargs = {
    'name': 'cjdb',
    'version': '1.1.0',
    'description': 'CJDB is a tool that enables CityJSON integration with a PostgreSQL database',
    'long_description': '# cjdb\n[![MIT badge](https://img.shields.io/pypi/l/cjdb)](LICENSE) &nbsp; [![PyPI](https://img.shields.io/pypi/v/cjdb)](https://pypi.org/project/cjdb)\n\nCJDB is a tool for enabling CityJSON integration with a PostgreSQL database.\n\nAuthors: Cynthia Cai, Lan Yan, Yitong Xia, Chris Poon, Siebren Meines, Leon Powalka\n\nMaintainer: Gina Stavropoulou\n\n## Table of Contents  \n### [1. Data model](#model)\n### [2. Installation & running](#install)\n### [3. Local development](#local)\n### [4. Running tests](#tests)\n---\n## 1. Data model <a name="model"></a>\nFor the underlying data model see [cjdb/model/README.md](cjdb/model/README.md)\n\n\n## 2. Installation & running <a name="install"></a>\n### Using pip\n\n```bash\npip install cjdb\n```\nIt is recommended to install it in an isolated environment, because of fragile external library dependencies for CQL filter parsing.\n\n### Using docker\nBuild:\n```bash\ndocker build -t cjdb:latest .\n```\n\nRun:\n```bash\ndocker run --rm -it cjdb cjdb --help\n```\n\nTo import some files, the `-v` option is needed to mount our local file directory in the container:\n```bash\ndocker run -v {MYDIRECTORY}:/data --rm -it --network=host cjdb cjdb -H localhost -U postgres -d postgres -W postgres /data/5870_ext.jsonl \n```\n\n## 3. Local development <a name="local"></a>\nMake sure `poetry` is installed. Then, to create a local environment with all the necessary dependencies, run from the repository root:\n```bash\npoetry install\n```\n\nTo build the wheel run:\n```bash\npoetry build\n```\n\nThen install the .whl file with pip:\n```bash\npip3 install dist/*.whl --force-reinstall\n```\n\nThen you can run the CLI command:\n```bash\ncjdb --help\n```\n\n## 4. Running tests <a name="tests"></a>\n---\nModify the arguments for the database connection to your own settings in:\n- /tests/cli_test.py\n\nThen run:\n```bash\npytest -v\n```\n\n\n\n\n\n',
    'author': 'Cynthia Cai',
    'author_email': 'None',
    'maintainer': 'Gina Stavropoulou',
    'maintainer_email': 'g.stavropoulou@tudelft.nl',
    'url': 'https://github.com/tudelft3d/cjdb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
