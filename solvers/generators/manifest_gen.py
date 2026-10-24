"""
Synthetic manifest generator for Project ZeST benchmarks.
Generates realistic cargo weights, corridor distribution, cryptographic tokens,
and eFTI regulatory data across configurable documentation filing regimes.
"""

import hashlib
import random
import uuid
from typing import List
from schemas.manifest_models import (
    ContainerManifest,
    VesselCallManifest,
    IsoContainerType,
    DestinationZone,
    CustomsChannel,
    RegulatoryTokens,
)


def generate_synthetic_manifest(
    total_containers: int = 1500,
    seed: int = 42,
    vessel_name: str = "ZeST Rotterdam Pioneer",
    vessel_imo: str = "IMO9988776",
    filing_regime: str = "HIGH_SEAS_eFTI"
) -> VesselCallManifest:
    """
    filing_regime:
      - 'HIGH_SEAS_eFTI': Settled during sea voyage; 90%+ green, pre-arrival lead time 12-96h.
      - 'LEGACY_DISCHARGE_TRIGGER': Documentation starts near berth; 60%+ lags 10h cut-off.
    """
    random.seed(seed)

    containers: List[ContainerManifest] = []
    zones = list(DestinationZone)
    zone_weights = [0.35, 0.20, 0.15, 0.12, 0.10, 0.08]

    iso_types = [
        (IsoContainerType.FORTY_HIGH_CUBE, 2.0, 3800.0, 0.65),
        (IsoContainerType.FORTY_FOOT, 2.0, 3650.0, 0.20),
        (IsoContainerType.TWENTY_FOOT, 1.0, 2200.0, 0.15),
    ]

    for i in range(total_containers):
        c_prefix = random.choice(["MSKU", "CMAU", "COSU", "HLCU", "MEDU"])
        c_num = f"{random.randint(1000000, 9999999)}"
        c_id = f"{c_prefix}{c_num}"

        iso_pick = random.choices(iso_types, weights=[x[3] for x in iso_types])[0]
        iso_type, teu, tare = iso_pick[0], iso_pick[1], iso_pick[2]

        if teu == 1.0:
            net_cargo = random.triangular(4000.0, 21800.0, 14000.0)
        else:
            net_cargo = random.triangular(8000.0, 26680.0, 18500.0)
        vgm = round(tare + net_cargo, 2)

        dest_zone = random.choices(zones, weights=zone_weights)[0]

        if filing_regime == "LEGACY_DISCHARGE_TRIGGER":
            # Reactive regime: Documentation starts when vessel is near or at berth
            reg_roll = random.random()
            if reg_roll < 0.70:
                customs = CustomsChannel.GREEN
                doc_release = random.random() < 0.60
                # Heavy cluster around berth (-18h to +8h)
                lead_time = random.uniform(-18.0, 8.0)
                mrn = f"26NL{uuid.uuid4().hex[:12].upper()}T1"
            elif reg_roll < 0.90:
                customs = CustomsChannel.YELLOW
                doc_release = False
                lead_time = random.uniform(-24.0, 4.0)
                mrn = f"26NL{uuid.uuid4().hex[:12].upper()}YEL"
            else:
                customs = CustomsChannel.RED
                doc_release = False
                lead_time = random.uniform(-48.0, -2.0)
                mrn = f"26NL{uuid.uuid4().hex[:12].upper()}RED"
        else:
            # ZeST High-Seas eFTI regime: Settled 1-4 days prior to arrival
            reg_roll = random.random()
            if reg_roll < 0.92:
                customs = CustomsChannel.GREEN
                doc_release = True
                lead_time = random.uniform(12.0, 96.0)
                mrn = f"26NL{uuid.uuid4().hex[:12].upper()}T1"
            elif reg_roll < 0.97:
                customs = CustomsChannel.YELLOW
                doc_release = random.choice([True, False])
                lead_time = random.uniform(-6.0, 10.0)
                mrn = f"26NL{uuid.uuid4().hex[:12].upper()}YEL"
            else:
                customs = CustomsChannel.RED
                doc_release = False
                lead_time = random.uniform(-48.0, -2.0)
                mrn = f"26NL{uuid.uuid4().hex[:12].upper()}RED"

        token_payload = f"{c_id}:{vgm}:{dest_zone.value}:{mrn}:{seed}:{i}".encode("utf-8")
        crypto_token = hashlib.sha256(token_payload).hexdigest()

        regulatory = RegulatoryTokens(
            ics2_status="APPROVED",
            customs_channel=customs,
            ncts_mrn=mrn,
            commercial_release=doc_release,
            data_lead_time_hours=round(lead_time, 2)
        )

        containers.append(
            ContainerManifest(
                container_id=c_id,
                iso_type=iso_type,
                teu=teu,
                tare_weight_kg=tare,
                net_cargo_weight_kg=round(net_cargo, 2),
                vgm_kg=vgm,
                destination_zone=dest_zone,
                cryptographic_token=crypto_token,
                regulatory=regulatory
            )
        )

    return VesselCallManifest(
        vessel_name=vessel_name,
        vessel_imo=vessel_imo,
        total_containers=total_containers,
        containers=containers
    )
