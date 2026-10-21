"""
schemas/manifest_models.py
==========================
Project ZeST: Zero-Sort Transport
Pydantic v2 Data Models for Federated eFTI / OpenManifest Specification.

Complies with:
- EU Regulation 2020/1056 (eFTI) common data set (CDS)
- SOLAS Chapter VI Regulation 2 (Verified Gross Mass - VGM)
- Union Customs Code (UCC) NCTS T1 transit bond protocols
"""

from __future__ import annotations

import re
from datetime import datetime
from enum import Enum
from typing import Annotated, Dict, List, Optional
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)


class ISOSizeTypeCode(str, Enum):
    """Standard ISO 6346 size/type codes for intermodal equipment."""
    GP_20 = "22G1"  # 20ft Standard General Purpose
    GP_40 = "42G1"  # 40ft Standard General Purpose
    HC_40 = "45G1"  # 40ft High Cube
    REEFER_40 = "45R1"  # 40ft High Cube Refrigerated
    OPEN_TOP_40 = "42U1"  # 40ft Open Top


class CustomsTransitStatus(str, Enum):
    """
    Customs transit status under the EU Union Customs Code (UCC).
    ZeST routes uncleared non-Union goods under NCTS T1 bond directly
    onto rail conveyors to prevent quay-side inspection fall-out delays.
    """
    UNION_CLEARED = "C"        # Released for free circulation
    NCTS_T1_BOND = "T1"        # Non-Union goods under in-bond rail transit
    T2_TRANSIT = "T2"          # Union goods passing non-EU territory
    CUSTOMS_HOLD = "HOLD"      # Offline rework / fall-out hold


class DestinationZoneCode(str, Enum):
    """
    Coarse-grained regional corridor delivery zones.
    Mapped 1:1 to inland dry port corridors along the TEN-T backbone.
    """
    ZONE_A_DUISBURG = "ZONE_A_DUI"
    ZONE_B_VERONA = "ZONE_B_VRN"
    ZONE_C_POZNAN = "ZONE_C_POZ"
    ZONE_D_VIENNA = "ZONE_D_VIE"
    ZONE_E_LYON = "ZONE_E_LYS"
    ZONE_F_BUDAPEST = "ZONE_F_BUD"


# Strict ISO 6346 Container Identifier: 4 capital letters + 7 digits (e.g., MSCU1234567)
ContainerID = Annotated[
    str,
    StringConstraints(
        pattern=r"^[A-Z]{4}\d{7}$",
        strip_whitespace=True,
    ),
]


class GeographicCoordinates(BaseModel):
    """WGS84 Coordinates for inland routing engines."""
    model_config = ConfigDict(frozen=True)

    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude in decimal degrees")


class InlandFinalDestination(BaseModel):
    """
    Micro-layer delivery address known at contract inception.
    Provides data required by Google Maps Routes API / local drayage.
    """
    model_config = ConfigDict(frozen=True)

    destination_id: str = Field(..., description="Unique delivery node identifier")
    postal_code: str = Field(..., min_length=2, max_length=12)
    country_code: str = Field(..., min_length=2, max_length=2, description="ISO 3166-1 alpha-2")
    coordinates: Optional[GeographicCoordinates] = None


