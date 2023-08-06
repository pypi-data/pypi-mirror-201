
"""
The library provides two packages, services and data, for constructing HTTP requests
to interact with the lementpro

The services package contains modules and methods for calling each lementpro API methods

The data package contains modules with data classes for making objects lementpro,
which you can send or receive in services package

To use the lementpro library, simply import the services and data packages
and use classes and methods in the services package for calling lementpro API methods
and use data package for making body/params and for research response body
"""

from .services import *
from .data import *
