# APhoS client for retrieving data in Python

This is Amateur Photometric Survey (APhoS) Application Programming Interface.  
Contains models and functions for work with data in APhoS database.  
Server is accessible from: https://ip-147-251-21-104.flt.cloud.muni.cz/  
Swagger UI (Interface for api of the server): https://ip-147-251-21-104.flt.cloud.muni.cz/swagger-ui/index.html  
Openapi json or yaml file (documentation of api): https://ip-147-251-21-104.flt.cloud.muni.cz/api-docs

## Installation
### Package: `aphos_openapi`

Install: `pip install aphos-openapi`  
Upgrade: `pip install aphos_openapi --upgrade`
(If you have pip3 instead of pip, just use pip3)

## Contents
References work only in github: https://github.com/pavel-kinc/aphos-client/blob/main/README.md
* [Basic info](README.md#aphos-client-for-retrieving-data-in-python)
* [Installation](README.md#installation)
* [Requirements](README.md#requirements)
* [Basic usage](README.md#usage-api-models)
* [Coordinates usage](README.md#usage-coordinates)
* [GraphData usage](README.md#usage-graphdata)
* [Support](README.md#support)
* [Functions documentation](README.md#documentation-for-functions)
* [Api models documentation](README.md#documentation-for-models)


## Requirements

* Python >=3.8,
* 'urllib3'>=1.25.3,
* 'python-dateutil',
* 'matplotlib',
* 'astropy'


## Usage Api models

```
from aphos_openapi import aphos
import datetime  # for setting apertures
from pprint import pprint  # pretty print for objects

def my_function():

    """
    Basic usage, info, get_objects_by_params, get_object
    """
    aphos.info()  # prints basic info about aphos_openapi package
    objects = aphos.get_objects_by_params(name="GK Cep") # gets objects which match the name
    if objects:
        print(objects[0].magnitude) # prints magnitude of first found object
    # pprint(objects[0])
    list_of_stars = aphos.get_objects_by_params()  # gets 100 space objects from database
    star = aphos.get_object("605-025126", "UCAC4")  # gets space object with fluxes

    """
    get_var_cmp_by_ids, set_var_cmp_apertures, resolve_name_aphos
    """
    if star is not None:
        comparison = aphos.get_var_cmp_by_ids(star.id, "604-024943", star.catalog, "UCAC4")
        pprint(comparison.variable)
        # pprint(comparison.data[0])
        if comparison is not None:
            date = datetime.date(2022,1, 6)  # first day of night we want to change apertures
            aphos.set_var_cmp_apertures(comparison, date, 3, 3)
            # pprint(comparison.data[0])
            aphos.set_var_cmp_apertures(comparison)  # back to auto apertures
            # pprint(comparison)
            
    potential_stars = aphos.resolve_name_aphos("V* FU Aur")
    if potential_stars:
        star = potential_stars[0]
        print(f"{star.id} {star.catalog} {str(star.magnitude)}")


if __name__ == '__main__':
    my_function()
```

## Usage Coordinates
__More info about object in package.__

```
from aphos_openapi import aphos
from aphos_openapi.models.coordinates import Coordinates
from astropy.coordinates import SkyCoord
from pprint import pprint  # pretty print for objects

"""
Coordinates can take astropy.coordinates SkyCoord or other strings format listed below.
If units are present in string, unit will be ignored.
Radius is float, and you can choose unit by 'm' or 's', otherwise it will be degrees.

Coordinates below are more or less equal, more in class documentation.
"""
coords1 = Coordinates("21h41m55.291s +71d18m41.12s", 8, radius_unit='m')
coords2 = Coordinates("21 41 55.291 +71 18 41.12", 0.1333333)  # default unit for RA is hour
coords3 = Coordinates(SkyCoord("21h41m55.291s +71d18m41.12s"), 0.1333333)
coords4 = Coordinates("21.698691944444448h +71.31142223d", 0.1333333)
coords5 = Coordinates("21:41:55.291 +71:18:41.12", 0.1333333)
coords6 = Coordinates("325.48037916666664d +71.31142223d", 0.1333333)
coords7 = Coordinates("325 28 49.365 +71 18 41.12", 8, 'd', 'm')

space_objects = aphos.get_objects_by_params(coordinates=coords7)
pprint(space_objects)
```

## Usage GraphData
__Main methods:__ 
* constructor 
* to_file()
* graph()
* composite_graph()
* phase_graph()

__More info about methods in package.__

```
from aphos_openapi import aphos
from aphos_openapi.models.graph_data import GraphData
from pprint import pprint  # pretty print for objects

var_cmp = aphos.get_var_cmp_by_ids("605-025126", "604-024943")
if var_cmp is not None:
    data = GraphData(var_cmp)  # create GraphData object from Comparison
    # pprint(data)
    data.graph()  # matplotlib graph
    data.to_file("path/to/file.csv")  # saves data to file
data_from_file = GraphData("path/to/file.csv")  # create GraphData from file
pprint(f"{data_from_file.variable} {data_from_file.comparison}")
pprint(data_from_file.data_list[0])  # print how 1 row of data looks like
data_from_file.composite_graph()
data_from_file.phase_graph(2455957.5, 1.209373)  # start of epoch and period
```

## Support

pavelkinc230@gmail.com

## Additional information for functions and models of this package

## Documentation For Functions
#### get_catalogs() -> Optional[List[str]]
Get all available catalogs from APhoS.  
Returns: List of available catalogs (strings).
<br/><br/>


#### get_object(<br/>object_id: str,<br/>catalog: str = DEFAULT_CATALOG) <br/>-> Optional[SpaceObjectWithFluxes]
Get object from APhoS based on parameters.  
Returns: SpaceObjectWithFluxes or None if there is no such object.  
Params:  
&emsp;object_id - object id of the space object  
&emsp;catalog - catalog of the space object
<br/><br/>

#### get_objects_by_params(<br/>object_id: Optional[str] = None, <br/> catalog: Optional[str] = None,<br/> name: Optional[str] = None, <br/>coordinates: Optional[Coordinates] = None,<br/> min_mag: Union[str, float, None] = None,<br/> max_mag: Union[str, float, None] = None) <br/>-> Optional[list[SpaceObject]]
Get space objects based on multiple parameters, where every can be None.  
Returns: List of space objects.  
Params:  
&emsp;object_id - object id of the space object  
&emsp;catalog - catalog of space objects  
&emsp;name - name of space objects  
&emsp;coordinates - coordinates  
&emsp;min_mag - minimum magnitude (0 and more)  
&emsp;max_mag - maximum magnitude (20 and less)
<br/><br/>

#### get_var_cmp_by_ids(<br/>variable_id: str,<br/>comparison_id: str,<br/>var_catalog: str = DEFAULT_CATALOG,<br/>cmp_catalog: str = DEFAULT_CATALOG) <br/>-> Optional[ComparisonObject]
Get Comparison object of variable star (space object) and comparison star based on IDs.  
Returns: Data about objects and fluxes.  
Params:  
&emsp;variable_id - id of variable star  
&emsp;comparison_id - id of comparison star  
&emsp;var_catalog - catalog of variable star  
&emsp;cmp_catalog - catalog of comparison star
<br/><br/>

#### get_user(<br/>username: str)<br/> -> Optional[User]
Get user by username.  
Returns: User (username and description).  
Params:  
&emsp;username - username of a user
<br/><br/>

#### set_var_cmp_apertures(<br/>comparison: ComparisonObject,<br/>night: Optional[date] = None,<br/>var: Optional[int] = None,<br/>cmp: Optional[int] = None)<br/> -> None
Sets apertures based on night and desired indexes in comparison object and recalculates magnitude and deviation.  
Params:  
&emsp;comparison - ComparisonObject - object to which the apertures are set  
&emsp;night - night to which the apertures are changing (None is all nights)  
&emsp;var - target index of aperture to set (from variable star)  
&emsp;cmp - target index of aperture to set (from comparison star)
<br/><br/>

#### resolve_name_aphos(<br/>name: str) <br/>-> Optional[list[SpaceObject]]
Resolve name based on astropy name resolver and tries to find equal potential objects in APhoS database (Cross-identification).  
Returns: List of space objects which are potentially equal to given name, from all catalogs.  
Params:  
&emsp;name - any name by which a space object can be resolved
<br/><br/>

#### upload_files(<br/>path: str) <br/>-> list[tuple[str, bool, str]]
Upload files as Anounymous user. Files are in format csv, with delimiter ';', generated from SIPS software. For authenticated upload use website -> info().  
Returns: List of tuple (file, success of upload of the given file, info about upload).  
Params:  
&emsp;path - path to file or directory with files
<br/><br/>

#### info() -> None
Prints useful documentation and info about this package.  
<br/>

__Object's methods are documented in package and in usage.__

## Documentation For Models
(Api models only, mostly genereated)
References work only in github: https://github.com/pavel-kinc/aphos-client/blob/main/README.md
 - [ComparisonObject](README.md#comparisonobject)
 - [ErrorMessage](README.md#errormessage)
 - [Flux](README.md#flux)
 - [FluxData](README.md#fluxdata)
 - [Night](README.md#night)
 - [PhotoProperties](README.md#photoproperties)
 - [SpaceObject](README.md#spaceobject)
 - [SpaceObjectWithFluxes](README.md#spaceobjectwithfluxes)
 - [User](README.md#user)

### ComparisonObject

#### Properties
| Name           | Type                                     | Description | Notes |
|----------------|------------------------------------------|-------------|-------|
| **variable**   | [**SpaceObject**](README.md#spaceobject) |             |       |
| **comparison** | [**SpaceObject**](README.md#spaceobject) |             |       |
| **data**       | [**[FluxData]**](README.md#fluxdata)     |             |       |

[[Back to Model list]](README.md#documentation-for-models)

### ErrorMessage

#### Properties
| Name        | Type    | Description | Notes      |
|-------------|---------|-------------|------------|
| **id**      | **str** |             | [optional] |
| **message** | **str** |             | [optional] |

[[Back to Model list]](README.md#documentation-for-models)

### Flux

#### Properties
| Name              | Type                                             | Description | Notes |
|-------------------|--------------------------------------------------|-------------|-------|
| **right_asc**     | **str**                                          |             |       |
| **declination**   | **str**                                          |             |       |
| **added_by**      | **str**                                          |             |       |
| **ap_auto**       | **float**                                        |             |       |
| **apertures**     | **[float]**                                      |             |       |
| **photo**         | [**PhotoProperties**](README.md#photoproperties) |             |       |
| **ap_auto_dev**   | **float**                                        |             |       |
| **aperture_devs** | **[float]**                                      |             |       |

[[Back to Model list]](README.md#documentation-for-models)

### FluxData

#### Properties
| Name                  | Type                         | Description | Notes |
|-----------------------|------------------------------|-------------|-------|
| **right_asc**         | **str**                      |             |       |
| **dec**               | **str**                      |             |       |
| **ap_auto**           | **str**                      |             |       |
| **ap_auto_dev**       | **float**                    |             |       |
| **apertures**         | **[str]**                    |             |       |
| **aperture_devs**     | **[float]**                  |             |       |
| **magnitude**         | **float**                    |             |       |
| **deviation**         | **float**                    |             |       |
| **username**          | **str**                      |             |       |
| **night**             | [**Night**](README.md#night) |             |       |
| **exp_middle**        | **str**                      |             |       |
| **cmp_ap_auto**       | **str**                      |             |       |
| **cmp_ap_auto_dev**   | **float**                    |             |       |
| **cmp_apertures**     | **[str]**                    |             |       |
| **cmp_aperture_devs** | **[float]**                  |             |       |

[[Back to Model list]](README.md#documentation-for-models)

### Night

#### Properties
| Name                         | Type    | Description | Notes |
|------------------------------|---------|-------------|-------|
| **first_date_of_the_night**  | **str** |             |       |
| **second_date_of_the_night** | **str** |             |       |
| **ap_to_be_used**            | **str** |             |       |
| **cmp_ap_to_be_used**        | **str** |             |       |

[[Back to Model list]](README.md#documentation-for-models)

### PhotoProperties

#### Properties
| Name               | Type         | Description | Notes |
|--------------------|--------------|-------------|-------|
| **exposure_begin** | **datetime** |             |       |
| **exposure_end**   | **datetime** |             |       |

[[Back to Model list]](README.md#documentation-for-models)

### SpaceObject

#### Properties
| Name             | Type      | Description | Notes |
|------------------|-----------|-------------|-------|
| **id**           | **str**   |             |       |
| **catalog**      | **str**   |             |       |
| **name**         | **str**   |             |       |
| **right_asc**    | **str**   |             |       |
| **declination**  | **str**   |             |       |
| **magnitude**    | **float** |             |       |
| **fluxes_count** | **int**   |             |       |

[[Back to Model list]](README.md#documentation-for-models)

### SpaceObjectWithFluxes
Extends SpaceObject by fluxes.

#### Properties
| Name             | Type                         | Description                              | Notes |
|------------------|------------------------------|------------------------------------------|-------|
| **fluxes**       | [**[Flux]**](README.md#flux) | Additional field compared to SpaceObject |       |
| **id**           | **str**                      |                                          |       |
| **catalog**      | **str**                      |                                          |       |
| **name**         | **str**                      |                                          |       |
| **right_asc**    | **str**                      |                                          |       |
| **declination**  | **str**                      |                                          |       |
| **magnitude**    | **float**                    |                                          |       |
| **fluxes_count** | **int**                      |                                          |       |

[[Back to Model list]](README.md#documentation-for-models)

### User

#### Properties
| Name            | Type    | Description | Notes |
|-----------------|---------|-------------|-------|
| **username**    | **str** | Unique      |       |
| **description** | **str** |             |       |

[[Back to Model list]](README.md#documentation-for-models)















