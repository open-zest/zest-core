# Project ZeST (`zest-core`)
**Zero-Stack Transfer Simulation Engine for Deep-Sea Intermodal Corridors**

[![Release](https://img.shields.io/badge/release-v0.4.0--credibility--pkg-blue.svg)](https://github.com/open-zest/zest-core/releases/tag/v0.4.0-credibility-pkg)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Corridor: RFC North Sea–Med](https://img.shields.io/badge/Corridor-RFC_NSRM_/_Rhine--Alpine-orange.svg)](https://corridor-nsrm.eu/)

Project ZeST is an open-source, vendor-neutral discrete-event simulation (DES) framework that models the operational and economic elimination of deep-sea terminal rail dwell. 

The core thesis reframes terminal dwell not as a physical crane or handling bottleneck, but as an **information latency failure**. By decoupling regulatory and commercial consignment data from physical ship arrivals via **eFTI (EU Regulation 2020/1056)** advance tokens, terminals can bypass legacy Automated Stacking Crane (ASC) storage yards entirely, routing pre-cleared containers directly from Ship-to-Shore (STS) discharge to quayside on-dock rail buffers.

---

## Validated Corridor Benchmark (Maasvlakte II)

* **Baseline Scenario:** Legacy ASC Yard Stacking with post-discharge customs/EDI clearance.
* **ZeST Scenario:** T-5 Day eFTI Data Crystallization, Portbase Secure Chain token pre-authorization, and direct quayside rail buffering.
* **Test Consignment:** 1,500 containers (2,792 TEU / 31,192 metric tonnes) arriving via deep-sea vessel at Rotterdam Maasvlakte II.

| Metric | Legacy Terminal Baseline | ZeST Direct-to-Rail Buffer | Variance / Impact |
| :--- | :--- | :--- | :--- |
| **Terminal Rail Dwell** | **54.9 hours** | **4.4 hours** | **-92.0% (50.5h compressed)** |
| **Yard Re-Handles / Box** | **3.8 moves** | **0.0 moves** | **100% elimination of yard churn** |
| **Zone 1: STS to Buffer** | 32.4h (yard block hold) | **0.8h (direct AGV transit)** | Irreducible physical transfer |
| **Zone 2: Buffer to Rake** | 14.2h (crane reshuffle) | **2.1h (active rake load)** | Dynamic rake assembly |
| **Zone 3: Consignment / Exit** | 8.3h (paper check / gate) | **1.5h (eFTI token match)** | Immediate border & rail release |
| **Terminal Energy Intensity** | 42.1 kWh / container | **6.4 kWh / container** | -84.8% terminal crane energy |

---

## Visual Architecture & Transition Models

The architectural models comparing the legacy stack baseline against the ZeST quayside buffer pipeline are available in both raw Mermaid syntax and high-resolution standalone vector SVGs for offline inspection:

| Artifact | Source (`.mmd`) | Vector Export (`.svg`) | Description |
| :--- | :--- | :--- | :--- |
| **Physical vs. Data Flow** | `docs/diagrams/data_vs_physical_flow.mmd` | `docs/diagrams/exports/data_vs_physical_flow.svg` | Sequence flow decoupling eFTI data crystallization at $T-5$ days at sea from physical berth tie-up. |
| **Transition Architecture** | `docs/diagrams/transition_architecture.mmd` | `docs/diagrams/exports/transition_architecture.svg` | Stacked end-to-end pipeline: Legacy yard churn (54.9h) vs. ZeST zero re-handle rail bypass (4.4h). |

### Generating & Previewing Diagrams Locally

To re-render or preview the architecture diagrams without IDE plugins:

```bash
# Export standalone SVGs to docs/diagrams/exports/
python scripts/export_diagrams.py

# Generate a local standalone HTML preview and open in browser
python scripts/preview_diagrams.py
open docs/diagrams/preview.html
Repository Structure
Plaintext
zest-core/
├── app.py                           # Interactive Streamlit corridor & telemetry dashboard
├── docs/
│   ├── technical_abstract.md        # Technical methodology and academic reference
│   └── diagrams/
│       ├── data_vs_physical_flow.mmd    # Data sequence diagram
│       ├── transition_architecture.mmd  # Stacked transition architecture
│       ├── preview.html                 # Offline browser preview of visual assets
│       └── exports/                     # Standalone high-res vector SVGs
│           ├── data_vs_physical_flow.svg
│           └── transition_architecture.svg
├── schemas/
│   └── manifest_models.py           # Pydantic v2 schemas for eFTI manifests & tokens
├── scripts/
│   ├── demo_runner.py               # Headless CLI benchmark runner
│   ├── export_diagrams.py           # SVG export utility
│   └── preview_diagrams.py          # HTML preview generator
├── solvers/
│   ├── des/
│   │   └── milkrun_sim.py           # SimPy discrete-event terminal bypass simulation
│   └── generators/
│       └── manifest_gen.py          # Synthetic multi-corridor deep-sea manifest generator
├── tests/
│   └── test_benchmark.py           # Verification test suite (7/7 passing)
└── pyproject.toml
Quickstart
1. Environment Setup
Bash
# Clone the repository
git clone [https://github.com/open-zest/zest-core.git](https://github.com/open-zest/zest-core.git)
cd zest-core

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies in editable mode
pip install -e ".[dev]"
2. Run Verification Suite
Bash
pytest -v
3. Launch Interactive Dashboard
Bash
streamlit run app.py
Regulatory & Standards Alignment
EU Regulation 2020/1056 (eFTI): Electronic Freight Transport Information common dataset and certified platform interoperability.   
UNECE
Portbase Secure Chain: Pre-arrival digital token authentication replacing manual PIN-based gate and rail siding releases.
EU Regulation 2024/1679 (TEN-T Revision): 740m standard freight train lengths, P400 loading gauges, and corridor modal shift compliance on RFC North Sea–Mediterranean and RFC Rhine-Alpine.
License
This project is licensed under the MIT License — see the LICENSE file for details.
