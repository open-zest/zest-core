import pytest
from solvers.des.milkrun_sim import StochasticMilkRunSimulator
from schemas.manifest_models import CorridorManifest, ZoneModel, ContainerModel

def test_stochastic_milkrun_simulation():
    zone = ZoneModel(zone_id="ZONE_A_DUI", crane_capacity=2)
    manifest = CorridorManifest(
        zones=[zone],
        containers=[
            ContainerModel(container_id=f"CNT-{i}", destination_zone="ZONE_A_DUI", weight_kg=20000.0)
            for i in range(10)
        ]
    )
    simulator = StochasticMilkRunSimulator(manifest, random_seed=42)
    metrics = simulator.run_simulation(duration=72.0)
    
    assert len(metrics["dwell_times"]) == 10
    assert len(metrics["queue_delays"]) == 10
    assert all(dt >= 0 for dt in metrics["dwell_times"])
