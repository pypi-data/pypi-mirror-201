# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fatld']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.3,<4.0.0',
 'numpy>=1.24.2,<2.0.0',
 'oapackage>=2.7.6,<3.0.0',
 'pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'fatld',
    'version': '0.1.3',
    'description': 'Generate and characterize designs with four-and-two-level (FATL) factors',
    'long_description': '# Four And Two Level Designs\n\n[![PyPI version](https://badge.fury.io/py/fatld.svg)](https://badge.fury.io/py/fatld)\n[![CI](https://github.com/ABohynDOE/fatld/actions/workflows/CI.yml/badge.svg)](https://github.com/ABohynDOE/fatld/actions/workflows/CI.yml)\n\nThe `fatld` package contains functionality to generate and characterize designs with four-and-two-level (FATL) factors.\nDesign characteristics include word length pattern, defining relation, and number of clear interactions.\nFor more information about the package see the documentation at [https://abohyndoe.github.io/fatld/](https://abohyndoe.github.io/fatld/).\nA large collection of FATL designs can be explored interactively using a web app at [https://abohyndoe.shinyapps.io/fatldesign-selection-tool/](https://abohyndoe.shinyapps.io/fatldesign-selection-tool/).\n\n## Usage\n\nThe package can be used from Python:\n\n```python\n>>> import fatld\n>>> D = fatld.Design(runsize=32, m=1, cols=[21, 27, 29])\n>>> D.wlp()\n[1, 3, 3, 0, 0]\n>>> D.defining_relation()\n[\'A1cef\', \'A3deg\', \'A1cdeh\']\n>>> print("There are %s 2-2 interactions totally clear from any main effect or other interaction." % D.clear(\'2-2\', \'all\'))\nThere are 6 2-2 interactions totally clear from any main effect or other interaction.\n>>> print("The design contains %s four-level factors and %s two-level factors" % (D.m, D.n))\nThe design contains 1 four-level factors and 6 two-level factors\n```\n\nFor more examples see the documentation.\n\n## Installation\n\nThe Python interface to the package is available on pypi. Installation can be done using the following command:\n\n```bash\npip install fatld\n```\n\n## Development\n\nAll development is done in a virtual environment based on `poetry`, activate it using:\n\n```shell\npoetry shell\n```\n\n### Code style\n\n* Try to follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide. A usefull tool for automated formatting is [black](https://pypi.python.org/pypi/black). We do allow lines upto 120 characters.\n* Document functions using the [Numpy docstring](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html#example-numpy) convention\n\n* Linting is based on `ruff`, configuration is found in the [pyproject.toml](pyproject.toml) file.\n\n* Tests are ran using `pytest` and a coverage report can be generated using `coverage` inside the virtual environment:\n\n    ```shell\n    coverage run -m pytest tests\n    coverage report -m\n    ```\n\n### Submitting code\n\nIf you would like to contribute, please submit a pull request. (See the [Github Hello World](https://guides.github.com/activities/hello-world/) example, if you are new to Github).\n\nBy contributing to the repository you state you own the copyright to those contributions and agree to include your contributions as part of this project under the BSD license.\n\n### Bugs reports and feature requests\n\nTo submit a bug report or feature request use the [Github issue tracker](https://github.com/ABohynDOE/fatld/issues).\nSearch for existing and closed issues first. If your problem or idea is not yet addressed, please open a new issue.\n\n### Contact\n\nFor further information please contact alexandre dot bohyn at kuleuven dot be\n',
    'author': 'Alexandre Bohyn',
    'author_email': 'alexandre.bohyn@kuleuven.be',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://abohyndoe.github.io/fatld/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
