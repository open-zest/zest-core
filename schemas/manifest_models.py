from pydantic import BaseModel, Field, computed_field
from typing import List, Optional, Any, Union, Dict
from enum import Enum
from datetime import datetime

class CustomsTransitStatus(str, Enum):
    CLEARED = "CLEARED"
    PENDING = "PENDING"
    IN_TRANSIT = "IN_TRANSIT"
    NCTS_T1_BOND = "NCTS_T1_BOND"
    CUSTOMS_HOLD = "CUSTOMS_HOLD"

class DestinationZoneCode(str, Enum):
    ZONE_A_DUISBURG = "ZONE_A_DUISBURG"
    ZONE_B_VERONA = "ZONE_B_VERONA"
    ZONE_C_POZNAN = "ZONE_C_POZNAN"
    ZONE_D_VIENNA = "ZONE_D_VIENNA"
    ZONE_E_LYON = "ZONE_E_LYON"
    ZONE_F_BUDAPEST = "ZONE_F_BUDAPEST"

class ISOSizeTypeCode(str, Enum):
    HC_40 = "40HC"
    GP_40 = "40GP"
    GP_20 = "20GP"
    TYPE_45G1 = "45G1"
    TYPE_42G1 = "42G1"
    TYPE_22G1 = "22G1"
    TYPE_L5G1 = "L5G1"

class GeographicCoordinates(BaseModel):
    latitude: float = 0.0
    longitude: float = 0.0

class InlandFinalDestination(BaseModel):
    destination_id: str
    postal_code: str
    country_code: str
    coordinates: GeographicCoordinates

class VesselCallInfo(BaseModel):
    vessel_name: str = "ZeST Rotterdam Express"
    imo_number: int = 9811000
    voyage_number: str = "2601W"
    origin_port: Optional[str] = "CNSHA"
    gateway_port: Optional[str] = "NLRTM"
    scheduled_berth_window: Optional[datetime] = None
    origin_locode: Optional[str] = "CNSHA"
    gateway_locode: Optional[str] = "NLRTM"

class ContainerModel(BaseModel):
    container_id: str
    destination_zone: Union[DestinationZoneCode, str] = DestinationZoneCode.ZONE_A_DUISBURG
    weight_kg: float = 20000.0
    vgm_kg: float = 20000.0
    customs_status: CustomsTransitStatus = CustomsTransitStatus.CLEARED
    iso_size_type: ISOSizeTypeCode = ISOSizeTypeCode.HC_40

class ContainerToken(BaseModel):
    container_id: str
    iso_code: Optional[ISOSizeTypeCode] = ISOSizeTypeCode.HC_40
    vgm_kg: float = 20000.0
    is_hazmat: bool = False
    customs_status: CustomsTransitStatus = CustomsTransitStatus.NCTS_T1_BOND
    destination_zone: Optional[Union[DestinationZoneCode, str]] = None
    assigned_zone: Optional[DestinationZoneCode] = None
    final_destination: Optional[InlandFinalDestination] = None
    destination: Optional[InlandFinalDestination] = None
    cryptographic_token: Optional[str] = None
    token_hash: Optional[str] = None
    token_id: Optional[str] = None
    origin: Optional[str] = "NLRTM"
    weight_kg: Optional[float] = 20000.0

    @computed_field
    @property
    def teu(self) -> float:
        code = self.iso_code
        if code in (ISOSizeTypeCode.GP_20, ISOSizeTypeCode.TYPE_22G1):
            return 1.0
        return 2.0

class ZoneModel(BaseModel):
    zone_id: str
    crane_capacity: int = 2
    coordinates: Optional[GeographicCoordinates] = None

class CorridorManifest(BaseModel):
    manifest_version: str = "1.0.0"
    zones: List[ZoneModel] = Field(default_factory=list)
    containers: List[Union[ContainerToken, ContainerModel]] = Field(default_factory=list)
    tokens: List[ContainerToken] = Field(default_factory=list)
    vessel_call: Optional[VesselCallInfo] = Field(default_factory=VesselCallInfo)
    vessel_name: Optional[str] = "ZeST Rotterdam Express"
    imo_number: Optional[int] = 9811000
    voyage_number: Optional[str] = "2601W"
    origin_locode: Optional[str] = "CNSHA"
    gateway_locode: Optional[str] = "NLRTM"

    @computed_field
    @property
    def total_teu(self) -> float:
        teu_sum = 0.0
        for c in self.containers:
            iso = getattr(c, "iso_code", None) or getattr(c, "iso_size_type", None)
            if iso in (ISOSizeTypeCode.GP_20, ISOSizeTypeCode.TYPE_22G1):
                teu_sum += 1.0
            else:
                teu_sum += 2.0
        return round(teu_sum, 1)

    @computed_field
    @property
    def total_vgm_tonnes(self) -> float:
        vgm_sum = sum(getattr(c, "vgm_kg", getattr(c, "weight_kg", 20000.0)) for c in self.containers)
        return round(vgm_sum / 1000.0, 2)

    @computed_field
    @property
    def total_payload_mass_tonnes(self) -> float:
        payload_sum = 0.0
        for c in self.containers:
            gross = getattr(c, "vgm_kg", getattr(c, "weight_kg", 20000.0))
            iso = getattr(c, "iso_code", None) or getattr(c, "iso_size_type", None)
            tare = 2200.0 if iso in (ISOSizeTypeCode.GP_20, ISOSizeTypeCode.TYPE_22G1) else 3800.0
            payload_sum += max(gross - tare, 0.0)
        return round(payload_sum / 1000.0, 2)

    def zone_distribution_summary(self) -> Dict[DestinationZoneCode, int]:
        dist: Dict[DestinationZoneCode, int] = {zone: 0 for zone in DestinationZoneCode}
        for c in self.containers:
            raw_zone = getattr(c, "destination_zone", None) or getattr(c, "assigned_zone", None)
            target = None
            if isinstance(raw_zone, DestinationZoneCode):
                target = raw_zone
            elif isinstance(raw_zone, str):
                for zone in DestinationZoneCode:
                    if raw_zone in (zone.value, zone.name):
                        target = zone
                        break
            if target in dist:
                dist[target] += 1
        return dist

# Backward-compatibility aliases
Container = ContainerModel
Manifest = CorridorManifest
VesselManifest = CorridorManifest
