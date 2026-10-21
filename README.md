# Project ZeST: Zero-Sort Transport
### Next-Generation Intermodal Freight via the Physical Internet & Packet-Switched Logistics

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/pytest-4%20passed-brightgreen.svg)]()
[![Standard](https://img.shields.io/badge/eFTI-EU%202020%2F1056-orange.svg)]()
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Project ZeST (Zero-Sort Transport) introduces an operational paradigm shift that eliminates seaport container terminal dwell time by harmonizing origin vessel stowage, rail corridor topology, and predictive data pipelines.

Anchored for demonstration at **Intermodal Europe 2026** (Rotterdam, Nov 10–12, 2026) and aligned with the **Post-2027 EU Multiannual Financial Framework (MFF 2028–2034)** and **CEF 3 Transport** funding windows.

---

## 1. Core Architecture: The Packet-Switched Freight Analogy

ZeST translates fundamental principles of digital packet-switching network design into physical freight networks:

| Digital Network Component | Physical Logistics Equivalent | ZeST Operational Role |
| :--- | :--- | :--- |
| **IP Data Packet** | ISO Intermodal Container (TEU) | Standardized payload unit routed via cryptographic token |
| **Header Routing Flags** | eFTI Token / Destination Zone | Minimal dispatch metadata exposed (`[Zone, VGM, T1 Bond]`) |
| **Fiber Backbone** | TEN-T Rail Corridors | Linear macro heavy-rail conveyor bypassing road congestion |
| **Edge Router** | Inland Dry Port (e.g. Duisburg) | Coarse packet router executing 15-min drop-offs without crane digging |
| **Local Device Delivery** | Micro-Layer Drayage Truck | High-frequency single-piece flow within a 30-mile radius |

---

## 2. Factory Physics & Flow Principles

Current maritime ports commit a structural error by treating customs clearance and random container yard stacking as inline blocking gates at the quay. ZeST applies mass-production flow controls:

* **Little's Law ($\text{WIP} = \text{Throughput} \times \text{Cycle Time}$):** Origin pre-sorting drops coastal yard dwell toward zero, drastically lowering Work-in-Progress (WIP) inventory while preserving peak throughput.
* **Kingman's Queueing Formula ($W_q \propto \frac{\rho}{1-\rho} \cdot \frac{\sigma_a^2 + \sigma_s^2}{2}$):** Removing random yard stacking sets service time $t_s \to 0$ for terminal digs and slashes variance ($\sigma_s^2$), preventing exponential queue explosions.
* **The Train Length Fallacy:** Moving away from static mega-batches (waiting hours for a 740m train to fully marshal) in favor of deterministic takt velocity on scheduled corridor slots.
* **Customs Fall-Out Bay:** NCTS T1 in-bond transit moves customs processing to inland dry ports, routing physical inspections offline to prevent mainline conveyor stalls.

---

## 3. Verified Benchmark Results

### A. Seaport Terminal Dwell & Crane Handling (`solvers/des/dwell_sim.py`)

| Metric | Traditional Operation | Project ZeST | Impact |
| :--- | :--- | :--- | :--- |
| **Mean Terminal Dwell** | **57.39 hours** | **4.43 hours** | **-92.3%** |
| **p95 Terminal Dwell** | 170.72 hours | 6.86 hours | **-96.0%** |
| **Yard Re-handles / TEU** | 1.46 re-handles | **0.00 re-handles** | **-100% (Zero Digs)** |
| **Rail Breakeven Distance** | 550 km | 195 km | **-64.5%** |

### B. Macro Corridor Rail Milk-Run Simulation (`solvers/des/milkrun_sim.py`)

Simulation of direct ramp-to-rail train dispatch from Rotterdam along the TEN-T corridor with 15-minute offline siding set-outs vs. traditional classification yard humping and re-marshalling:

| Corridor Dry Port | Zone Code | ZeST Arrival | Traditional Arrival | Transit Reduction |
| :--- | :--- | :--- | :--- | :--- |
| **Duisburg Intermodal** | `ZONE_A_DUI` | **3.05 h** | 11.30 h | **-8.25 h** |
| **Verona Quadrante Europa** | `ZONE_B_VRN` | **14.50 h** | 31.00 h | **-16.50 h** |
| **Poznan Franowo** | `ZONE_C_POZ` | **16.48 h** | 41.23 h | **-24.75 h** |

---

## 4. Repository Structure

open-zest/zest-core/
├── schemas/
│   ├── openmanifest.v1.json      # eFTI CDS-compliant JSON schema (SOLAS VGM, UCC T1)
│   └── manifest_models.py        # Strict Pydantic v2 data models & token validation
├── solvers/
│   ├── zestow/
│   │   └── zone_stow.py          # ZB-CSPP 6-zone vessel stowage optimizer (IMO Intact GM)
│   └── des/
│       ├── dwell_sim.py          # SimPy terminal dwell discrete-event simulation
│       └── milkrun_sim.py        # SimPy corridor rail milk-run & siding set-out simulation
├── tests/
│   ├── test_benchmark.py         # Regression tests for terminal dwell & stowage
│   └── test_corridor.py          # Regression tests for corridor linear rail conveyor
├── requirements.txt
└── README.md

---

## 5. Quickstart & Benchmark Reproduction

### Prerequisites
* Python 3.11+
* Virtual environment (`.venv`)

### Installation
```bash
git clone [https://github.com/open-zest/zest-core.git](https://github.com/open-zest/zest-core.git)
cd zest-core
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Reproduce Benchmarks
Run the full test suite (4/4 automated regression checks):
Bash
pytest -v
Execute individual simulation engines:
Bash
# Terminal Dwell & Re-handle Benchmark
python3 solvers/des/dwell_sim.py

# Macro Corridor Rail Milk-Run Benchmark
python3 solvers/des/milkrun_sim.py

# Zone-Block Vessel Stowage Optimizer
python3 solvers/zestow/zone_stow.py
6. Regulatory & Standards Alignment
EU Regulation 2020/1056 (eFTI): Common Data Set (CDS) digital freight interface compliance ahead of the mandatory July 9, 2027 deadline.
IMO Intact Stability: Strict adherence to SOLAS Chapter VI Reg 2 Verified Gross Mass (VGM) and minimum metacentric height (GM≥0.15 m).
Union Customs Code (UCC): NCTS T1 bond customs transit deferral for non-Union goods directly onto rail conveyors.
