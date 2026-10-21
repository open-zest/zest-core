"""
tests/test_corridor.py
======================
Regression tests for Macro Layer Linear Rail Conveyor (Milk-Run Simulator).
"""

import pytest
from solvers.des.milkrun_sim import execute_corridor_benchmark, DEFAULT_CORRIDOR_PORTS


def test_corridor_benchmark_execution():
    results = execute_corridor_benchmark()
    
    assert "zest_delivery_hours" in results
    assert "traditional_delivery_hours" in results
    
    zest = results["zest_delivery_hours"]
    trad = results["traditional_delivery_hours"]
    
    # Verify all configured dry ports exist in output
    for port in DEFAULT_CORRIDOR_PORTS:
        assert port.zone_code in zest
        assert port.zone_code in trad
        
        # ZeST must strictly outperform traditional re-marshalling
        assert zest[port.zone_code] < trad[port.zone_code]


def test_corridor_siding_setout_dwell_advantage():
    results = execute_corridor_benchmark()
    zest = results["zest_delivery_hours"]
    trad = results["traditional_delivery_hours"]
    
    # Duisburg (first drop) should reflect elimination of intermediate re-marshalling
    dui_savings = trad["ZONE_A_DUI"] - zest["ZONE_A_DUI"]
    assert dui_savings >= 8.0  # Slashes over 8 hours on leg 1

    # Compounding latency advantage down the corridor
    poz_savings = trad["ZONE_C_POZ"] - zest["ZONE_C_POZ"]
    assert poz_savings > dui_savings
    assert poz_savings >= 24.0  # Over 24 hours saved at corridor terminus
