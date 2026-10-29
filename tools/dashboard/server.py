"""
Project ZeST — Multi-Ship Seaport SDN & Rail Transfer Telemetry Server
File: tools/dashboard/server.py
Architecture: Decoupled T-5 Control Plane (eFTI Packet Headers) vs. T=0 Cut-Through Switch
License: Apache 2.0 (open-zest/zest-core)
"""

import asyncio
import json
import math
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Project ZeST — SDN Port & Rail Transfer Telemetry",
    version="0.4.1-sdn-packet-fix",
    description="T-5 Control Plane vs. T=0 Physical Forwarding Plane Telemetry Engine"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DASHBOARD_HTML_PATH = Path(__file__).parent / "index.html"
REPO_ROOT = Path(__file__).resolve().parents[2]
MAP_SCRIPT_PATH = REPO_ROOT / "tools" / "corridor_map" / "build_map.py"
MAP_CANDIDATE_PATHS = [
    REPO_ROOT / "tools" / "corridor_map" / "corridor_nsrm_map.html",
    REPO_ROOT / "corridor_nsrm_map.html",
    REPO_ROOT / "docs" / "corridor_nsrm_map.html",
]

# ---------------------------------------------------------------------------
# LOCKED MASTER SPEC BENCHMARK CONSTANTS & ZONAL TOPOLOGY
# ---------------------------------------------------------------------------
ZONES: List[Dict[str, Any]] = [
    {
        "zone_id": "ZONE_A_DUI",
        "name": "Duisburg Gateway (Ruhr)",
        "corridor": "RFC 1 Rhine-Alpine",
        "country": "DE",
        "distance_km": 210,
        "siding_m": 740,
        "setout_min": 15,
        "teu_allocated": 640,
        "air_diverted_tonnes": 420,
    },
    {
        "zone_id": "ZONE_B_VRN",
        "name": "Venlo Border Hub (195km Breakeven)",
        "corridor": "NL-DE Feeder Axis",
        "country": "NL/DE",
        "distance_km": 195,
        "siding_m": 740,
        "setout_min": 12,
        "teu_allocated": 480,
        "air_diverted_tonnes": 310,
    },
    {
        "zone_id": "ZONE_C_POZ",
        "name": "Poznań Franowo / Sławków",
        "corridor": "RFC 8 North Sea-Baltic (3SI)",
        "country": "PL",
        "distance_km": 890,
        "siding_m": 740,
        "setout_min": 15,
        "teu_allocated": 520,
        "air_diverted_tonnes": 610,
    },
    {
        "zone_id": "ZONE_D_VIE",
        "name": "Prague-Uhříněves / Česká Třebová",
        "corridor": "RFC 7 / RFC 9 Bohemian Spine",
        "country": "CZ",
        "distance_km": 820,
        "siding_m": 740,
        "setout_min": 15,
        "teu_allocated": 440,
        "air_diverted_tonnes": 540,
    },
    {
        "zone_id": "ZONE_E_LYS",
        "name": "Basel Kleinhüningen / Upper Rhine",
        "corridor": "RFC 1 / RFC 2 Alpine Portal",
        "country": "CH/DE",
        "distance_km": 680,
        "siding_m": 740,
        "setout_min": 15,
        "teu_allocated": 360,
        "air_diverted_tonnes": 390,
    },
    {
        "zone_id": "ZONE_F_BUD",
        "name": "Budapest BILK & Curtici Railport",
        "corridor": "RFC Orient / East-Med (3SI)",
        "country": "HU/RO",
        "distance_km": 1280,
        "siding_m": 740,
        "setout_min": 15,
        "teu_allocated": 400,
        "air_diverted_tonnes": 580,
    },
]

