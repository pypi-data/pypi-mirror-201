# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['carbonizer']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'pyppeteer>=1.0.2,<2.0.0',
 'rich>=13.3.3,<14.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['carbonize = carbonizer.cli:carbonize']}

setup_kwargs = {
    'name': 'carbonizer',
    'version': '0.3.1',
    'description': 'A Small CLI to utilize Carbon.now.sh',
    'long_description': '# Carbonizer\n\nA Python CLI to create carbonized versions of your code. \nThis projects is based on: [Carbon](carbon.now.sh), [Pyppetter](https://miyakogi.github.io/pyppeteer/index.html)\nand the wonderful [Typer](https://typer.tiangolo.com/) Framework.\n\n\n## Installation:\n\n```bash\n$ pip install carbonizer\n```\n\n\n## Usage\n\n```bash \ncarbonizer --help\n# This creates a carbonized version in the same directory\ncarbonizer some_file.py \n\n# To create the output in a specific folder\ncarbonizer -o target  some_file.py\n\n# This will grab all files and carbonize them\ncarbonizer -o target . \n\n# The -c flag directly copied the output into your clipboard\ncarbonizer -c some_file.py\n\n# If you prefer to run the raw code you can also use the project like \npython __main__.py  -t "one-light" carbonizer -o target\n```\n\nNote: The copy functionality is only Linux  is tested  while Mac is also supported - theoretically.\n',
    'author': 'marvin taschenberger',
    'author_email': 'marvin.taschenberger@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
