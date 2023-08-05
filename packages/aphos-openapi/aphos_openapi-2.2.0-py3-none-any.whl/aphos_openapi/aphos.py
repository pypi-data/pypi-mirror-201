"""Module providing access to APhoS database through API"""

import io as _io  # type: ignore
import os as _os
from typing import Optional as _Optional
from typing import List as _List
from typing import Union as _Union
from typing import Tuple as _Tuple
from astropy.coordinates import SkyCoord as _SkyCoord  # type: ignore

import aphos_openapi  # type: ignore
from aphos_openapi.models.coordinates import Coordinates


DEFAULT_CATALOG = "UCAC4"

ALL_CATALOGS = "All catalogues"

_DEV_CONSTANT = 2.5/aphos_openapi.math.log(10)

_READ_ME = "https://test.pypi.org/project/aphos-openapi/"

_WEBSITE = "https://ip-147-251-21-104.flt.cloud.muni.cz/"


def get_catalogs() -> _Optional[_List[str]]:
    """
    Get all available catalogs from APhoS.

    Returns: List of available catalogs (strings).

    """
    # Enter a context with an instance of the API client
    with aphos_openapi.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = aphos_openapi.catalog_api.CatalogApi(api_client)

        try:
            # Find all catalogs
            return api_instance.get_catalogs()
        except aphos_openapi.OpenApiException as exc:
            print(exc)
            return None


def get_object(object_id: str, catalog: str = DEFAULT_CATALOG) \
        -> _Optional[aphos_openapi.models.SpaceObjectWithFluxes]:
    """
    Get object from APhoS based on parameters.

    Args:
        object_id: object id of the space object
        catalog: catalog of the space object

    Returns: SpaceObjectWithFluxes or None if there is no such object.

    """
    with aphos_openapi.ApiClient() as api_client:
        api_instance = aphos_openapi.space_object_api.SpaceObjectApi(api_client)

        try:
            return api_instance.get_space_object_by_id(object_id, catalog=catalog)
        except aphos_openapi.OpenApiException as exc:
            print(exc)
            return None


def get_objects_by_params(object_id: _Optional[str] = None, catalog: _Optional[str] = None,
                          name: _Optional[str] = None, coordinates: _Optional[Coordinates] = None,
                          min_mag: _Union[str, float, None] = None,
                          max_mag: _Union[str, float, None] = None) -> \
        _Optional[_List[aphos_openapi.models.SpaceObject]]:
    """
    Get space objects based on multiple parameters, where every can be None.

    Args:
        object_id: object id of the space object
        catalog: catalog of space objects
        name: name of space objects
        coordinates: coordinates
        min_mag: minimum magnitude (0 and more)
        max_mag: maximum magnitude (20 and less)

    Returns: List of space objects.

    """
    if min_mag is not None and float(min_mag) >= 15 and max_mag is None:
        max_mag = 20
    local_args = locals().copy()

    try:
        params = dict()
        for key in local_args.keys():
            if local_args[key] is not None:
                if key == 'coordinates':
                    local_args[key] = str(local_args[key])
                params[key] = local_args[key]
        with aphos_openapi.ApiClient() as api_client:
            api_instance = aphos_openapi.space_object_api.SpaceObjectApi(api_client)
            return api_instance.find_space_objects_by_params(**params)
    except aphos_openapi.OpenApiException as exc:
        print(exc)
        return None


def get_var_cmp_by_ids(variable_id: str, comparison_id: str,
                       var_catalog: str = DEFAULT_CATALOG,
                       cmp_catalog: str = DEFAULT_CATALOG) \
        -> _Optional[aphos_openapi.models.ComparisonObject]:
    """
    Get Comparison object of variable star (space object) and comparison star based on IDs.

    Args:
        variable_id: id of variable star
        comparison_id: id of comparison star
        var_catalog: catalog of variable star
        cmp_catalog: catalog of comparison star

    Returns: Data about objects and fluxes.

    """
    try:
        with aphos_openapi.ApiClient() as api_client:
            api_instance = aphos_openapi.space_object_api.SpaceObjectApi(api_client)
            return api_instance.get_comparison_by_identificators \
                (variable_id, comparison_id, original_cat=var_catalog, reference_cat=cmp_catalog)
    except aphos_openapi.OpenApiException as exc:
        print(exc)
        return None


def get_user(username: str) -> _Optional[aphos_openapi.models.User]:
    """
    Get user by username.

    Args:
        username: username of a user

    Returns: User (username and description).

    """
    try:
        with aphos_openapi.ApiClient() as api_client:
            api_instance = aphos_openapi.user_api.UserApi(api_client)
            return api_instance.get_user_by_username(username)
    except aphos_openapi.OpenApiException as exc:
        print(exc)
        return None


