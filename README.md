# Project ZeST (`zest-core`) — Zero-Stack Terminal & Software-Defined Intermodal Network (SDN)

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Release: v0.5.0-rotterdam-showcase](https://img.shields.io/badge/Release-v0.5.0--rotterdam--showcase-emerald.svg)](https://github.com/open-zest/zest-core/releases)
[![Tests: 10 Passed](https://img.shields.io/badge/pytest-10_passed-brightgreen.svg)](#5-automated-verification--test-suite)
[![Standard: EU eFTI 2020/1056](https://img.shields.io/badge/Control_Plane-EU_eFTI_2020%2F1056-sky.svg)](#1-the-core-abstraction-axiom)

**Intermodal Europe 2026 (Rotterdam Ahoy, Nov 10–12) • Technical & Visual Architecture Suite**

---

## 1. The Core Abstraction Axiom

**Intermodal freight is not a single physical flow—it is a dual-stream packet-switching network consisting of a Control Plane (Manifest & Regulatory Data) and a Data Plane (Physical Containers).**

- **Legacy State of the Art (Router Bufferbloat):** Customs clearance (NCTS T1), commercial release pins, and rail wagon assignments resolve *asynchronously after vessel arrival* (`T=0`). Because the physical container arrives before its routing header is solved, terminals dump 78.6% of boxes into 5-high concrete yard stacks (`84.5%` density), triggering **1.65 unproductive re-handles (digs) per box**, **57.39 hours** of mean terminal dwell, and **15.4% quayside AGV starvation**.
- **The Project ZeST Paradigm (T-5 Control Plane Decoupling):** By binding the cryptographic **`openmanifest.v1` + EU eFTI (Reg 2020/1056)** header **5 days (`T-120h`) before pilot boarding**—paired with 4th-tensor origin-port block stowage—the seaport transforms from a passive storage warehouse into a **0.31-hour Layer-2 Cut-Through Switch** (`0.00` yard digs, `4.43h` total terminal turn).

---

## 2. Executive Benchmark Summary (Maasvlakte II ➔ European Hinterland)

| Operational Metric | Legacy Terminal Baseline | Project ZeST (100% SDN) | Day-1 Hybrid (50% Partial eFTI) | Strategic Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Control Plane Header Lock** | `T+0h` to `T+48h` (21.4% at berth) | **`T-120h` (100% at sea)** | `50%` Pre-Cleared / `50%` Stack | Eliminates customs & pin holds at spreader release |
| **Quayside-to-Rail Transfer** | `6.80 hours` | **`0.31 hours` (18.6 min)** | `3.56 hours` (Blended) | Direct STS crane ➔ AGV loop ➔ 740m on-dock rail siding |
| **Mean Terminal Turnaround** | `57.39 hours` | **`4.43 hours` (-92.3%)** | `30.91 hours` (-46.1%) | Eliminates concrete yard stack bufferbloat |
| **Unproductive Yard Re-Handles** | `1.65 digs/box` (5.2 lifts) | **`0.00 digs/box` (2.0 lifts)** | `0.83 digs/box` (3.6 lifts) | Saves **€785,000** in wasted crane work per ULCV call |
| **Gross Mega-Ship Berth Time** | `54.0 hours` (25.1 mph) | **`38.5 hours` (-28.7% / 34.2 mph)** | `46.3 hours` (-14.4%) | **+28% virtual quay capacity** with zero concrete capex |
| **Offshore Queue Wait (`M/Ek/c`)** | `ρ = 0.86` (Gridlock elbow) | **`ρ = 0.64` (-71.1% queue wait)** | **`ρ = 0.75` (-47.1% queue wait)** | **Non-linear dividend:** 50% adoption cuts queue wait by nearly half |
| **Rail-vs-Truck Break-Even** | `540 km` | **`195 km` (Venlo Gateway)** | `368 km` | Unlocks short-haul NL/DE feeder rail parity |
| **Corridor Transit Variance (`σ`)** | `±6.8 days` (Ad-hoc hump yards) | **`±0.35 days` (`<24h` SLA)** | `±3.58 days` | Pulls **$4.50/kg Air Freight** back onto **$0.25/kg Rail** (-97% CO₂) |
| **Origin-Port 4th-Tensor Stowage** | 3-Tensor (`B, R, T`) | **4-Tensor (`B, R, T, Zr`)** | Compatible | **`ΔGM = ±1.32 cm`** (inside ±5 cm sensor noise floor; 0 restows) |

---

## 3. Interactive Visual & Telemetry Suite (1-Command Master Launcher)

Start the FastAPI + WebSocket telemetry server to launch all **6 interactive HTML views** from a single browser window:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn tools.dashboard.server:app --host 127.0.0.1 --port 8050 --reload
```

Open **`http://127.0.0.1:8050/`** and use the top-right launcher bar to navigate the suite:

1. **Live Multi-Ship SDN & Rail Transfer Dashboard (`/`)** — `tools/dashboard/index.html`
   - Real-time WebSocket container packet stream (`1.5s` ticks), 3-mode view switcher (*Stacked*, *Legacy Only*, *ZeST Only*), interactive **Partial eFTI / Pre-Cleared Adoption Slider (`α_eFTI ∈ [0%, 100%]`)**, and multi-entity cross-filtering across 4 ULCV berths, 4 on-dock 740m rail tracks, and 6 EU catchment zones.
2. **Pan-EU / UK / IT Packet-Switched Corridor Map (`/map`)** — `docs/nsrm_packet_network_map.html`
   - Interactive Leaflet topology spanning Rotterdam Maasvlakte II across the UK Channel Tunnel spine (to Mossend/Scotland), the Rhine-Alpine & Italian spine (to Palermo), and the North Sea-Baltic / Bohemian / Three Seas Initiative (3SI) hubs (`ZONE_A_DUI` to `ZONE_F_BUD`).
3. **3-in-1 Persona Swimlane Storyboard (`/swimlane`)** — `docs/zest_swimlane_evolution.html`
   - Decoupled JSON-driven (`schemas/swimlane_phases.json`) storyboard with an instant lens switcher tailored for **Panasonic Automotive VSM (Lean/JIS)**, **Google Cloud SDN (OpenFlow/Packet Switching)**, and **EU TEN-T / DG MOVE (eFTI/CEF III Policy)**.
4. **3-Part Dual-Stream Process Block Architecture (`/process`)** — `docs/zest_process_architecture.html`
   - Side-by-side Mermaid process architecture diagrams (`schemas/diagrams/*.mmd`) covering (1) End-to-End Dual-Stream Flow, (2) Seaport Ingress Cut-Through Switching, and (3) Dry-Port 15-Minute Siding Egress.
5. **Origin-Port 4th-Tensor Stowage & Hydrostatic Proof (`/hydrostatics`)** — `docs/cspp_hydrostatic_feasibility.html` & `.md`
   - Naval architecture & Master Mariner feasibility brief proving that adding Destination Rail Zone (`Zr`) at Asian loading ports shifts metacentric height by only **`ΔGM = ±1.32 cm`** with `96.4%` shear-force safety margin and zero restows.
6. **1-Page Executive GUI Presenter Cheat Sheet (`/cheatsheet`)** — `docs/gui_presenter_cheatsheet.html` & `.md`
   - Printable 5-click demo choreography (90-second walkthrough) and Rotterdam stakeholder pivot matrix.

---

## 4. Repository Structure

```text
zest-core/
├── docs/
│   ├── nsrm_packet_network_map.html       # Pan-EU/UK/IT + 3SI interactive Leaflet map (/map)
│   ├── zest_swimlane_evolution.html       # 3-in-1 Persona Swimlane Storyboard (/swimlane)
│   ├── zest_process_architecture.html     # 3-part Dual-Stream Process Block Diagrams (/process)
│   ├── cspp_hydrostatic_feasibility.html  # 4th-Tensor Hydrostatic Proof ΔGM = ±1.32 cm (/hydrostatics)
│   ├── cspp_hydrostatic_feasibility.md    # Markdown edition of the Hydrostatic Proof
│   ├── gui_presenter_cheatsheet.html      # Printable 1-page presenter field guide (/cheatsheet)
│   └── gui_presenter_cheatsheet.md        # Markdown edition of the presenter cheat sheet
├── schemas/
│   ├── openmanifest.v1.json               # T-5 Control Plane JSON Schema (eFTI + VGM + UIC slot)
│   ├── manifest_models.py                 # Pydantic v2 models & cryptographic token validators
│   ├── nsrm_topology.json                 # Pan-European rail corridor & catchment zone topology
│   ├── swimlane_phases.json               # 3-persona vocabulary & phase definitions
│   └── diagrams/                          # Modular Mermaid (.mmd) source definitions
├── solvers/
│   ├── des/dwell_sim.py                   # SimPy discrete-event terminal & quayside queuing engine
│   ├── des/milkrun_sim.py                 # Stochastic 740m Takt rail milk-run & 15-min set-out solver
│   ├── zestow/zone_stow.py                # 4th-tensor origin-port stowage & GM stability solver
│   └── generators/manifest_gen.py         # Synthetic ULCV call & eFTI token generator
├── scripts/
│   ├── demo_runner.py                     # CLI benchmark runner (1,500 containers / 31,051.5t)
│   ├── build_nsrm_map.py                  # Generator for docs/nsrm_packet_network_map.html
│   ├── build_swimlane_flow.py             # Generator for docs/zest_swimlane_evolution.html
│   ├── build_process_diagrams.py          # Generator for docs/zest_process_architecture.html
│   └── build_cspp_brief.py                # Generator for docs/cspp_hydrostatic_feasibility.html
├── tools/dashboard/
│   ├── server.py                          # FastAPI + WebSocket telemetry engine & suite router
│   ├── index.html                         # Responsive Tailwind UI with Partial eFTI slider
│   └── queries.sql                        # Analytical SQL queries for port-rail transfer telemetry
└── tests/                                 # 10 automated pytest suites (DES, stowage, corridor, SDN)
```

---

## 5. Automated Verification & Test Suite

Run the complete 10-test verification suite (covering SimPy queuing, 4th-tensor hydrostatic stability, corridor set-outs, cryptographic manifest invariants, and non-linear `M/Ek/c` Partial eFTI adoption telemetry):

```bash
source .venv/bin/activate
pytest -v
```

---

## 6. License

Licensed under the **Apache License, Version 2.0**. Open-source reference architecture for the European physical internet and software-defined intermodal rail networks (`open-zest/zest-core`).
