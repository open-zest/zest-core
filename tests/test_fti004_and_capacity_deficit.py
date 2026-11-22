"""
Verification tests for FTI004 intermodal schema extensions,
offline customs fall-out routing, and the 2027 10% port capacity deficit stress test.
"""

from schemas.manifest_models import (
    ContainerManifest,
    CorridorManifest,
    CustomsChannel,
    DestinationZone,
    IntermodalHandoffFTI004,
    PreArrivalSyncTier,
    RegulatoryTokens,
)
from solvers.des.milkrun_sim import (
    StochasticMilkRunSimulator,
    execute_capacity_deficit_stress_test,
)


def test_fti004_schema_and_t5_sync_tier():
    reg = RegulatoryTokens(
        data_lead_time_hours=120.0,
        ebl_reference="DCSA-EBL-2026-0001",
        efti_gate_id="RO-EFTI-GATE-01",
        ncts_mrn="26ROCONST0000123",
    )
    assert reg.sync_tier == PreArrivalSyncTier.T_MINUS_5D
    assert reg.is_t5_cut_through_ready is True

    handoff = IntermodalHandoffFTI004(
        origin_zone_stow_block="BAY12-ZONE_F_BUD",
        quay_to_rail_cut_through=True,
        rail_undertaking_rics="2153",
        target_dry_port_unlocode="HUBUD",
        train_path_slot_id="RFC9-2026-1124-04",
        wagon_sequence_index=7,
        offline_customs_fallout=True,
    )
    container = ContainerManifest(
        container_id="MSKU9045123",
        destination_zone=DestinationZone.ZONE_F_BUD,
        regulatory=reg,
        fti004_handoff=handoff,
    )
    assert container.fti004_handoff.efti_subset_code == "FTI004"
    assert container.fti004_handoff.quay_to_rail_cut_through is True
    assert container.vgm_kg == 21800.0


def test_offline_customs_fallout_bypasses_coastal_yard():
    manifest = CorridorManifest(
        containers=[
            ContainerManifest(
                container_id="MSKU1111111",
                destination_zone=DestinationZone.ZONE_F_BUD,
                regulatory=RegulatoryTokens(
                    customs_channel=CustomsChannel.RED,
                    ncts_mrn="26RO0000099999",
                    data_lead_time_hours=120.0,
                ),
                fti004_handoff=IntermodalHandoffFTI004(
                    quay_to_rail_cut_through=True,
                    offline_customs_fallout=True,
                ),
            )
        ]
    )
    res = StochasticMilkRunSimulator(manifest=manifest, seed=42).run_simulation()
    rec = res["records"][0]
    assert rec["route_path"] == "DIRECT_TO_RAIL_T1_FALLOUT"
    assert rec["rehandles"] == 0
    assert rec["dwell_hours"] < 1.0


def test_2027_capacity_deficit_stress_test():
    res = execute_capacity_deficit_stress_test(
        capacity_deficit_pct=0.10,
        yard_utilization_pct=0.85,
        container_count=30,
    )
    assert res["legacy_mean_dwell_hours"] > 60.0
    assert res["legacy_mean_rehandles"] > 2.0
    assert res["zest_mean_dwell_hours"] < 2.0
    assert res["zest_mean_rehandles"] == 0.0
    assert res["dwell_reduction_pct"] > 95.0
