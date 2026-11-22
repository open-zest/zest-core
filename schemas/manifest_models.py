"""
Data models for Project ZeST synthetic manifests and operational telemetry.
Aligned with eFTI Common Data Set (Regulation (EU) 2020/1056 & (EU) 2024/2024),
FTI004 intermodal handoff extensions, DCSA 3.0 eBL, and DTLF specifications.
"""

from collections import Counter
from enum import Enum
from typing import Optional, List, Dict, Union, Any
from pydantic import BaseModel, Field, model_validator


class IsoContainerType(str, Enum):
    TWENTY_FOOT = "20GP"
    FORTY_FOOT = "40GP"
    FORTY_HIGH_CUBE = "40HC"
    FORTY_FIVE_HIGH_CUBE = "45HC"


class DestinationZone(str, Enum):
    ZONE_A_DUI = "ZONE_A_DUI"   # Duisburg DIT
    ZONE_B_VRN = "ZONE_B_VRN"   # Verona Quadrante Europa
    ZONE_C_POZ = "ZONE_C_POZ"   # Poznan Franowo
    ZONE_D_VIE = "ZONE_D_VIE"   # Vienna Freudenau
    ZONE_E_LYS = "ZONE_E_LYS"   # Lyon Saint-Exupery
    ZONE_F_BUD = "ZONE_F_BUD"   # Budapest BILK


# Backward-compatible alias for existing test suites
DestinationZoneCode = DestinationZone


class CustomsChannel(str, Enum):
    GREEN = "GREEN"    # Automated release / Onward transit authorized
    YELLOW = "YELLOW"  # Documentary check hold
    RED = "RED"        # Non-intrusive scan or physical turn-out


class PreArrivalSyncTier(str, Enum):
    T_MINUS_14D = "T-14D"          # Origin inception lock (>= 336h pre-berth)
    T_MINUS_5D = "T-5D"            # Regional cut-through lock (>= 120h pre-berth)
    T_MINUS_24H = "T-24H"          # Short-sea / late pre-advise (>= 24h pre-berth)
    POST_BERTH_LAG = "POST_BERTH"  # Legacy reactive EDI (< 24h or post-berth)


class RegulatoryTokens(BaseModel):
    ics2_status: str = Field(default="APPROVED", description="ICS2 Safety and Security filing status")
    customs_channel: CustomsChannel = Field(default=CustomsChannel.GREEN, description="Automated customs routing decision")
    ncts_mrn: Optional[str] = Field(default=None, description="T1 Transit Master Reference Number")
    ebl_reference: Optional[str] = Field(default=None, description="DCSA 3.0 Electronic Bill of Lading reference")
    efti_gate_id: Optional[str] = Field(default=None, description="Member State eFTI Gate identifier (EU 2020/1056)")
    commercial_release: bool = Field(default=True, description="Bill of lading surrendered & freight charges cleared")
    data_lead_time_hours: float = Field(
        default=48.0,
        description="Hours prior to berth that the complete eFTI data token was verified in Portbase/Gate (negative means lagged)"
    )

    @property
    def sync_tier(self) -> PreArrivalSyncTier:
        if self.data_lead_time_hours >= 336.0:
            return PreArrivalSyncTier.T_MINUS_14D
        if self.data_lead_time_hours >= 120.0:
            return PreArrivalSyncTier.T_MINUS_5D
        if self.data_lead_time_hours >= 24.0:
            return PreArrivalSyncTier.T_MINUS_24H
        return PreArrivalSyncTier.POST_BERTH_LAG

    @property
    def is_t5_cut_through_ready(self) -> bool:
        """True when eFTI token & commercial release clear at least T-5 days (120h) prior to berth."""
        return (
            self.data_lead_time_hours >= 120.0
            and self.commercial_release
            and self.ics2_status == "APPROVED"
        )


class IntermodalHandoffFTI004(BaseModel):
    """FTI004 intermodal sea-to-rail handoff extension fields (DG MOVE / DTLF annex)."""
    efti_subset_code: str = Field(default="FTI004", description="eFTI regulatory data subset identifier")
    origin_zone_stow_block: Optional[str] = Field(
        default=None,
        description="Coarse origin stowage bay/block mapped to inland rail corridor (e.g. BAY14-ZONE_F_BUD)"
    )
    quay_to_rail_cut_through: bool = Field(
        default=False,
        description="Authorizes direct STS-to-wagon zero-sort transfer bypassing coastal stack yard"
    )
    rail_undertaking_rics: Optional[str] = Field(
        default=None,
        description="4-digit UIC/RICS rail undertaking identifier"
    )
    target_dry_port_unlocode: Optional[str] = Field(
        default=None,
        description="UN/LOCODE of destination inland dry port (e.g. HUBUD, ATWIE, ROBUH)"
    )
    train_path_slot_id: Optional[str] = Field(
        default=None,
        description="Pre-allocated TEN-T Rail Freight Corridor train path slot ID"
    )
    wagon_sequence_index: Optional[int] = Field(
        default=None,
        ge=1,
        description="Target wagon slot index for deterministic siding drop"
    )
    offline_customs_fallout: bool = Field(
        default=False,
        description="Routes YELLOW/RED channel units under T1 bond to inland dry-port inspection bay"
    )