class ContainerToken(BaseModel):
    """
    ATM Federated Trust Token for individual containerized shipments.
    Exposes zero proprietary commercial data (rates, BCO identity, shipper).
    Exposes only physical and regulatory dispatch invariants.
    """
    model_config = ConfigDict(frozen=True, extra="forbid")

    container_id: ContainerID = Field(
        ...,
        description="Standard ISO 6346 container number (4 alpha, 7 numeric)",
        examples=["MSCU7654321"],
    )
    iso_code: ISOSizeTypeCode = Field(
        default=ISOSizeTypeCode.HC_40,
        description="Standard ISO equipment dimension/type",
    )
    vgm_kg: float = Field(
        ...,
        gt=2000.0,
        le=36000.0,
        description="SOLAS Verified Gross Mass in kilograms (tare + cargo payload)",
    )
    is_hazmat: bool = Field(
        default=False,
        description="Flag indicating hazardous cargo requiring segregated bay stowage",
    )
    customs_status: CustomsTransitStatus = Field(
        default=CustomsTransitStatus.NCTS_T1_BOND,
        description="Customs status governing immediate ramp-to-rail clearance",
    )
    destination_zone: DestinationZoneCode = Field(
        ...,
        description="Target coarse delivery zone mapping to inland dry port siding",
    )
    final_destination: InlandFinalDestination = Field(
        ...,
        description="Precise inland delivery target for micro-layer drayage",
    )
    cryptographic_token: str = Field(
        ...,
        description="Single-use SHA-256 hash or eFTI bearer token proving data integrity",
    )

    @field_validator("cryptographic_token")
    @classmethod
    def validate_token_format(cls, value: str) -> str:
        if not re.match(r"^[a-fA-F0-9]{64}$", value):
            raise ValueError("cryptographic_token must be a 64-character hex SHA-256 token")
        return value.lower()


class VesselCallInfo(BaseModel):
    """Voyage header metadata anchoring the aggregate booking."""
    model_config = ConfigDict(frozen=True)

    vessel_name: str = Field(..., min_length=2, max_length=64)
    imo_number: int = Field(..., ge=1000000, le=9999999, description="7-digit IMO ship identifier")
    voyage_number: str = Field(..., min_length=1, max_length=16)
    origin_port: str = Field(..., min_length=5, max_length=5, description="UN/LOCODE of loading port (e.g. CNSHA)")
    gateway_port: str = Field(..., min_length=5, max_length=5, description="UN/LOCODE of gateway discharge port (e.g. NLRTM)")
    scheduled_berth_window: datetime = Field(..., description="Estimated Time of Arrival / Berth window")


class VesselManifest(BaseModel):
    """
    Aggregate Ship-Level Manifest.
    Represents the full contract-inception dataset (15,000–24,000 TEU aggregate)
    used for simultaneous zero-sort zone pre-stowing and corridor planning.
    """
    model_config = ConfigDict(extra="forbid")

    manifest_version: str = Field(
        default="1.0.0",
        description="Semantic version of the OpenManifest specification",
    )
    vessel_call: VesselCallInfo
    containers: List[ContainerToken] = Field(
        ...,
        min_length=1,
        description="Complete list of tokenized container payloads for the voyage",
    )

    @property
    def total_teu(self) -> float:
        """Calculates total TEUs dynamically based on ISO codes."""
        teu_weights = {
            ISOSizeTypeCode.GP_20: 1.0,
            ISOSizeTypeCode.GP_40: 2.0,
            ISOSizeTypeCode.HC_40: 2.0,
            ISOSizeTypeCode.REEFER_40: 2.0,
            ISOSizeTypeCode.OPEN_TOP_40: 2.0,
        }
        return sum(teu_weights.get(c.iso_code, 2.0) for c in self.containers)

    @property
    def total_payload_mass_tonnes(self) -> float:
        """Returns total verified gross mass in metric tonnes."""
        return sum(c.vgm_kg for c in self.containers) / 1000.0

    @model_validator(mode="after")
    def verify_unique_containers(self) -> VesselManifest:
        seen = set()
        duplicates = set()
        for container in self.containers:
            cid = container.container_id
            if cid in seen:
                duplicates.add(cid)
            seen.add(cid)
        if duplicates:
            raise ValueError(f"Duplicate container IDs discovered in manifest: {sorted(duplicates)}")
        return self

    def zone_distribution_summary(self) -> Dict[DestinationZoneCode, int]:
        """Provides container count distribution by inland corridor zone."""
        distribution: Dict[DestinationZoneCode, int] = {zone: 0 for zone in DestinationZoneCode}
        for c in self.containers:
            distribution[c.destination_zone] += 1
        return distribution
