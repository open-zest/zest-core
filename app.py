import streamlit as st

st.set_page_config(
    page_title="Project ZeST | Port-Rail Corridor Twin",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Parameter Lookup Matrix (Grounded in zest-core Benchmarks)
CORRIDOR_DATA = {
    "RFC North Sea-Med (Rotterdam → Bettembourg/Basel/Lyon)": {
        "dest": "Bettembourg / Basel / Lyon",
        "corridor_code": "RFC 2",
        "border_gate": "Sterpenich / Bettembourg Border",
        "legacy_dwell": 54.9,
        "zest_dwell": 4.4,
        "legacy_border_dwell": 8.5,
        "zest_border_dwell": 0.2,
    },
    "RFC Rhine-Alpine (Rotterdam → Duisburg)": {
        "dest": "Duisburg Intermodal Terminal (DIT)",
        "corridor_code": "RFC 1",
        "border_gate": "Emmerich Border Siding",
        "legacy_dwell": 57.4,
        "zest_dwell": 4.4,
        "legacy_border_dwell": 6.8,
        "zest_border_dwell": 0.3,
    }
}

SCALE_DATA = {
    "1,500 Containers (2,792 TEU)": {
        "teu": 2792,
        "mass_tonnes": 31051,
        "legacy_velocity": 4.1,
        "zest_velocity": 18.2,
        "legacy_buf_util": 74.2,
        "zest_buf_util": 98.4,
    },
    "750 Containers (Feeder Batch)": {
        "teu": 1396,
        "mass_tonnes": 15525,
        "legacy_velocity": 3.2,
        "zest_velocity": 12.6,
        "legacy_buf_util": 58.1,
        "zest_buf_util": 89.2,
    }
}

# 2. Sidebar Controls
st.sidebar.header("Corridor Parameters")
corridor_choice = st.sidebar.selectbox(
    "Freight Corridor",
    list(CORRIDOR_DATA.keys())
)
scale_choice = st.sidebar.selectbox(
    "Vessel Consignment Scale",
    list(SCALE_DATA.keys())
)

st.sidebar.markdown("---")
st.sidebar.subheader("Architecture Mode")
mode = st.sidebar.radio(
    "Operational Selection (Before vs. After)",
    [
        "Legacy Baseline (Gate & Yard Dwell)",
        "ZeST Optimized (eFTI Pre-Clearance)"
    ],
    index=0
)
is_zest = mode.startswith("ZeST")

# 3. Dynamic Data Resolution
c_data = CORRIDOR_DATA[corridor_choice]
s_data = SCALE_DATA[scale_choice]

mean_dwell = c_data["zest_dwell"] if is_zest else c_data["legacy_dwell"]
dwell_delta = f"-{c_data['legacy_dwell'] - c_data['zest_dwell']:.1f} hrs (-{int(((c_data['legacy_dwell'] - c_data['zest_dwell'])/c_data['legacy_dwell'])*100)}%)" if is_zest else None

velocity = s_data["zest_velocity"] if is_zest else s_data["legacy_velocity"]
velocity_pct = int(((s_data["zest_velocity"] - s_data["legacy_velocity"]) / s_data["legacy_velocity"]) * 100)
velocity_delta = f"+{velocity_pct}% throughput" if is_zest else None

border_dwell = c_data["zest_border_dwell"] if is_zest else c_data["legacy_border_dwell"]
border_delta = f"-{c_data['legacy_border_dwell'] - c_data['zest_border_dwell']:.1f} hrs" if is_zest else None

buf_util = s_data["zest_buf_util"] if is_zest else s_data["legacy_buf_util"]
buf_delta = f"+{s_data['zest_buf_util'] - s_data['legacy_buf_util']:.1f}%" if is_zest else None

# 4. Main View Header
st.title("Project ZeST: Intermodal Digital Corridor Twin")
st.caption(f"Maasvlakte II → {c_data['dest']} | {c_data['corridor_code']} Alignment | eFTI (EU 2020/1056)")
st.markdown("---")

# 5. Executive Performance Indicators
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric(
        label="Mean Container Dwell",
        value=f"{mean_dwell:.1f} hrs",
        delta=dwell_delta
    )
with k2:
    st.metric(
        label="Terminal Yard Re-handles",
        value="0.0 moves" if is_zest else "3.8 moves",
        delta="-100% eliminated" if is_zest else None
    )
with k3:
    st.metric(
        label="Rail Transfer Velocity",
        value=f"{velocity:.1f} TEU/hr",
        delta=velocity_delta
    )
with k4:
    st.metric(
        label="Manifest Mass (Simulated)",
        value=f"{s_data['mass_tonnes']:,} t",
        delta=f"{s_data['teu']:,} TEU total"
    )

st.markdown("---")

# 6. Dynamic 3-Zone Telemetry
st.markdown("#### Transition Zone Telemetry")
z1, z2, z3 = st.columns(3)

with z1:
    st.markdown("**Zone 1: Ship-to-Shore**")
    if is_zest:
        st.success("Pre-Cleared (eFTI Token)")
        st.write("Routing: Direct to Quayside Rail Buffer")
        st.progress(1.0)
    else:
        st.error("Inspection Hold / Batch EDI")
        st.write("Routing: Terminal Storage Yard Stack")
        st.progress(0.35)

with z2:
    st.markdown("**Zone 2: Quayside Rail Buffer**")
    if is_zest:
        st.success("Single Direct Drop (STS → Wagon)")
        st.metric("Buffer Utilization", f"{buf_util:.1f}%", delta=buf_delta)
        st.progress(buf_util / 100.0)
    else:
        st.error("3 to 5 Yard Shuffles (Stack → AGV → Rail)")
        st.metric("Buffer Utilization", f"{buf_util:.1f}%")
        st.progress(buf_util / 100.0)

with z3:
    st.markdown(f"**Zone 3: Inland Border ({c_data['border_gate']})**")
    if is_zest:
        st.success("Digital Token Handshake (eFTI e-CMR/e-CIM)")
        st.metric("Border Stop Dwell", f"{border_dwell:.1f} hrs", delta=border_delta)
        st.progress(0.95)
    else:
        st.error("Physical Document Inspection & Rail Siding Halt")
        st.metric("Border Stop Dwell", f"{border_dwell:.1f} hrs")
        st.progress(0.20)

st.markdown("---")
st.caption(
    "Operational Principle: Dwell is an information latency failure. Decoupling data from physical ship arrival via eFTI tokens eliminates yard buffer re-handling."
)
