from typing import List, Optional

from pydantic import BaseModel

from ..models.available_time_slot import AvailableTimeSlot


class Municipality(BaseModel):
    id: str
    name: str
    longitude: float
    latitude: float
    _internal_id: str
    public_entry_address: str
    zip_code: str
    city_name: str
    decoded_city_name: Optional[str]
    website: Optional[str]
    city_logo: Optional[str]
    _editor_name: Optional[str]

    class Config:
        underscore_attrs_are_private = True


class MunicipalityWithDistance(Municipality):
    distance_km: float


class MunicipalityWithSlots(MunicipalityWithDistance):
    available_slots: List[AvailableTimeSlot]


class OfflineMunicipality(BaseModel):
    id: str
    name: str
    longitude: float
    latitude: float
    public_entry_address: str
    zip_code: str
    city_name: str
    phone_number: Optional[str]
    decoded_city_name: Optional[str]
    website: Optional[str]
    city_logo: Optional[str]


class OfflineMunicipalityWithDistance(OfflineMunicipality):
    distance_km: float