def set_var_cmp_apertures(comparison: aphos_openapi.models.ComparisonObject,
                          night: _Optional[aphos_openapi.datetime.date] = None, var: _Optional[int] = None,
                          cmp: _Optional[int] = None) -> None:
    """
    Sets apertures based on night and desired indexes in comparison object and
    recalculates magnitude and deviation.

    Args:
        comparison: ComparisonObject - object to which the apertures are set
        night: night to which the apertures are changing (None is all nights)
        var: target index of aperture to set (from variable star)
        cmp: target index of aperture to set (from comparison star)
    """
    ignore = False
    night_str = ""
    if night is None:
        ignore = True
    else:
        night_str = str(night.strftime("%d-%m-%Y"))
    for flux in comparison.data:

        if ignore or flux.night.first_date_of_the_night == night_str:

            ap_len = len(flux.apertures)
            ref_ap_len = len(flux.cmp_apertures)
            if (var is not None and not 0 <= var < ap_len) or \
                    (cmp is not None and not 0 <= cmp < ref_ap_len):
                # in case of variable lengths, this needs to be modified with continue
                raise IndexError(f"Index out of bounds, use None or {0}-{min(ap_len, ref_ap_len) - 1}")

            flux.night.ap_to_be_used = str(var) if var is not None else "auto"
            flux.night.cmp_ap_to_be_used = str(cmp) if cmp is not None else "auto"

            orig_ap = flux.apertures[var] if var is not None else flux.ap_auto
            ref_ap = flux.cmp_apertures[cmp] if cmp is not None else flux.cmp_ap_auto

            if not orig_ap == "saturated" and not ref_ap == "saturated":
                flux.magnitude = \
                    round(-2.5 * aphos_openapi.math.log(float(orig_ap) / float(ref_ap), 10), 7)
                orig_dev = flux.aperture_devs[var] if var is not None else flux.ap_auto_dev
                ref_dev = flux.cmp_aperture_devs[cmp] if cmp is not None else flux.cmp_ap_auto_dev
                var_sq = (orig_dev / float(orig_ap)) ** 2
                cmp_sq = (ref_dev / float(ref_ap)) ** 2
                flux.deviation = round(_DEV_CONSTANT * ((var_sq + cmp_sq) ** 0.5), 8)
            else:
                flux.magnitude = float('-inf')
                flux.deviation = None


def resolve_name_aphos(name: str) -> _Optional[_List[aphos_openapi.models.SpaceObject]]:
    """
    Resolve name based on astropy name resolver and tries to find equal potential objects
    in APhoS database (Cross-identification).

    !WARNING- it resolves based on coordinates and is not always correct!

    Args:
        name: any name by which a space object can be resolved

    Returns: List of space objects which are potentially equal to given name, from all catalogs.

    """
    try:
        astropy_coords = _SkyCoord.from_name(name)
    except:
        return None
    coord = Coordinates(astropy_coords, 1, radius_unit='s')
    res = get_objects_by_params(coordinates=coord)
    if res is not None and len(res) == 0:
        coord = Coordinates(astropy_coords, 3, radius_unit='s')
        res = get_objects_by_params(coordinates=coord)
    return res


def _upload_files(path: str) -> _List[_Tuple[str, bool, str]]:
    """
    Upload files as Anounymous user. Files are in format csv, with delimiter ';',
    generated from SIPS software. For authenticated upload use website -> info().

    Args:
        path: path to file or directory with files

    Returns: List of tuple (file, success of upload of the given file, info about upload).

    """
    with aphos_openapi.ApiClient() as api_client:
        api_instance = aphos_openapi.space_object_api.SpaceObjectApi(api_client)
        res = []
        if _os.path.isdir(path):
            files_threads = []
            for file in _os.listdir(path):
                os_path = _os.path.join(path, file)
                if _os.path.isfile(os_path):
                    csv_file = _io.FileIO(os_path, 'rb')
                    files_threads.append((file, api_instance.upload_csv(file=csv_file, async_req=True)))
            for file, thread in files_threads:
                try:
                    res.append((file, True, thread.get()))
                except aphos_openapi.ApiException as exc:
                    res.append((file, False, str(exc.status)))
        else:
            csv_file = _io.FileIO(path, 'rb')
            try:
                res.append((path, True, api_instance.upload_csv(file=csv_file)))
            except aphos_openapi.ApiException as exc:
                res.append((path, False, str(exc.status)))
        return res


def info() -> None:
    """
    Prints useful documentation and info about this package.
    """
    print(f"help -> documentation -> {_READ_ME}")
    print("APhoS version: "
          + aphos_openapi.pkg_resources.require("aphos_openapi")[0].version)
    print(f"Website can be found here: {_WEBSITE}")
