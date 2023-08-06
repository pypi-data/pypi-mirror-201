quickGPT
========

|PyPI - Downloads| |PyPI|

.. figure:: https://raw.githubusercontent.com/benbaptist/quickgpt/main/screenshot.png
   :alt: example of quickgpt command

   example of quickgpt command

**quickGPT** is a lightweight and easy-to-use Python library that
provides a simplified interface for working with the new API interface
of OpenAI’s ChatGPT. With quickGPT, you can easily generate natural
language responses to prompts and questions using state-of-the-art
language models trained by OpenAI.

For the record, this README.md was (mostly) generated with ChatGPT.
That’s why it’s a little braggy.

Installation
------------

You can install **quickGPT** using pip:

.. code:: sh

   pip install quickgpt

Usage
-----

To use quickgpt, you’ll need an OpenAI API key, which you can obtain
from the OpenAI website. Once you have your API key, you can specify
your API key using an environment variable:

::

   export OPENAI_API_KEY="YOUR_API_KEY_HERE"

or by passing it to the ``api_key`` parameter of ``QuickGPT``:

::

   chat = QuickGPT(api_key="YOUR_API_KEY_HERE")

See the examples for more information on how it works. Or, you can use
the ``quickgpt`` tool for an interactive ChatGPT session in your command
line. Make sure ``~/.local/bin/`` is in your ``$PATH``.

::

   usage: quickgpt [-h] [-k API_KEY] [-t THREAD] [-p PROMPT] [-l] [-n] [-i] [-v]

   Interactive command line tool to access ChatGPT

   options:
     -h, --help            show this help message and exit
     -k API_KEY, --api-key API_KEY
                           Specify an API key to use with OpenAI
     -t THREAD, --thread THREAD
                           Recall a previous conversation, or start a new one
                           with the provided identifer
     -p PROMPT, --prompt PROMPT
                           Specify the initial prompt
     -l, --list            Lists saved threads
     -n, --no-initial-prompt
                           Disables the initial prompt, and uses the User's first
                           input as the prompt
     -i, --stdin           Takes a single prompt from stdin, and returns the
                           output via stdout
     -v, --version         Returns the version of the QuickGPT library (and this
                           command)

Documentation
-------------

There’s no documentation yet. Stay tuned.

Contributing
------------

If you find a bug or have an idea for a new feature, please submit an
issue on the GitHub repository. Pull requests are also welcome!

License
-------

This project is licensed under the MIT License.

.. |PyPI - Downloads| image:: https://img.shields.io/pypi/dm/quickgpt?style=for-the-badge
   :target: https://pypi.org/project/quickgpt/
.. |PyPI| image:: https://img.shields.io/pypi/v/quickgpt?style=for-the-badge
   :target: https://pypi.org/project/quickgpt/