VESSELS: List[Dict[str, Any]] = [
    {
        "vessel_id": "VSL-01",
        "name": "MSC AMELIA (24,000 TEU)",
        "berth_id": "BERTH_Q01",
        "phase": "AT_BERTH_DISCHARGING",
        "eta_hours": 0,
        "call_containers": 1500,
        "call_teu": 2840,
        "gross_mass_t": 31051.5,
        "efti_resolved_pct_zest": 100.0,
        "efti_resolved_pct_legacy": 21.4,
        "legacy_berth_hrs": 54.0,
        "zest_berth_hrs": 38.5,
        "legacy_crane_mph": 25.2,
        "zest_crane_mph": 34.1,
    },
    {
        "vessel_id": "VSL-02",
        "name": "MAERSK MC-KINNEY MØLLER",
        "berth_id": "BERTH_Q02",
        "phase": "AT_BERTH_DISCHARGING",
        "eta_hours": 0,
        "call_containers": 1420,
        "call_teu": 2680,
        "gross_mass_t": 29410.0,
        "efti_resolved_pct_zest": 100.0,
        "efti_resolved_pct_legacy": 18.0,
        "legacy_berth_hrs": 51.5,
        "zest_berth_hrs": 36.8,
        "legacy_crane_mph": 24.8,
        "zest_crane_mph": 33.6,
    },
    {
        "vessel_id": "VSL-03",
        "name": "CMA CGM JACQUES SAADÉ",
        "berth_id": "BERTH_Q03",
        "phase": "T_MINUS_72H_BAY_OF_BISCAY",
        "eta_hours": -72,
        "call_containers": 1610,
        "call_teu": 3020,
        "gross_mass_t": 33120.0,
        "efti_resolved_pct_zest": 99.8,
        "efti_resolved_pct_legacy": 4.2,
        "legacy_berth_hrs": 58.0,
        "zest_berth_hrs": 41.2,
        "legacy_crane_mph": 25.5,
        "zest_crane_mph": 34.5,
    },
    {
        "vessel_id": "VSL-04",
        "name": "EVER ALOT (24,004 TEU)",
        "berth_id": "BERTH_Q04",
        "phase": "T_MINUS_120H_SUEZ_APPROACH",
        "eta_hours": -120,
        "call_containers": 1550,
        "call_teu": 2910,
        "gross_mass_t": 31890.0,
        "efti_resolved_pct_zest": 98.4,
        "efti_resolved_pct_legacy": 0.0,
        "legacy_berth_hrs": 55.5,
        "zest_berth_hrs": 39.4,
        "legacy_crane_mph": 25.0,
        "zest_crane_mph": 33.9,
    },
]

RAIL_TRACKS: List[Dict[str, Any]] = [
    {"track_id": "TRK-02", "zone_id": "ZONE_A_DUI", "rake_length_m": 740, "wagons": 36, "mass_limit_t": 2200, "utilization_zest_pct": 97.2, "utilization_legacy_pct": 74.5},
    {"track_id": "TRK-04", "zone_id": "ZONE_C_POZ", "rake_length_m": 740, "wagons": 36, "mass_limit_t": 2200, "utilization_zest_pct": 96.8, "utilization_legacy_pct": 71.0},
    {"track_id": "TRK-06", "zone_id": "ZONE_D_VIE", "rake_length_m": 740, "wagons": 36, "mass_limit_t": 2200, "utilization_zest_pct": 95.9, "utilization_legacy_pct": 73.2},
    {"track_id": "TRK-08", "zone_id": "ZONE_F_BUD", "rake_length_m": 740, "wagons": 36, "mass_limit_t": 2200, "utilization_zest_pct": 96.4, "utilization_legacy_pct": 69.8},
]


def compute_queuing_compounding(queue_ships: int = 6, berth_hours_saved: float = 15.5) -> Dict[str, Any]:
    rho_legacy = 0.86
    rho_zest = 0.64
    pk_legacy = rho_legacy / (1.0 - rho_legacy)
    pk_zest = rho_zest / (1.0 - rho_zest)
    queue_collapse_pct = round((1.0 - (pk_zest / pk_legacy)) * 100.0, 1)

    fleet_hours_saved = round(queue_ships * berth_hours_saved, 1)
    hourly_ship_burn_eur = 3666.0
    fleet_cash_saved_eur = int(fleet_hours_saved * hourly_ship_burn_eur)

    return {
        "anchored_ships_waiting": queue_ships,
        "berth_hours_shaved_per_call": berth_hours_saved,
        "berth_time_reduction_pct": 28.7,
        "rho_legacy": rho_legacy,
        "rho_zest": rho_zest,
        "queue_collapse_pct": queue_collapse_pct,
        "total_fleet_hours_eliminated": fleet_hours_saved,
        "fleet_cash_saved_eur": fleet_cash_saved_eur,
    }


def generate_live_packets(tick: int) -> List[Dict[str, Any]]:
    prefixes = ["MSCU", "MAEU", "CMAU", "EISU"]
    packets = []
    for i in range(12):
        zone = ZONES[(i + tick) % len(ZONES)]
        vessel = VESSELS[i % len(VESSELS)]
        track = RAIL_TRACKS[i % len(RAIL_TRACKS)]
        bic = f"{prefixes[i % 4]}{482910 + i * 137 + (tick % 9)}0"
        vgm_t = round(18.4 + ((i * 1.7) % 11.2), 1)
        wagon_slot = f"UIC-W{(i % 36) + 1:02d}-P{(i % 2) + 1}"

        packets.append({
            "bic_id": bic,
            "vessel_id": vessel["vessel_id"],
            "vessel_name": vessel["name"],
            "berth_id": vessel["berth_id"],
            "track_id": track["track_id"],
            "zone_id": zone["zone_id"],
            "zone_name": zone["name"],
            "vgm_tonnes": vgm_t,
            "t5_header_hash": f"0x9f{i:02x}e7a{tick % 10}",
            "ncts_t1_status": "PRE_CLEARED_T_MINUS_5D",
            "wagon_slot": wagon_slot,
            "legacy_routing": f"3D_YARD_STACK_BLK_{chr(65 + (i % 4))}_TIER_{(i % 4) + 1}",
            "legacy_digs": round(1.4 + ((i % 3) * 0.4), 1),
            "legacy_dwell_h": round(52.0 + ((i * 2.3) % 11.0), 1),
            "zest_routing": f"CUT_THROUGH_AGV -> {track['track_id']} ({wagon_slot})",
            "zest_digs": 0.0,
            "zest_dwell_h": 0.31,
        })
    return packets


