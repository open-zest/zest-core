"""
Unit and regression tests for Project ZeST Core Engine.
Validates DES throughput gains and ZB-CSPP stability heuristics.
"""

import pytest
import simpy
from solvers.des.dwell_sim import execute_comparison
from solvers.zestow.zone_stow import ZoneStowageOptimizer


def test_des_dwell_and_rehandles():
    """Verify ZeST achieves <12hr dwell and exactly 0 re-handles."""
    summary = execute_comparison(sample_size=300)
    
    zest_row = summary[summary["mode"] == "zest"].iloc[0]
    trad_row = summary[summary["mode"] == "traditional"].iloc[0]

    # Validate core ZeST operational constraints
    assert zest_row["mean_rehandles"] == 0.0, "ZeST must produce zero yard crane re-handles"
    assert zest_row["mean_dwell_hrs"] < 12.0, f"Expected ZeST mean dwell < 12h, got {zest_row['mean_dwell_hrs']}"
    assert zest_row["p95_dwell_hrs"] < 24.0, f"Expected ZeST P95 dwell < 24h, got {zest_row['p95_dwell_hrs']}"

    # Verify structural improvement over baseline
    assert trad_row["mean_dwell_hrs"] > zest_row["mean_dwell_hrs"] * 4.0
    assert trad_row["mean_rehandles"] > 1.0


def test_zone_stowage_stability():
    """Verify heavier containers are stacked into lower tiers (GM >= 0.15m heuristic)."""
    optimizer = ZoneStowageOptimizer(num_bays=6, max_tier=4)

    # Synthetic sample of 12 containers across zones with varying SOLAS VGM
    manifest_sample = [
        {
            "token_id": f"token-{i}",
            "transport_equipment": {"container_id": f"ZSTU{i:07d}", "vgm_kg": 5000 + (i * 2200)},
            "zest_corridor_routing": {"destination_zone_code": f"ZONE_{(i % 3) + 1}"}
        }
        for i in range(12)
    ]

    stowage_plan = optimizer.allocate_manifest(manifest_sample)
    assert optimizer.verify_stability(stowage_plan), "Vertical stability check failed (heavier containers must be lower)"
