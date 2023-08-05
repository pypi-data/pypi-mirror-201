# Failures handler - Print

[![Tests](https://github.com/mediadnan/failures_handler_print/actions/workflows/test.yml/badge.svg)](https://github.com/mediadnan/failures_handler_print/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/mediadnan/failures_handler_print/branch/main/graph/badge.svg?token=UFQKGKXQ5H)](https://codecov.io/gh/mediadnan/failures_handler_print)
[![Failures Version](https://img.shields.io/badge/Failures-v0.1-green)](https://pypi.org/project/failures/)

An official plugin for [failures](https://pypi.org/project/failures/) module that implements a default handler 
for failures, the handler is a simple function that prints colorful errors
to the console.

## Installation
You can add this plugin if ``failures`` is already installed in your environment
with the following command:

````shell
pip install failures_handler_print
````

Or you can install ``failures`` with this plugin included with the following command:

````shell
pip install "failures[print]"
````

## Testing

Let's create a file and name it ``main.py`` and put the following code into it, then save it.

````python
import failures

with failures.handle("test"):
    with failures.scope("sub"):
        with failures.scope("inner"):
            raise Exception("test error")
````

Run the script and the output should be something like:

_For windows_

![WinOutput](./_static/win_output.png)

_For Unix_

![UnixOutput](./_static/unix_output.png)
