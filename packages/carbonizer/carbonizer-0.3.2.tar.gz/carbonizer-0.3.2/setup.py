# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['carbonizer']

package_data = \
{'': ['*']}

install_requires = \
['bump2version>=1.0.1,<2.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pyppeteer>=1.0.2,<2.0.0',
 'rich>=13.3.3,<14.0.0',
 'sphinx-copybutton>=0.5.1,<0.6.0',
 'sphinx-rtd-theme>=1.2.0,<2.0.0',
 'sphinx>=6.1.3,<7.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['carbonize = carbonizer.cli:carbonize']}

setup_kwargs = {
    'name': 'carbonizer',
    'version': '0.3.2',
    'description': 'A Small CLI to utilize Carbon.now.sh',
    'long_description': 'Carbonizer\n============\n\nA Python CLI to create carbonized versions of your code. \nThis projects is based on: Carbon_, Pyppetter_\nand the wonderful Typer_ Framework.\n\n\nInstallation:\n-----------------\n\n\n.. code-block:: bash\n\n    $ pip install carbonizer\n\n\n\nUsage\n-----------\n\n\n.. code-block:: bash \n\n    carbonizer --help\n    # This creates a carbonized version in the same directory\n    carbonizer some_file.py \n    \n    # To create the output in a specific folder\n    carbonizer -o target  some_file.py\n    \n    # This will grab all files and carbonize them\n    carbonizer -o target . \n    \n    # The -c flag directly copied the output into your clipboard\n    carbonizer -c some_file.py\n    \n    # If you prefer to run the raw code you can also use the project like \n    python __main__.py  -t "one-light" carbonizer -o target\n\n\nNote: The copy functionality is only tested on Linux devices - while Mac is also supported theoretically, there is no support for windows.\n\n\n.. _Typer: https://typer.tiangolo.com/\n.. _Carbon: https://carbon.now.sh\n.. _Pyppetter: https://miyakogi.github.io/pyppeteer/index.html\n',
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
