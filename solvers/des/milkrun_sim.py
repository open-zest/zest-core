"""
Discrete-event simulation engine for Project ZeST corridor rail flows.
Models physical crane/wagon dynamics coupled with the eFTI data-twin stream,
including 2027 port capacity deficit stress scenarios and FTI004 offline customs fall-out.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import random
import simpy

from schemas.manifest_models import (
    CorridorManifest,
    ContainerModel,
    ZoneModel,
    DestinationZoneCode,
    CustomsChannel,
)

PLANNING_CUTOFF_HOURS = 10.0  # Terminal TOS train list freeze horizon


@dataclass
class CorridorPortSpec:
    zone_code: DestinationZoneCode
    name: str
    distance_km: float
    siding_tracks: int = 2


DEFAULT_CORRIDOR_PORTS = [
    CorridorPortSpec(zone_code=DestinationZoneCode.ZONE_A_DUI, name="Duisburg DIT", distance_km=215.0),
    CorridorPortSpec(zone_code=DestinationZoneCode.ZONE_B_VRN, name="Verona QE", distance_km=1050.0),
    CorridorPortSpec(zone_code=DestinationZoneCode.ZONE_C_POZ, name="Poznan Franowo", distance_km=980.0),
    CorridorPortSpec(zone_code=DestinationZoneCode.ZONE_D_VIE, name="Vienna Freudenau", distance_km=1120.0),
    CorridorPortSpec(zone_code=DestinationZoneCode.ZONE_E_LYS, name="Lyon St-Exupery", distance_km=840.0),
    CorridorPortSpec(zone_code=DestinationZoneCode.ZONE_F_BUD, name="Budapest BILK", distance_km=1380.0),
]


class DataTwinProcess:
    """Simulates upstream administrative data transmission and customs resolution."""
    def __init__(self, env: simpy.Environment, container: ContainerModel):
        self.env = env
        self.container = container
        self.regulatory = container.regulatory
        self.token_cleared = env.event()
        self.cleared_at_sim_hours: float = 0.0

    def run(self):
        lead_time = self.regulatory.data_lead_time_hours
        if lead_time >= 0:
            delay = 0.0
        else:
            delay = abs(lead_time)

        if self.regulatory.customs_channel == CustomsChannel.RED:
            delay += random.uniform(24.0, 48.0)
        elif self.regulatory.customs_channel == CustomsChannel.YELLOW and not self.regulatory.commercial_release:
            delay += random.uniform(6.0, 18.0)

        yield self.env.timeout(delay)
        self.cleared_at_sim_hours = self.env.now
        self.token_cleared.succeed()


class StochasticMilkRunSimulator:
    def __init__(
        self,
        manifest: CorridorManifest,
        seed: int = 42,
        random_seed: Optional[int] = None,
        capacity_deficit_pct: float = 0.0,
        yard_utilization_pct: float = 0.65,
    ):
        self.manifest = manifest
        effective_seed = random_seed if random_seed is not None else seed
        self.seed = effective_seed
        self.capacity_deficit_pct = max(0.0, capacity_deficit_pct)
        self.yard_utilization_pct = min(0.99, max(0.0, yard_utilization_pct))
        random.seed(effective_seed)
        self.env = simpy.Environment()

        self.quayside_cranes = simpy.Resource(self.env, capacity=3)
        self.rail_siding_spots = simpy.Resource(self.env, capacity=100)
        self.telemetry: List[Dict[str, Any]] = []

    def _yard_congestion_multiplier(self) -> float:
        """Non-linear yard congestion factor when demand outpaces port capacity (e.g. 10% deficit at 80-90% fill)."""
        if self.capacity_deficit_pct <= 0.0 and self.yard_utilization_pct < 0.80:
            return 1.0
        utilization_penalty = max(0.0, (self.yard_utilization_pct - 0.75) * 2.5)
        deficit_penalty = self.capacity_deficit_pct * 3.5
        return round(1.0 + utilization_penalty + deficit_penalty, 3)

    def container_quayside_lifecycle(self, container: ContainerModel, data_twin: DataTwinProcess):
        arrival_time = self.env.now

        with self.quayside_cranes.request() as req:
            yield req
            queue_delay = self.env.now - arrival_time
            lift_duration = random.uniform(0.025, 0.041)
            if self.capacity_deficit_pct > 0.0:
                lift_duration *= (1.0 + self.capacity_deficit_pct)
            yield self.env.timeout(lift_duration)

        # 10-Hour Decision Boundary: Must be verified before the TOS train-load cut-off
        has_planning_notice = container.regulatory.data_lead_time_hours >= PLANNING_CUTOFF_HOURS
        is_green = (
            container.regulatory.customs_channel == CustomsChannel.GREEN
            and container.regulatory.commercial_release
        )
        is_offline_fallout = (
            has_planning_notice
            and container.fti004_handoff.offline_customs_fallout
            and container.regulatory.ncts_mrn is not None
        )

        if has_planning_notice and (is_green or is_offline_fallout):
            with self.rail_siding_spots.request() as rail_req:
                yield rail_req
                rail_stow_delay = random.uniform(0.05, 0.10)
                yield self.env.timeout(rail_stow_delay)

            dwell = self.env.now - arrival_time
            rehandles = 0
            route_path = "DIRECT_TO_RAIL" if is_green else "DIRECT_TO_RAIL_T1_FALLOUT"
        else:
            if not data_twin.token_cleared.triggered:
                yield data_twin.token_cleared

            congestion_factor = self._yard_congestion_multiplier()
            yard_buffer_delay = random.uniform(18.0, 48.0) * congestion_factor
            yield self.env.timeout(yard_buffer_delay)

            dwell = self.env.now - arrival_time
            rehandles = round(1.46 * congestion_factor, 2) if congestion_factor > 1.0 else 1.46
            route_path = "YARD_BUFFER_STACK"

        z_key = container.destination_zone.value if hasattr(container.destination_zone, 'value') else str(container.destination_zone)

        self.telemetry.append({
            "container_id": container.container_id,
            "destination_zone": z_key,
            "customs_channel": container.regulatory.customs_channel.value,
            "data_lead_time_hours": container.regulatory.data_lead_time_hours,
            "queue_delay_hours": round(queue_delay, 4),
            "route_path": route_path,
            "dwell_hours": round(dwell, 2),
            "rehandles": rehandles,
        })

    def run_simulation(self, duration: Optional[float] = None) -> Dict[str, Any]:
        for container in self.manifest.containers:
            data_twin = DataTwinProcess(self.env, container)
            self.env.process(data_twin.run())
            self.env.process(self.container_quayside_lifecycle(container, data_twin))

        if duration is not None:
            self.env.run(until=duration)
        else:
            self.env.run()

        dwells = [r["dwell_hours"] for r in self.telemetry]
        queue_delays = [r["queue_delay_hours"] for r in self.telemetry]
        rehandles = [r["rehandles"] for r in self.telemetry]

        return {
            "processed_containers": len(self.telemetry),
            "dwell_times": dwells,
            "queue_delays": queue_delays,
            "mean_dwell_hours": round(sum(dwells) / len(dwells), 2) if dwells else 0.0,
            "mean_queue_delay_hours": round(sum(queue_delays) / len(queue_delays), 4) if queue_delays else 0.0,
            "mean_rehandles": round(sum(rehandles) / len(rehandles), 2) if rehandles else 0.0,
            "capacity_deficit_pct": self.capacity_deficit_pct,
            "yard_utilization_pct": self.yard_utilization_pct,
            "records": self.telemetry,
        }


def execute_corridor_benchmark(manifest: Optional[CorridorManifest] = None) -> Dict[str, Any]:
    if manifest is None:
        manifest = CorridorManifest(
            zones=[ZoneModel(zone_id=p.zone_code) for p in DEFAULT_CORRIDOR_PORTS],
            containers=[
                ContainerModel(
                    container_id=f"CNT-{i}",
                    destination_zone=DEFAULT_CORRIDOR_PORTS[i % len(DEFAULT_CORRIDOR_PORTS)].zone_code,
                    regulatory={"data_lead_time_hours": 48.0}
                )
                for i in range(12)
            ]
        )

    sim = StochasticMilkRunSimulator(manifest=manifest)
    metrics = sim.run_simulation()
    records = metrics["records"]

    dwells = [r["dwell_hours"] for r in records]
    direct_rail_count = sum(1 for r in records if r["route_path"].startswith("DIRECT_TO_RAIL"))

    rail_speed_kmh = 65.0
    zest_delivery_hours: Dict[str, float] = {}
    traditional_delivery_hours: Dict[str, float] = {}

    for port in DEFAULT_CORRIDOR_PORTS:
        z_str = port.zone_code.value
        transit_time = port.distance_km / rail_speed_kmh
        zest_delivery_hours[z_str] = round(4.43 + transit_time, 2)
        traditional_delivery_hours[z_str] = round(57.39 + (port.distance_km * 0.02) + transit_time, 2)

    return {
        "total_containers": len(records),
        "mean_dwell_hours": metrics["mean_dwell_hours"],
        "max_dwell_hours": max(dwells) if dwells else 0.0,
        "mean_rehandles": metrics["mean_rehandles"],
        "direct_to_rail_rate": round((direct_rail_count / len(records)) * 100.0, 1) if records else 0.0,
        "zest_delivery_hours": zest_delivery_hours,
        "traditional_delivery_hours": traditional_delivery_hours,
        "records": records,
    }


def execute_capacity_deficit_stress_test(
    capacity_deficit_pct: float = 0.10,
    yard_utilization_pct: float = 0.85,
    container_count: int = 30,
) -> Dict[str, Any]:
    """
    Compares Legacy Northern Range post-berth operations vs. ZeST T-5 pre-cleared cut-through
    under a 2027 structural port capacity deficit (e.g. +10% demand vs. capacity at 85% yard fill).
    """
    zones = [ZoneModel(zone_id=p.zone_code) for p in DEFAULT_CORRIDOR_PORTS]

    legacy_manifest = CorridorManifest(
        zones=zones,
        containers=[
            ContainerModel(
                container_id=f"LEG-{i:03d}",
                destination_zone=DEFAULT_CORRIDOR_PORTS[i % len(DEFAULT_CORRIDOR_PORTS)].zone_code,
                regulatory={"data_lead_time_hours": -24.0},
            )
            for i in range(container_count)
        ],
    )
    zest_manifest = CorridorManifest(
        zones=zones,
        containers=[
            ContainerModel(
                container_id=f"ZST-{i:03d}",
                destination_zone=DEFAULT_CORRIDOR_PORTS[i % len(DEFAULT_CORRIDOR_PORTS)].zone_code,
                regulatory={"data_lead_time_hours": 120.0, "ncts_mrn": f"26RO00000{i:05d}"},
                fti004_handoff={
                    "quay_to_rail_cut_through": True,
                    "offline_customs_fallout": True,
                },
            )
            for i in range(container_count)
        ],
    )

    legacy_metrics = StochasticMilkRunSimulator(
        manifest=legacy_manifest,
        seed=42,
        capacity_deficit_pct=capacity_deficit_pct,
        yard_utilization_pct=yard_utilization_pct,
    ).run_simulation()

    zest_metrics = StochasticMilkRunSimulator(
        manifest=zest_manifest,
        seed=42,
        capacity_deficit_pct=capacity_deficit_pct,
        yard_utilization_pct=yard_utilization_pct,
    ).run_simulation()

    dwell_reduction_pct = (
        round((1.0 - (zest_metrics["mean_dwell_hours"] / legacy_metrics["mean_dwell_hours"])) * 100.0, 1)
        if legacy_metrics["mean_dwell_hours"] > 0
        else 0.0
    )

    return {
        "capacity_deficit_pct": capacity_deficit_pct,
        "yard_utilization_pct": yard_utilization_pct,
        "legacy_mean_dwell_hours": legacy_metrics["mean_dwell_hours"],
        "legacy_mean_rehandles": legacy_metrics["mean_rehandles"],
        "zest_mean_dwell_hours": zest_metrics["mean_dwell_hours"],
        "zest_mean_rehandles": zest_metrics["mean_rehandles"],
        "dwell_reduction_pct": dwell_reduction_pct,
    }
