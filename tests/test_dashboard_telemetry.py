"""
Unit tests for Project ZeST SDN Port-Rail Transfer Telemetry Server
and Partial eFTI / Pre-Cleared Adoption (alpha_eFTI in [0%, 100%]) math.
"""

from tools.dashboard.server import (
    build_telemetry_snapshot,
    compute_queuing_compounding,
    generate_live_packets,
)


def test_full_efti_adoption_100_pct():
    snap = build_telemetry_snapshot(tick=0, adoption_pct=100.0)
    zest = snap["sdn_architecture"]["data_plane_comparison"]["zest"]
    q = snap["sdn_architecture"]["maritime_queue_compounding"]

    assert snap["adoption_pct"] == 100.0
    assert zest["mean_terminal_dwell_h"] == 4.43
    assert zest["quayside_transfer_h"] == 0.31
    assert zest["yard_rehandles_per_box"] == 0.0
    assert zest["gross_vessel_berth_h"] == 38.5
    assert zest["rail_breakeven_km"] == 195
    assert q["queue_collapse_pct"] == 71.1
    assert all(p["is_pre_cleared"] for p in snap["live_packets"])


def test_legacy_baseline_0_pct_adoption():
    snap = build_telemetry_snapshot(tick=0, adoption_pct=0.0)
    zest = snap["sdn_architecture"]["data_plane_comparison"]["zest"]
    q = snap["sdn_architecture"]["maritime_queue_compounding"]

    assert snap["adoption_pct"] == 0.0
    assert zest["mean_terminal_dwell_h"] == 57.39
    assert zest["yard_rehandles_per_box"] == 1.65
    assert zest["gross_vessel_berth_h"] == 54.0
    assert zest["rail_breakeven_km"] == 540
    assert q["queue_collapse_pct"] == 0.0
    assert not any(p["is_pre_cleared"] for p in snap["live_packets"])


def test_partial_efti_hybrid_50_pct_nonlinear_queue_collapse():
    q50 = compute_queuing_compounding(queue_ships=6, max_berth_hours_saved=15.5, adoption_pct=50.0)
    # At 50% adoption, rho drops from 0.86 to 0.75 -> Pollaczek-Khinchine queue collapses > 45%
    assert q50["rho_zest"] == 0.75
    assert q50["queue_collapse_pct"] > 45.0
    assert q50["berth_hours_shaved_per_call"] == 7.75

    packets_50 = generate_live_packets(tick=1, adoption_pct=50.0)
    cleared_count = sum(1 for p in packets_50 if p["is_pre_cleared"])
    assert cleared_count == 6