def build_telemetry_snapshot(tick: int = 0) -> Dict[str, Any]:
    jitter = math.sin(tick * 0.3) * 0.02
    queuing = compute_queuing_compounding(queue_ships=6, berth_hours_saved=15.5)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tick": tick,
        "sdn_architecture": {
            "axiom": "Data Precedes Physical Unit by T-5 Days (120 Hours)",
            "control_plane": {
                "standard": "EU eFTI Reg 2020/1056 + openmanifest.v1",
                "crystallization_lead_hours": 120,
                "headers_resolved_at_sea_pct": 100.0,
                "legacy_headers_resolved_at_berth_pct": 21.4,
            },
            "data_plane_comparison": {
                "legacy": {
                    "mode_label": "LEGACY: ASYNC HEADERS -> 3D STACK BUFFERBLOAT (DISK STORAGE)",
                    "mean_terminal_dwell_h": round(57.39 + jitter * 5, 2),
                    "quayside_transfer_h": 6.80,
                    "yard_rehandles_per_box": 1.65,
                    "port_to_rail_lifts": 5.2,
                    "yard_stack_occupancy_pct": 84.5,
                    "agv_starvation_idle_pct": 15.4,
                    "gross_crane_rate_mph": round(25.1 + jitter * 2, 1),
                    "gross_vessel_berth_h": 54.0,
                    "rehandle_waste_eur_per_call": 785000,
                    "transit_variance_sigma_days": 6.8,
                    "rail_breakeven_km": 540,
                },
                "zest": {
                    "mode_label": "ZeST SDN: T-5 HEADER LOCKED -> CUT-THROUGH SWITCH (ZERO STACK)",
                    "mean_terminal_dwell_h": 4.43,
                    "quayside_transfer_h": 0.31,
                    "yard_rehandles_per_box": 0.00,
                    "port_to_rail_lifts": 2.0,
                    "yard_stack_occupancy_pct": 8.2,
                    "agv_starvation_idle_pct": 1.1,
                    "gross_crane_rate_mph": round(34.2 - jitter * 2, 1),
                    "gross_vessel_berth_h": 38.5,
                    "rehandle_savings_eur_per_call": 785000,
                    "transit_variance_sigma_days": 0.35,
                    "rail_breakeven_km": 195,
                },
            },
            "maritime_queue_compounding": queuing,
            "air_freight_arbitrage": {
                "air_freight_rate_usd_kg": 4.50,
                "zest_rail_rate_usd_kg": 0.25,
                "air_co2_g_tkm": 680,
                "zest_rail_co2_g_tkm": 18,
                "corridor_door_to_door_days": "18–21 Days (σ < 24h)",
                "high_value_tonnes_converted_per_call": 2850,
                "bco_freight_savings_usd_per_call": 12112500,
            },
        },
        "vessels": VESSELS,
        "rail_tracks": RAIL_TRACKS,
        "zones": ZONES,
        "live_packets": generate_live_packets(tick),
    }


@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    if DASHBOARD_HTML_PATH.exists():
        return HTMLResponse(content=DASHBOARD_HTML_PATH.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Dashboard HTML not found</h1>", status_code=404)


@app.get("/map", response_class=HTMLResponse)
async def serve_corridor_map():
    for candidate in MAP_CANDIDATE_PATHS:
        if candidate.exists():
            return HTMLResponse(content=candidate.read_text(encoding="utf-8"))
    if MAP_SCRIPT_PATH.exists():
        subprocess.run([sys.executable, str(MAP_SCRIPT_PATH)], cwd=str(REPO_ROOT), check=False)
        for candidate in MAP_CANDIDATE_PATHS:
            if candidate.exists():
                return HTMLResponse(content=candidate.read_text(encoding="utf-8"))
    return HTMLResponse(
        content="<h1>Corridor Map HTML not found. Run: python tools/corridor_map/build_map.py</h1>",
        status_code=404,
    )


@app.get("/api/telemetry", response_class=JSONResponse)
async def get_telemetry_snapshot():
    return JSONResponse(content=build_telemetry_snapshot(tick=1))


@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    await websocket.accept()
    tick = 0
    try:
        while True:
            payload = build_telemetry_snapshot(tick=tick)
            await websocket.send_text(json.dumps(payload))
            tick += 1
            await asyncio.sleep(1.5)
    except WebSocketDisconnect:
        pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8050, reload=True)
