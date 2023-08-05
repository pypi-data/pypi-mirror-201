import logging
from typing import List

from geopy import distance
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from ..models.municipality import (
    Municipality,
    MunicipalityWithDistance,
    OfflineMunicipality,
    OfflineMunicipalityWithDistance,
)


def search_close_meeting_points(
    all_points: List[Municipality],
    latitude: float,
    longitude: float,
    radius_km: int,
) -> List[MunicipalityWithDistance]:
    """
    Search the closest meeting points.
    Args:
        all_points (List[Municipality]): list of the municipality.
        latitude (float): latitude of the search.
        longitude (float): longitude of the search.
        radius_km (int): radius_km of the search.
    Returns:
        List[MunicipalityWithDistance]: The list of closest meeting point.
    """
    _logger = logging.getLogger("root")

    close_points: List[MunicipalityWithDistance] = []

    for point in all_points:
        try:
            copy_point = point.copy()
            copy_point["distance_km"] = round(
                distance.distance(
                    (latitude, longitude), (point["latitude"], point["longitude"])
                ).km,
                2,
            )
            if copy_point["distance_km"] < radius_km:
                close_points.append(copy_point)
        except Exception as geolocalisation_e:
            _logger.error(
                "Error while calculating distance from %s : %s",
                point["name"],
                geolocalisation_e,
            )
    return close_points


def search_close_offline_meeting_points(
    all_points: List[OfflineMunicipality],
    latitude: float,
    longitude: float,
    radius_km: int,
) -> List[OfflineMunicipalityWithDistance]:
    """
    Search the closest offline meeting points.
    Args:
        all_points (List[OfflineMunicipality]): list of the offline municipalities.
        latitude (float): latitude of the search.
        longitude (float): longitude of the search.
        radius_km (int): radius_km of the search.
    Raises:
        HTTPException: Raise http-400 when there is bad type of params.
    Returns:
        List[OfflineMunicipalityWithDistance]: The list of closest offline meeting points.
    """
    close_points: List[OfflineMunicipalityWithDistance] = []
    try:
        for point in all_points:
            copy_point = point.copy()
            copy_point["distance_km"] = round(
                distance.distance(
                    (latitude, longitude), (point["latitude"], point["longitude"])
                ).km,
                2,
            )
            if copy_point["distance_km"] < radius_km:
                close_points.append(copy_point)
    except Exception:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Bad type of params"
        )
    return close_points
