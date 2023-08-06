# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pg_docker']

package_data = \
{'': ['*']}

install_requires = \
['psycopg2>=2.9.5,<3.0.0']

entry_points = \
{'pytest11': ['pg_docker = pg_docker._plugin']}

setup_kwargs = {
    'name': 'pg-docker',
    'version': '0.7.0',
    'description': '',
    'long_description': '# PG Docker\n\nA python package to provide containerized postgres databases in python\n\n**Why would you need this?**\n\nIf you are using postgres and want to write tests that run against a real database, then this will make your life easier.\n\n## Installation\n\nInstall via pip:\n```\npip install pg-docker\n```\n\nYou will also need to have [docker](https://www.docker.com/).\n\n## Usage\n\nNote: *This package is mainly built with pytest in mind, but you can use the context managers documented below with other testing frameworks as well.*\n\n### Example\n\nWith pytest:\n```py\nimport psycopg2\n\n\npytest_plugins = ["pg_docker"]\n\n\ndef test_using_a_database(pg_database):\n    db_connection = psycopg2.connect(**pg_database.connection_kwargs())\n    cursor = db_connection.cursor()\n    cursor.execute("SELECT \'hello world!\'")\n\n    assert cursor.fetchone() == ("hello world!",)\n```\n\n### Usage with pytest\n\nYou first need to enable the plugin. To do this add a `conftest.py` to the root directory of your tests and add:\n```py\npytest_plugins = ["pg_docker"]\n```\nYou can find more details on how to activate plugins in the [pytest docs](https://docs.pytest.org/en/latest/how-to/plugins.html#requiring-loading-plugins-in-a-test-module-or-conftest-file)\n\nThe plugin The following fixtures:\n\n - `pg_database`: `DatabaseParams` for a clean database.\n - `pg_database_pool`: A `DatabasePool` instance. Use this if you need more than one database in your tests at a time.\n\n\n### Configuring Database Migrations\n\nUse the below template in your `conftest.py` to configure how your databases are set up. \n```py\ndef setup_db(pg_params):\n    """Add any setup logic for your database in here."""\n    pass\n\n@pytest.fixture(scope="session")\ndef pg_setup_db():\n    return setup_db\n```\nNote: *You might be inclined to edit the above code to nest the setup_db function inside of the fixture function. This will not work, because the fixture result needs to be [pickleable](https://docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled)!*\n\n\n### Advanced Usage (and other testing frameworks)\n\nFor other use cases you can use the `database_pool` context manager:\n```py\nwith database_pool() as db_pool:\n    with db_pool.database as db_params:\n        connection = psycopg2.connect(**db_params.connection_kwargs())\n```\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
