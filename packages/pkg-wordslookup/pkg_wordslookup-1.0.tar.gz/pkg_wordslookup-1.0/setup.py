# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pkg_wordslookup']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pkg-wordslookup',
    'version': '1.0',
    'description': 'This package will look the instances of a specific word provided as an input inside a file also provided as an input. The package will give the amount of times the word is in the file and it will print the line in which the word is placed',
    'long_description': '# pkg_wordslookup\n\nThis package will look the instances of a specific word provided as an input inside a file also provided as an input. The package will give the amount of times the word is in the file and it will print the line in which the word is placed\n\n## Installation\n\n```bash\n$ pip install pkg_wordslookup\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`pkg_wordslookup` was created by Gabriel Coronel. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`pkg_wordslookup` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Gabriel Coronel',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
