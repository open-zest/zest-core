"""
solvers/generators/manifest_gen.py
==================================
Project ZeST: Zero-Sort Transport
Synthetic High-Volume Manifest Generator (Pydantic v2).

Generates realistic 15,000–24,000 TEU aggregate vessel manifests matching
schemas/manifest_models.py to stress-test stowage solvers and discrete-event models.
"""

from __future__ import annotations

import hashlib
import os
import random
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List

# Ensure repository root is in sys.path for direct execution
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from schemas.manifest_models import (
    ContainerToken,
    CustomsTransitStatus,
    DestinationZoneCode,
    GeographicCoordinates,
    InlandFinalDestination,
    ISOSizeTypeCode,
    VesselCallInfo,
    VesselManifest,
)

ZONE_COORDINATE_CENTROIDS = {
    DestinationZoneCode.ZONE_A_DUISBURG: GeographicCoordinates(latitude=51.4508, longitude=6.7623),
    DestinationZoneCode.ZONE_B_VERONA: GeographicCoordinates(latitude=45.3888, longitude=10.9577),
    DestinationZoneCode.ZONE_C_POZNAN: GeographicCoordinates(latitude=52.3683, longitude=16.9930),
    DestinationZoneCode.ZONE_D_VIENNA: GeographicCoordinates(latitude=48.1633, longitude=16.4719),
    DestinationZoneCode.ZONE_E_LYON: GeographicCoordinates(latitude=45.7196, longitude=4.8972),
    DestinationZoneCode.ZONE_F_BUDAPEST: GeographicCoordinates(latitude=47.4110, longitude=19.0620),
}

ZONE_COUNTRY_CODES = {
    DestinationZoneCode.ZONE_A_DUISBURG: "DE",
    DestinationZoneCode.ZONE_B_VERONA: "IT",
    DestinationZoneCode.ZONE_C_POZNAN: "PL",
    DestinationZoneCode.ZONE_D_VIENNA: "AT",
    DestinationZoneCode.ZONE_E_LYON: "FR",
    DestinationZoneCode.ZONE_F_BUDAPEST: "HU",
}


def generate_synthetic_manifest(
    total_containers: int = 1000,
    vessel_name: str = "ZeST Rotterdam Express",
    imo_number: int = 9811000,
    voyage_number: str = "2601W",
    origin_locode: str = "CNSHA",
    gateway_locode: str = "NLRTM",
    seed: int = 42,
) -> VesselManifest:
    """
    Generates a deterministic, schema-compliant synthetic manifest.
    """
    random.seed(seed)
    containers: List[ContainerToken] = []
    zones = list(DestinationZoneCode)

    for i in range(total_containers):
        container_id = f"ZSTU{i:07d}"
        iso_code = random.choices(
            [ISOSizeTypeCode.HC_40, ISOSizeTypeCode.GP_40, ISOSizeTypeCode.GP_20],
            weights=[0.70, 0.20, 0.10],
            k=1,
        )[0]

        # Realistic container gross mass: tare (3,800 kg) + cargo (8,000 to 26,000 kg)
        vgm_kg = round(random.uniform(11800.0, 29800.0), 1)
        is_hazmat = random.random() < 0.04
        customs_status = (
            CustomsTransitStatus.CUSTOMS_HOLD
            if random.random() < 0.02
            else CustomsTransitStatus.NCTS_T1_BOND
        )
        assigned_zone = random.choice(zones)
        centroid = ZONE_COORDINATE_CENTROIDS[assigned_zone]
        country_code = ZONE_COUNTRY_CODES[assigned_zone]

        token_hash = hashlib.sha256(
            f"{container_id}:{vgm_kg}:{assigned_zone.value}:{i}".encode()
        ).hexdigest()

        destination = InlandFinalDestination(
            destination_id=f"DEST-{assigned_zone.name[-3:]}-{i:04d}",
            postal_code=f"{random.randint(10000, 99999)}",
            country_code=country_code,
            coordinates=centroid,
        )

        token = ContainerToken(
            container_id=container_id,
            iso_code=iso_code,
            vgm_kg=vgm_kg,
            is_hazmat=is_hazmat,
            customs_status=customs_status,
            destination_zone=assigned_zone,
            final_destination=destination,
            cryptographic_token=token_hash,
        )
        containers.append(token)

    vessel_call = VesselCallInfo(
        vessel_name=vessel_name,
        imo_number=imo_number,
        voyage_number=voyage_number,
        origin_port=origin_locode,
        gateway_port=gateway_locode,
        scheduled_berth_window=datetime(2026, 11, 10, 6, 0, tzinfo=timezone.utc),
    )

    return VesselManifest(
        manifest_version="1.0.0",
        vessel_call=vessel_call,
        containers=containers,
    )


if __name__ == "__main__":
    count = 1500
    manifest = generate_synthetic_manifest(total_containers=count)
    print("=" * 65)
    print(f"Generated Synthetic Manifest: {manifest.vessel_call.vessel_name}")
    print("=" * 65)
    print(f"Total Containers : {len(manifest.containers)}")
    print(f"Total TEU        : {manifest.total_teu:.1f}")
    print(f"Payload Mass     : {manifest.total_payload_mass_tonnes:,.2f} metric tonnes")
    print("\nZone Distribution:")
    for zone, qty in manifest.zone_distribution_summary().items():
        print(f"  - {zone.value:<14}: {qty:>4} containers")
    print("=" * 65)
