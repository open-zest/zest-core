"""
Project ZeST - Interactive Physical-Digital Twin Dashboard
Couples physical container flows with upstream eFTI regulatory data tokens.
Visualizes terminal dwell alongside end-to-end corridor delivery times.
"""

from collections import Counter
import streamlit as st
import pandas as pd

from solvers.generators.manifest_gen import generate_synthetic_manifest
from solvers.des.milkrun_sim import StochasticMilkRunSimulator, DEFAULT_CORRIDOR_PORTS, PLANNING_CUTOFF_HOURS
from schemas.manifest_models import CorridorManifest, ZoneModel, CustomsChannel

st.set_page_config(
    page_title="Project ZeST | Digital-Physical Twin",
    page_icon="🚆",
    layout="wide"
)

# Header & Context
st.title("🚆 Project ZeST: Physical-Digital Container Twin")
st.caption("Discrete-Event Simulation Coupling Physical Rail Gantry Moves with eFTI CDS Regulatory Tokens | EU Reg 2020/1056")

# Sidebar Controls
st.sidebar.header("Operational Regime")

regime_choice = st.sidebar.radio(
    "Documentation Settlement Horizon:",
    [
        "Project ZeST: High-Seas eFTI Settlement",
        "Legacy Push: Discharge Trigger (Current Baseline)"
    ],
    help="Toggle between shifting paperwork settlement upstream to the sea voyage vs. treating vessel arrival as the documentation trigger."
)

regime_key = "HIGH_SEAS_eFTI" if "ZeST" in regime_choice else "LEGACY_DISCHARGE_TRIGGER"

st.sidebar.markdown("---")
st.sidebar.header("Simulation Parameters")
total_containers = st.sidebar.slider("Vessel Manifest Size (Boxes)", min_value=100, max_value=2500, value=1500, step=100)
sim_seed = st.sidebar.number_input("Random Seed", value=42, step=1)
vessel_name = st.sidebar.text_input("Vessel Name", value="ZeST Rotterdam Pioneer")

# Run Simulation Pipeline
@st.cache_data(show_spinner="Running discrete-event coupled simulation...")
def run_twin_pipeline(n_boxes, seed, name, regime):
    vessel_manifest = generate_synthetic_manifest(
        total_containers=n_boxes, 
        seed=seed, 
        vessel_name=name,
        filing_regime=regime
    )
    zones = [ZoneModel(zone_id=p.zone_code, name=p.name) for p in DEFAULT_CORRIDOR_PORTS]
    corridor_manifest = CorridorManifest(
        vessel_manifest=vessel_manifest,
        zones=zones,
        containers=vessel_manifest.containers
    )
    sim = StochasticMilkRunSimulator(manifest=corridor_manifest, seed=seed)
    metrics = sim.run_simulation()
    return vessel_manifest, metrics

vessel_manifest, metrics = run_twin_pipeline(total_containers, sim_seed, vessel_name, regime_key)
records = metrics["records"]
df_records = pd.DataFrame(records)

# 1. Top-Level Physical & Data KPI Cards
st.subheader("1. Upstream eFTI Data Stream vs. Terminal Gate Outcome")
c1, c2, c3, c4 = st.columns(4)

channels = Counter(c.regulatory.customs_channel for c in vessel_manifest.containers)
pre_arrival_rate = sum(1 for c in vessel_manifest.containers if c.regulatory.data_lead_time_hours >= PLANNING_CUTOFF_HOURS) / total_containers * 100.0

direct_rail = df_records[df_records["route_path"] == "DIRECT_TO_RAIL"]
yard_buffer = df_records[df_records["route_path"] == "YARD_BUFFER_STACK"]
direct_rail_rate = len(direct_rail) / total_containers * 100.0

c1.metric(
    "eFTI Green Channel Rate", 
    f"{channels[CustomsChannel.GREEN] / total_containers * 100:.1f}%", 
    f"{channels[CustomsChannel.GREEN]} of {total_containers} boxes"
)
c2.metric(
    f"Pre-Cleared (≥{PLANNING_CUTOFF_HOURS:.0f}h Notice)", 
    f"{pre_arrival_rate:.1f}%", 
    "Verified for Train Load List"
)
c3.metric(
    "Direct-to-Rail Bypass Rate", 
    f"{direct_rail_rate:.1f}%", 
    f"+{direct_rail_rate:.1f}% vs 0% baseline",
    delta_color="normal"
)
c4.metric(
    "Mean Dwell (Fleet Wide)", 
    f"{metrics['mean_dwell_hours']:.1f} hrs", 
    f"-{57.39 - metrics['mean_dwell_hours']:.1f} hrs vs 57.4h baseline",
    delta_color="inverse"
)

st.markdown("---")

# 2. Comparative Operational Metrics
st.subheader("2. Operational Dwell & Crane Utilization Comparison")
col_comp1, col_comp2 = st.columns(2)

with col_comp1:
    comp_data = {
        "Operational Metric": [
            "Direct-to-Rail Siding Rate",
            "Yard Buffer Divert Rate (Exceptions)",
            "Mean Dwell (Direct Rail Flow)",
            "Mean Dwell (Buffer Exceptions)",
            "Fleet-Wide Mean Dwell",
            "Crane Rehandles per Container"
        ],
        "Traditional Push Baseline": [
            "0.0%",
            "100.0%",
            "N/A (All Buffered)",
            "57.39 hrs",
            "57.39 hrs",
            "1.46 moves"
        ],
        "Current Simulation Output": [
            f"{direct_rail_rate:.1f}%",
            f"{100.0 - direct_rail_rate:.1f}%",
            f"{direct_rail['dwell_hours'].mean():.2f} hrs" if not direct_rail.empty else "N/A (0 boxes)",
            f"{yard_buffer['dwell_hours'].mean():.2f} hrs" if not yard_buffer.empty else "0.0 hrs",
            f"{metrics['mean_dwell_hours']:.2f} hrs",
            f"{metrics['mean_rehandles']:.2f} moves"
        ]
    }
    st.table(pd.DataFrame(comp_data))

