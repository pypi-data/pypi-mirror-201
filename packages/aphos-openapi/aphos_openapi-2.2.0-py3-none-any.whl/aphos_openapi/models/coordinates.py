import math
from typing import Tuple as _Tuple
from typing import Union as _Union
from astropy import units as _u  # type: ignore
from astropy.coordinates import Angle as _Angle  # type: ignore
from astropy.coordinates import SkyCoord as _SkyCoord  # type: ignore


class Coordinates:
    """
    Coordinates class for working with coordinates.
    Attributes:
        rightAsc: str, right ascension in string ':' format, unit = hour
        declination: str, declination in string ':' format, unit = degree
        radius: float, radius, unit = degree
    """

    def __init__(self, coordinates: _Union[str, _SkyCoord], radius: float,
                 default_unit: str = 'h', radius_unit: str = 'd') -> None:
        """
        Constructor for Coordinates object.

        Args:
            coordinates: coordinates - string in correct format or astropy SkyCoord
            radius: float number for angle radius
            default_unit: default unit for right ascension (in case of string with no unit), 'h' for hours,
                'd' for degrees [optional]
            radius_unit: default unit for radius ('m' for minutes, 's' for seconds, otherwise degrees)
                [optional]
        """
        self.rightAsc, self.declination = parse_coordinates(coordinates, default_unit)
        self.radius = parse_radius(radius, radius_unit)

    def __str__(self) -> str:
        # return _pprint.pformat(self.__dict__)
        return '{{"rightAsc": "{}",  "declination": "{}","radius": {}}}' \
            .format(self.rightAsc, self.declination, self.radius)

    def __eq__(self, other: object) -> bool:
        """
        Equality method for objects.

        Returns true if Coordinates objects are very similar.
        (RA on 0.01 sec diff, declination on 0.01 sec diff, radius - 0.001 sec diff)

        Args:
            other: object

        Returns: if the objects are equal

        """
        if not isinstance(other, Coordinates):
            return False
        if self.rightAsc[:11] != other.rightAsc[:11] or self.declination[:11] != other.declination[:11]:
            return False
        if not math.isclose(self.radius, other.radius, abs_tol=0.001):
            return False
        return True



def parse_coordinates(coordinates: _Union[str, _SkyCoord], default_unit: str = 'h') -> _Tuple[str, str]:
    """
    Parse coordinates.

    Args:
        coordinates: string in correct format or astropy SkyCoord
        default_unit: default unit for non-unit strings [optional]

    Returns: tuple of formatted right ascension and declination.

    """
    if type(coordinates) == _SkyCoord:
        sky_coord = coordinates
    else:
        coordinates.strip()
        sign = '+'
        if '-' in coordinates:
            sign = '-'
        if coordinates.count(' ') > 1 or coordinates.count(':') > 1:
            coord_arr = coordinates.split(sign)
            coord_arr[0] = coord_arr[0].strip() + default_unit
            coord_arr[1] = sign + coord_arr[1].strip() + 'd'
            coordinates = coord_arr[0] + coord_arr[1]
        sky_coord = _SkyCoord(coordinates)
    return sky_coord.ra.to_string(unit=_u.hour, sep=':', precision=3), \
        sky_coord.dec.to_string(unit=_u.degree, sep=':')


def parse_radius(radius: float, radius_unit: str = 'd') -> float:
    """
    Parse radius.

    Args:
        radius: radius (angle)
        radius_unit: unit of the angle

    Returns: float in degree unit.

    """
    if radius_unit not in "ms" or len(radius_unit) > 1:
        return radius
    return _Angle(str(radius) + radius_unit).degree
