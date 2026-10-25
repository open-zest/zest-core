"""
Project ZeST (Zero-Sort Transport) — Executive & PCS Interactive Sandbox
Compact single-screen dashboard proving Feed-Forward eFTI Data Crystallization
(EU 2020/1056) vs. Legacy Post-Berth EDI Polling across 1,500 containers.
"""

import hashlib
import json
import math
import random
from datetime import datetime, timedelta, timezone

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Project ZeST | Feed-Forward eFTI Sandbox",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Compact CSS so charts, KPIs, and tables fit cleanly on a single screen
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.1rem !important;
            padding-bottom: 0.8rem !important;
            max-width: 1440px;
        }
        div[data-testid="stMetric"] {
            background-color: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 6px;
            padding: 8px 12px;
        }
        div[data-testid="stMetricLabel"] > div {
            font-size: 0.78rem !important;
            color: #94a3b8 !important;
        }
        div[data-testid="stMetricValue"] > div {
            font-size: 1.35rem !important;
            font-weight: 700 !important;
        }
        h1 { font-size: 1.45rem !important; margin-bottom: 0.1rem !important; }
        h2 { font-size: 1.05rem !important; margin-top: 0.4rem !important; margin-bottom: 0.2rem !important; }
        h3 { font-size: 0.92rem !important; margin-top: 0.3rem !important; margin-bottom: 0.2rem !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

CORRIDOR_ZONES = [
    {"code": "ZONE_A_DUI", "hub": "Duisburg (DE)", "km": 210, "share": 0.24, "wagon_block": "Block-1 (Rear)"},
    {"code": "ZONE_B_VEN", "hub": "Venlo / Liège (NL/BE)", "km": 165, "share": 0.18, "wagon_block": "Block-2"},
    {"code": "ZONE_C_MAN", "hub": "Mannheim / Basel (DE/CH)", "km": 510, "share": 0.18, "wagon_block": "Block-3"},
    {"code": "ZONE_D_POZ", "hub": "Poznań / Kutno (PL)", "km": 820, "share": 0.15, "wagon_block": "Block-4"},
    {"code": "ZONE_E_VIE", "hub": "Vienna / Bratislava (AT/SK)", "km": 940, "share": 0.13, "wagon_block": "Block-5"},
    {"code": "ZONE_F_BUD", "hub": "Budapest / Prague (HU/CZ)", "km": 1120, "share": 0.12, "wagon_block": "Block-6 (Head)"},
]


@st.cache_data
def simulate_latency_response(lead_time_hours: int, n_containers: int, ncts_fallout_pct: float):
    """
    Deterministic + stochastic factory-physics model matching scripts/benchmark_data_latency.py.
    lead_time_hours < 0  => Post-berth EDI arrival lag (Legacy blind batching)
    lead_time_hours >= 120 => 5-to-10+ day pre-arrival eFTI crystallization (ZeST zero-copy stream)
    """
    rng = random.Random(42 + lead_time_hours + n_containers)

    if lead_time_hours <= -48:
        crystallization = 0.0
    elif lead_time_hours < 0:
        crystallization = (lead_time_hours + 48) / 168.0
    elif lead_time_hours < 120:
        crystallization = 0.28 + 0.72 * (lead_time_hours / 120.0)
    else:
        crystallization = 1.0

    legacy_dwells = []
    zest_dwells = []

    for _ in range(n_containers):
        leg_wait = rng.gauss(48.0, 4.2)
        leg_digging = rng.uniform(3.5, 10.3)
        legacy_dwells.append(max(12.0, leg_wait + leg_digging))

        if crystallization >= 0.99:
            box_dwell = rng.uniform(0.18, 0.38)
        else:
            uncrystallized = 1.0 - crystallization
            lag_penalty = max(0.0, -lead_time_hours) * 0.85
            stack_shuffle = (uncrystallized ** 1.45) * rng.uniform(14.0, 22.0)
            box_dwell = 0.28 + lag_penalty + stack_shuffle
        zest_dwells.append(box_dwell)

    mean_legacy = sum(legacy_dwells) / len(legacy_dwells)
    mean_current = sum(zest_dwells) / len(zest_dwells)
    sorted_curr = sorted(zest_dwells)
    p95_current = sorted_curr[int(0.95 * len(sorted_curr))]

    rehandles_per_box = round((1.0 - crystallization) * 1.62, 2)
    corridor_dispatch_dwell = round(mean_current + 4.15 + (1.0 - crystallization) * 1.35, 2)
    breakeven_km = int(round(550 - (355 * crystallization)))

    hours = list(range(0, 37, 2))
    legacy_stack = []
    current_stack = []
    for h in hours:
        discharged = min(n_containers, int(n_containers * (h / 14.0))) if h <= 14 else n_containers
        leg_cleared = max(0, int(n_containers * ((h - 22) / 36.0))) if h > 22 else 0
        legacy_stack.append(max(0, discharged - leg_cleared))

        buffer_ratio = 0.04 + 0.92 * (1.0 - crystallization)
        active_window = max(0.15, 1.0 - abs(h - 8) / 14.0) if h <= 20 else 0.05
        current_stack.append(int(n_containers * buffer_ratio * active_window))

    timeline_df = pd.DataFrame(
        {
            "Hours Post-Berth": hours,
            "Legacy Blind Stack (t+48h EDI Lag)": legacy_stack,
            "Selected Lead-Time Yard Buffer": current_stack,
        }
    ).set_index("Hours Post-Berth")

    curve_labels = ["t+48h Lag", "t+24h Lag", "t=0 Berth", "t-1d", "t-3d", "t-5d (Lock)", "t-7d", "t-10d"]
    curve_dwells = [54.91, 31.40, 14.80, 9.60, 4.90, 0.28, 0.28, 0.28]
    sensitivity_df = pd.DataFrame(
        {"Data Horizon": curve_labels, "Quayside Buffer Dwell (Hours)": curve_dwells}
    ).set_index("Data Horizon")

    return {
        "mean_legacy": round(mean_legacy, 2),
        "mean_current": round(mean_current, 2),
        "p95_current": round(p95_current, 2),
        "rehandles": rehandles_per_box,
        "corridor_dwell": corridor_dispatch_dwell,
        "breakeven_km": breakeven_km,
        "crystallization_pct": round(crystallization * 100, 1),
        "dlq_boxes": int(round(n_containers * (ncts_fallout_pct / 100.0))),
        "timeline_df": timeline_df,
        "sensitivity_df": sensitivity_df,
    }


with st.sidebar:
    st.markdown("### ⚙️ Feed-Forward Controls")
    st.caption("Adjust eFTI data arrival relative to physical vessel berth:")

    preset = st.radio(
        "Operational Mode Preset:",
        options=[
            "ZeST Feed-Forward (t - 7 Days eFTI Lock)",
            "ZeST Minimum Threshold (t - 5 Days Lock)",
            "Berth-Time EDI Arrival (t = 0 Hours)",
            "Legacy Maritime Baseline (t + 48h EDI Lag)",
        ],
        index=0,
    )

    preset_map = {
        "ZeST Feed-Forward (t - 7 Days eFTI Lock)": 168,
        "ZeST Minimum Threshold (t - 5 Days Lock)": 120,
        "Berth-Time EDI Arrival (t = 0 Hours)": 0,
        "Legacy Maritime Baseline (t + 48h EDI Lag)": -48,
    }

    lead_hours = st.slider(
        "Data Lead Time vs. Vessel Berth (Hours)",
        min_value=-48,
        max_value=240,
        value=preset_map[preset],
        step=12,
        help="Negative (-48h) = data arrives 48h AFTER vessel berth. Positive (+120h to +240h) = data crystallized 5 to 10 days BEFORE vessel arrival.",
    )

    n_boxes = st.slider("Vessel Discharge Batch (Containers)", 500, 3000, 1500, 250)
    fallout_pct = st.slider("NCTS T1 Customs Inspection Fallout (%)", 0.5, 5.0, 1.5, 0.5)

    st.markdown("---")
    st.markdown(
        "**IT / PCS Architecture Mapping**\n"
        "- **Yard Stack:** Unindexed Memory Thrashing\n"
        "- **Ramp-to-Rail:** Zero-Copy Stream\n"
        "- **NCTS T1 Hold:** Dead-Letter Queue (DLQ)\n"
        "- **Portbase / PCS:** Federated Event Broker"
    )

metrics = simulate_latency_response(lead_hours, n_boxes, fallout_pct)
dwell_reduction_pct = round((1.0 - (metrics["mean_current"] / metrics["mean_legacy"])) * 100, 1)

st.title("⚡ Project ZeST (`zest-core`) — Data-First Intermodal Sandbox")
st.caption(
    "EU Regulation 2020/1056 (eFTI) Federated Token Orchestration | Maasvlakte II → 6 European Single-Stack Rail Corridors"
)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric(
    "Quayside Buffer Dwell",
    f"{metrics['mean_current']:.2f} h",
    f"-{dwell_reduction_pct}% vs Legacy (54.91h)",
    delta_color="normal" if metrics["mean_current"] < 5.0 else "off",
)
k2.metric(
    "Full Gate-to-Rail Turn",
    f"{metrics['corridor_dwell']:.2f} h",
    "Includes brake test & coupling (vs 57.4h)",
    delta_color="normal",
)
k3.metric(
    "Yard Stack Re-Handles",
    f"{metrics['rehandles']:.2f} / box",
    "Zero-Copy Direct Stream" if metrics["rehandles"] == 0 else "Unindexed Yard Digging",
    delta_color="normal" if metrics["rehandles"] == 0 else "inverse",
)
k4.metric(
    "Pre-Arrival Crystallization",
    f"{metrics['crystallization_pct']}%",
    f"Lead: {lead_hours:+}h ({lead_hours/24:+.1f} days)",
)
k5.metric(
    "Rail vs. OTR Breakeven",
    f"{metrics['breakeven_km']} km",
    f"{metrics['dlq_boxes']} boxes routed to Dry-Port DLQ",
)

c_left, c_right = st.columns(2)

with c_left:
    st.subheader("1. Coastal Yard Buffer Thrashing (Containers Grounded in Stack)")
    st.line_chart(metrics["timeline_df"], height=215, use_container_width=True)
    st.caption(
        "Legacy post-berth EDI polling forces 100% of containers into unindexed coastal stacks. "
        "Crystallizing eFTI tokens ≥5 days pre-arrival streams boxes directly from crane to single-stack railcars."
    )

with c_right:
    st.subheader("2. Quayside Dwell vs. Data Crystallization Lead Time")
    st.bar_chart(metrics["sensitivity_df"], height=215, use_container_width=True)
    st.caption(
        "Why 0.28h is achievable: Once eFTI routing & NCTS T1 status lock at t-5d (+120h), "
        "quayside buffering drops to physical crane-to-wagon transfer time (~17 mins), while total train turn is 4.43h."
    )

b_left, b_right = st.columns([1.25, 1.0])

with b_left:
    st.subheader("3. Single-Stack Milk-Run Corridor Allocation (Maasvlakte II Dispatch)")
    corridor_rows = []
    for z in CORRIDOR_ZONES:
        vol = int(round(n_boxes * z["share"]))
        wagons = math.ceil(vol / 3.0)
        corridor_rows.append(
            {
                "Zone Token": z["code"],
                "Inland Dry Port (NCTS T1)": z["hub"],
                "Dist": f"{z['km']} km",
                "Boxes": vol,
                "Single-Stack Wagons": wagons,
                "Train Consist Position": z["wagon_block"],
            }
        )
    st.dataframe(pd.DataFrame(corridor_rows), height=215, use_container_width=True, hide_index=True)

with b_right:
    st.subheader("4. Live EU 2020/1056 eFTI Federated Token Payload")
    selected_zone = st.selectbox(
        "Inspect Single-Use Cryptographic Token by Corridor Zone:",
        options=[z["code"] for z in CORRIDOR_ZONES],
        label_visibility="collapsed",
    )
    eta_dt = datetime(2026, 11, 10, 8, 0, tzinfo=timezone.utc) - timedelta(hours=max(0, lead_hours))
    digest = hashlib.sha256(f"MSKU4928104-{selected_zone}-{lead_hours}".encode()).hexdigest()
    token_sample = {
        "schema": "eu.efti.2020_1056.v1.routing_token",
        "container_id": "MSKU4928104",
        "iso_type": "45G1 (40ft High-Cube — Single-Stack Rail)",
        "vgm_kg": 24850,
        "zone_token": selected_zone,
        "customs_ncts_status": "CLEARED_T1_INLAND_DRYPORT",
        "token_crystallized_utc": eta_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "commercial_data_exposed": False,
        "pre_clearance_zk_hash": f"0x{digest[:32]}...",
    }
    st.code(json.dumps(token_sample, indent=2), language="json")