with col_comp2:
    if regime_key == "HIGH_SEAS_eFTI":
        st.success(
            f"""
            **Active Regime: Project ZeST (High-Seas Settlement)**
            * **The Root Cause Solved:** Data settled while steaming across the ocean.
            * **Outcome:** **{direct_rail_rate:.1f}%** of containers beat the 10-hour planning freeze with Green status, completely bypassing the yard buffer.
            * **Terminal Impact:** Rehandles collapse to **{metrics['mean_rehandles']:.2f}** moves per box.
            """
        )
    else:
        st.error(
            f"""
            **Active Regime: Legacy Push (Discharge Trigger)**
            * **The Flaw Exposed:** Paperwork only starts when the ship hits the harbor.
            * **Outcome:** Only **{direct_rail_rate:.1f}%** clear before the 10-hour freeze. **{100.0 - direct_rail_rate:.1f}%** are dumped into the yard stack.
            * **Terminal Impact:** Dwell climbs to **{metrics['mean_dwell_hours']:.1f} hours** with high rehandles.
            """
        )

st.markdown("---")

# 3. Interactive Data Lead-Time vs. Dwell Curve
st.subheader("3. Data Readiness vs. Terminal Dwell Curve (The 10-Hour Boundary)")
st.caption(f"The vertical threshold at X = {PLANNING_CUTOFF_HOURS:.0f}h represents the terminal TOS train-planning lock. Boxes to the right with Green tokens flow direct to rail; boxes to the left get locked into the yard buffer stack.")

chart_data = df_records[["data_lead_time_hours", "dwell_hours", "route_path", "customs_channel"]]
st.scatter_chart(
    chart_data,
    x="data_lead_time_hours",
    y="dwell_hours",
    color="route_path",
    height=420
)

st.markdown("---")

# 4. Total End-to-End Time to Delivery (Terminal Dwell + Line-Haul Rail Transit)
st.subheader("4. Total Through-Time to Delivery: Rotterdam Quay ➔ Inland Dry Port")
st.caption("Total elapsed time from vessel lift-off to arrival at the hinterland rail ramp. Notice how 57 hours of static port dwell dominates traditional transit times.")

rail_speed_kmh = 65.0  # Commercial average speed including crew changes & border crossings

delivery_rows = []
for port in DEFAULT_CORRIDOR_PORTS:
    z_key = port.zone_code.value
    zone_recs = df_records[df_records["destination_zone"] == z_key]
    sim_dwell = zone_recs["dwell_hours"].mean() if not zone_recs.empty else metrics["mean_dwell_hours"]
    
    line_haul_transit = port.distance_km / rail_speed_kmh
    
    # Traditional: 57.39h dwell + intermediate marshalling buffer (~2h/100km) + rail transit
    trad_total = 57.39 + (port.distance_km * 0.02) + line_haul_transit
    # Simulated Active Scenario: actual simulated dwell + direct scheduled line-haul
    sim_total = sim_dwell + line_haul_transit
    
    delivery_rows.append({
        "Dry Port": port.name,
        "Distance (km)": port.distance_km,
        "Traditional Baseline (Hours)": round(trad_total, 1),
        "Active Simulation (Hours)": round(sim_total, 1),
        "Time Saved (Hours)": round(trad_total - sim_total, 1),
        "Velocity Improvement": f"{((trad_total - sim_total) / trad_total) * 100:.0f}% faster"
    })

df_delivery = pd.DataFrame(delivery_rows)

col_chart, col_stats = st.columns([3, 2])

with col_chart:
    st.markdown("**Comparison of End-to-End Delivery Hours**")
    chart_df = df_delivery.set_index("Dry Port")[["Traditional Baseline (Hours)", "Active Simulation (Hours)"]]
    st.bar_chart(chart_df, height=360)

with col_stats:
    st.markdown("**Corridor Velocity Table**")
    st.dataframe(
        df_delivery[["Dry Port", "Distance (km)", "Active Simulation (Hours)", "Traditional Baseline (Hours)", "Velocity Improvement"]],
        use_container_width=True,
        hide_index=True
    )
    st.caption("💡 Line-haul rail speed assumed at 65 km/h across TEN-T Core Network Corridors.")

st.markdown("---")

# 5. Macro-Corridor Allocation
st.subheader("5. Macro-Corridor Rail Siding Allocation")

zone_summary = vessel_manifest.zone_distribution_summary()
zone_rows = []
for port in DEFAULT_CORRIDOR_PORTS:
    z_key = port.zone_code.value
    cnt = zone_summary.get(z_key, 0)
    zone_rows.append({
        "Corridor Dry Port": port.name,
        "Macro Zone Code": z_key,
        "Allocated Volume (Boxes)": cnt,
        "Share (%)": f"{cnt / total_containers * 100:.1f}%",
        "Corridor Rail Distance": f"{port.distance_km:.0f} km"
    })

st.dataframe(pd.DataFrame(zone_rows), use_container_width=True, hide_index=True)
