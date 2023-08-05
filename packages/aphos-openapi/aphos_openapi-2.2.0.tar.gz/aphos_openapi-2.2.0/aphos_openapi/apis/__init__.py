
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from aphos_openapi.api.catalog_api import CatalogApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from aphos_openapi.api.catalog_api import CatalogApi
from aphos_openapi.api.flux_api import FluxApi
from aphos_openapi.api.space_object_api import SpaceObjectApi
from aphos_openapi.api.user_api import UserApi
