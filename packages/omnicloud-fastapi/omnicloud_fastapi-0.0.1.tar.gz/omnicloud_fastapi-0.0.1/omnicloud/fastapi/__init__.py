'''
Base classes & functions for building REST API faster.
'''

from pkgutil import extend_path

from ._app import BaseURL

__path__ = extend_path(__path__, __name__)  # needed for using in a distributed namespace