class ContainerManifest(BaseModel):
    container_id: str = Field(..., description="Unique BIC container identifier (e.g. MSKU1234567)")
    iso_type: IsoContainerType = Field(default=IsoContainerType.FORTY_HIGH_CUBE)
    teu: float = Field(default=2.0)
    tare_weight_kg: float = Field(default=3800.0)
    net_cargo_weight_kg: float = Field(default=18000.0, ge=0)
    weight_kg: Optional[float] = Field(default=None, description="Total container mass (alias for vgm)")
    vgm_kg: Optional[float] = Field(default=None, description="Verified Gross Mass (tare + net)")
    destination_zone: DestinationZone = Field(..., description="Macro-corridor destination zone")
    cryptographic_token: str = Field(default="", description="SHA-256 consignment tamper-proof token")
    imdg_code: Optional[str] = Field(default=None, description="IMDG hazard class if dangerous cargo")
    regulatory: RegulatoryTokens = Field(default_factory=RegulatoryTokens, description="eFTI data twin & customs clearance tokens")
    fti004_handoff: IntermodalHandoffFTI004 = Field(
        default_factory=IntermodalHandoffFTI004,
        description="FTI004 intermodal sea-to-rail synchronization metadata"
    )

    @model_validator(mode="before")
    @classmethod
    def harmonize_weights(cls, data: Any) -> Any:
        if isinstance(data, dict):
            w = data.get("weight_kg")
            v = data.get("vgm_kg")
            if w is not None and v is None:
                data["vgm_kg"] = float(w)
            elif v is not None and w is None:
                data["weight_kg"] = float(v)
        return data

    @model_validator(mode="after")
    def compute_vgm_if_missing(self) -> "ContainerManifest":
        if self.vgm_kg is None:
            self.vgm_kg = round(self.tare_weight_kg + self.net_cargo_weight_kg, 2)
        if self.weight_kg is None:
            self.weight_kg = self.vgm_kg
        return self


class VesselCallManifest(BaseModel):
    vessel_name: str
    vessel_imo: str
    port_of_discharge: str = "NL-RTM"
    vessel_class_teu: Optional[int] = Field(
        default=None,
        description="Nominal vessel capacity in TEU (e.g. 13500 regional Suez string vs 24000 North Sea ULCV)"
    )
    scheduled_berth_hours: float = 0.0
    total_containers: int
    containers: List[ContainerManifest]

    @property
    def total_teu(self) -> float:
        return sum(c.teu for c in self.containers)

    @property
    def total_vgm_tonnes(self) -> float:
        return sum(c.vgm_kg for c in self.containers if c.vgm_kg is not None) / 1000.0

    @property
    def total_payload_mass_tonnes(self) -> float:
        return sum(c.net_cargo_weight_kg for c in self.containers) / 1000.0

    @property
    def total_net_cargo_tonnes(self) -> float:
        return self.total_payload_mass_tonnes

    def zone_distribution_summary(self) -> Dict[str, int]:
        counts = Counter(c.destination_zone.value for c in self.containers)
        return dict(counts)


# Backward-compatible model aliases
VesselManifest = VesselCallManifest
ContainerModel = ContainerManifest


class ZoneModel(BaseModel):
    zone_id: Optional[DestinationZone] = None
    zone_code: Optional[DestinationZone] = None
    crane_capacity: int = 1
    name: str = ""
    rail_terminal_code: str = ""

    @model_validator(mode="before")
    @classmethod
    def harmonize_zone_identifiers(cls, data: Any) -> Any:
        if isinstance(data, dict):
            z_id = data.get("zone_id")
            z_code = data.get("zone_code")
            if z_id and not z_code:
                data["zone_code"] = z_id
            elif z_code and not z_id:
                data["zone_id"] = z_code
        return data


class CorridorManifest(BaseModel):
    manifest_id: str = "CORRIDOR-MANIFEST-001"
    vessel_manifest: Optional[VesselCallManifest] = None
    zones: List[ZoneModel] = Field(default_factory=list)
    containers: List[ContainerManifest] = Field(default_factory=list)
    origin_port: str = "NL-RTM"
    target_corridor: str = "RFC_NORTH_SEA_MED"

    @model_validator(mode="after")
    def synthesize_vessel_if_missing(self) -> "CorridorManifest":
        if self.vessel_manifest is None and self.containers:
            self.vessel_manifest = VesselCallManifest(
                vessel_name="Corridor Feeder",
                vessel_imo="IMO9999999",
                total_containers=len(self.containers),
                containers=self.containers
            )
        return self
