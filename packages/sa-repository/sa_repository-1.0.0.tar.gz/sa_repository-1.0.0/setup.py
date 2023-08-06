# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sa_repository']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=9.1.0,<10.0.0', 'sqlalchemy>=2.0.2,<3.0.0']

setup_kwargs = {
    'name': 'sa-repository',
    'version': '1.0.0',
    'description': 'Repository pattern for SQLAlchemy models',
    'long_description': "# SQLAlchemy Repository for models\n![tests workflow](https://github.com/Gasper3/sa-repository/actions/workflows/actions.yml/badge.svg)\n\nThis project contains simple Repository pattern for SQLAlchemy models.  \nAll you need to do is:\n1. Install this package `python -m pip install sa-repository`\n2. Use it in your project\n    ```python\n    from sa_repository import BaseRepository\n    from models import YourSAModel\n    \n    class SomeModelRepository(BaseRepository[YourSAModel]):\n        pass\n    ```\n\nBase class contains some general methods to simplify your work with sqlalchemy models e.x\n```python\nvar = SomeModelRepository(session).get(YourSAModel.attr == 'some_value')\n```\n\nIf you don't want to create new repository classes, you can use `get_repository_from_model` method\n```python\nrepository = BaseRepository.get_repository_from_model(db_session, SomeModel)\n```\n",
    'author': 'Gasper3',
    'author_email': 'trzecik65@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Gasper3/sa-repository',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
