'''
This package contains classes for building Plotly Dash application.

- Bootstrapped - application with preloaded bootstrap theme

- CoLab - for running inside Google CoLab notebook

- PyScript - contains preloaded [PyScript](https://pyscript.net/) environment

- Servers - provides methods for running development server and/or production server with HTTP/2
    support and serving local static files
'''


from pkgutil import extend_path

from ._dash import Bootstrapped, CoLab, PyScript, Servers

__path__ = extend_path(__path__, __name__)  # needed for using in a distributed namespace
