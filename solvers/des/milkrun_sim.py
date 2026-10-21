"""
solvers/des/milkrun_sim.py
==========================
Project ZeST: Zero-Sort Transport
Discrete-Event Simulation (SimPy) of the Macro Layer Linear Rail Conveyor.

Models:
- Direct ramp-to-rail train dispatch from maritime gateway (Rotterdam).
- Sequential inland dry port drop-offs (milk-run corridor topology).
- Deterministic 15-minute offline siding set-outs vs. traditional classification yard humping.
"""

from __future__ import annotations

import simpy
from dataclasses import dataclass
from typing import List, Dict


@dataclass(frozen=True)
class CorridorDryPort:
    name: str
    zone_code: str
    distance_km: float
    target_block_teu: int


# Reference TEN-T Rhine-Alpine / North Sea-Baltic Corridor Sequence
DEFAULT_CORRIDOR_PORTS: List[CorridorDryPort] = [
    CorridorDryPort(name="Duisburg Intermodal Terminal", zone_code="ZONE_A_DUI", distance_km=210.0, target_block_teu=32),
    CorridorDryPort(name="Verona Quadrante Europa", zone_code="ZONE_B_VRN", distance_km=1050.0, target_block_teu=28),
    CorridorDryPort(name="Poznan Franowo", zone_code="ZONE_C_POZ", distance_km=1180.0, target_block_teu=30),
]


class MilkRunCorridorSim:
    """
    Simulates the scheduled linear rail conveyor under both ZeST
    (pre-stowed sequence + siding set-outs) and Traditional
    (humping, flat switching, and terminal re-marshalling).
    """

    def __init__(
        self,
        env: simpy.Environment,
        ports: List[CorridorDryPort] = None,
        train_speed_kmh: float = 75.0,
        zest_setout_minutes: float = 15.0,
        trad_remarshall_hours: float = 8.5,
    ):
        self.env = env
        self.ports = ports or DEFAULT_CORRIDOR_PORTS
        self.train_speed_kmh = train_speed_kmh
        self.zest_setout_hours = zest_setout_minutes / 60.0
        self.trad_remarshall_hours = trad_remarshall_hours
        self.metrics: Dict[str, Dict[str, float]] = {
            "zest": {},
            "traditional": {}
        }

    def run_zest_corridor(self):
        """
        ZeST: Rear cars are set out into sidings via simple 15-minute decoupling.
        Mainline track slot is cleared immediately.
        """
        current_km = 0.0
        for port in self.ports:
            leg_distance = port.distance_km - current_km
            travel_time = leg_distance / self.train_speed_kmh
            yield self.env.timeout(travel_time)
            
            # Siding drop-off
            yield self.env.timeout(self.zest_setout_hours)
            self.metrics["zest"][port.zone_code] = self.env.now
            current_km = port.distance_km

    def run_traditional_corridor(self):
        """
        Traditional: Intermodal trains enter classification/switch yards,
        requiring extensive switching, brake tests, and crane sorting.
        """
        current_km = 0.0
        for port in self.ports:
            leg_distance = port.distance_km - current_km
            travel_time = leg_distance / self.train_speed_kmh
            yield self.env.timeout(travel_time)
            
            # Traditional intermediate yard delay
            yield self.env.timeout(self.trad_remarshall_hours)
            self.metrics["traditional"][port.zone_code] = self.env.now
            current_km = port.distance_km


def execute_corridor_benchmark() -> Dict[str, Dict[str, float]]:
    # Run ZeST Simulation
    env_zest = simpy.Environment()
    sim_zest = MilkRunCorridorSim(env_zest)
    env_zest.process(sim_zest.run_zest_corridor())
    env_zest.run()

    # Run Traditional Simulation
    env_trad = simpy.Environment()
    sim_trad = MilkRunCorridorSim(env_trad)
    env_trad.process(sim_trad.run_traditional_corridor())
    env_trad.run()

    return {
        "zest_delivery_hours": sim_zest.metrics["zest"],
        "traditional_delivery_hours": sim_trad.metrics["traditional"],
    }


if __name__ == "__main__":
    results = execute_corridor_benchmark()
    print("=" * 65)
    print("Project ZeST: Macro Corridor Rail Milk-Run Simulation Results")
    print("=" * 65)
    print(f"{'Dry Port Zone':<16} | {'ZeST Arrival (h)':<18} | {'Traditional (h)':<18} | {'Delta':<8}")
    print("-" * 65)
    for zone in results["zest_delivery_hours"]:
        z_time = results["zest_delivery_hours"][zone]
        t_time = results["traditional_delivery_hours"][zone]
        savings = t_time - z_time
        print(f"{zone:<16} | {z_time:<18.2f} | {t_time:<18.2f} | -{savings:.2f}h")
    print("=" * 65)
