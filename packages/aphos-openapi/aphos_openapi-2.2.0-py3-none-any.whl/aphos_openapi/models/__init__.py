# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from aphos_openapi.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from aphos_openapi.model.comparison_object import ComparisonObject
from aphos_openapi.model.error_message import ErrorMessage
from aphos_openapi.model.flux import Flux
from aphos_openapi.model.flux_data import FluxData
from aphos_openapi.model.night import Night
from aphos_openapi.model.photo_properties import PhotoProperties
from aphos_openapi.model.space_object import SpaceObject
from aphos_openapi.model.space_object_with_fluxes import SpaceObjectWithFluxes
from aphos_openapi.model.user import User
import math

