Carbonizer
============

A Python CLI to create carbonized versions of your code. 
This projects is based on: Carbon_, Pyppetter_
and the wonderful Typer_ Framework.


Installation:
-----------------


.. code-block:: bash

    $ pip install carbonizer



Usage
-----------


.. code-block:: bash 

    carbonizer --help
    # This creates a carbonized version in the same directory
    carbonizer some_file.py 
    
    # To create the output in a specific folder
    carbonizer -o target  some_file.py
    
    # This will grab all files and carbonize them
    carbonizer -o target . 
    
    # The -c flag directly copied the output into your clipboard
    carbonizer -c some_file.py
    
    # If you prefer to run the raw code you can also use the project like 
    python __main__.py  -t "one-light" carbonizer -o target


Note: The copy functionality is only tested on Linux devices - while Mac is also supported theoretically, there is no support for windows.


.. _Typer: https://typer.tiangolo.com/
.. _Carbon: https://carbon.now.sh
.. _Pyppetter: https://miyakogi.github.io/pyppeteer/index.html
