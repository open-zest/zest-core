# Project ZeST (`zest-core`) — Zero-Sort Transport

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Docs: Live Site](https://img.shields.io/badge/Docs-open--zest.web.app-indigo.svg)](https://open-zest.web.app)
[![Release: v0.6.0-continental-parity](https://img.shields.io/badge/Release-v0.6.0--continental--parity-emerald.svg)](https://github.com/open-zest/zest-core/releases)
[![Standard: EU eFTI 2020/1056](https://img.shields.io/badge/Standard-EU_eFTI_2020%2F1056-sky.svg)](https://open-zest.web.app)

> **Sequenced Loads Eliminate the Need for In-Process Sort.**

Project ZeST (**Open ZeST**) is an open-source systems architecture and discrete-event simulation framework for European intermodal freight.

By resolving **eBL** and **EU eFTI (Reg 2020/1056)** clearance tokens **5 to 10 days before vessel arrival**—paired with destination-zone stowage at the outbound port—containers move from the outbound seaport yard to final European delivery in **three lifts** with direct ship-to-rail transfer and zero inbound yard stacking.

---

## Documentation & Field Guides

Full narrative briefs, corridor maps, process architecture, and methodology are published on the live documentation site:

👉 **[Project ZeST Documentation (`https://open-zest.web.app`)](https://open-zest.web.app)**

---

## Reference Benchmark Summary

Validated on a 1,500-container ULCV call baseline (Maasvlakte II) and modeled across Europe's **11 primary seaport clusters**—from Rotterdam and Antwerp-Bruges to Valencia, La Spezia, Piraeus, and Gdańsk:

| Operational Metric | Legacy Terminal Baseline | Project ZeST (100% Pre-Cleared) | Day-1 Hybrid (50% eFTI) | Strategic Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Pre-Arrival Data Lock** | `T+0h` to `T+48h` (post-berth) | **`T-120h` to `T-240h` (at sea)** | `50%` Pre-Cleared / `50%` Stack | Separates customs & release paperwork from physical iron |
| **Quayside-to-Rail Transfer** | `6.80 hours` | **`0.31 hours` (18.6 min)** | `3.56 hours` (Blended) | Direct STS crane to on-dock 740m rail siding |
| **Mean Terminal Turnaround** | `57.39 hours` | **`4.43 hours` (-92.3%)** | `30.91 hours` (-46.1%) | Eliminates yard stacking delays across regional gateways |
| **Unproductive Yard Re-Handles** | `1.65 digs/box` | **`0.00 digs/box`** | `0.83 digs/box` | Saves **€785,000** in wasted crane moves per ULCV call |
| **Gross Vessel Berth Time** | `54.0 hours` | **`38.5 hours` (-28.7%)** | `46.3 hours` (-14.4%) | Unlocks virtual quay capacity without new concrete |
| **Offshore Queue Wait (`M/Ek/c`)** | `ρ = 0.86` | **`ρ = 0.64` (-71.1% wait)** | **`ρ = 0.75` (-47.1% wait)** | Non-linear congestion relief even at 50% adoption |
| **Rail-vs-Truck Break-Even** | `520 km` | **`195 km`** | `368 km` | Makes regional short-haul rail competitive across TEN-T corridors |
| **Corridor Transit Variance (`σ`)** | `±6.8 days` | **`±0.35 days` (<24h SLA)** | `±3.58 days` | Delivers air-freight reliability at rail cost |
| **Zone-Sequenced Stowage** | Standard (`B, R, T`) | **Zone-Aware (`B, R, T, Zr`)** | Compatible | **`ΔGM = ±1.32 cm`** (within sensor noise floor; 0 restows) |

---

## Repository Structure

```text
zest-core/
├── docs/                  # Live MkDocs Material source published to open-zest.web.app
├── schemas/               # eFTI/openmanifest v1 JSON schemas, Pydantic v2 models & corridor topology
├── solvers/               # SimPy discrete-event queuing, rail milk-run & zone stowage solvers
├── scripts/               # CLI benchmark runner (demo_runner.py) & exhibit generators
├── tools/dashboard/       # FastAPI + WebSocket real-time telemetry server & UI
├── protos/                # Protocol buffer definitions
└── tests/                 # Automated pytest verification suite
Quick Start
1. Install Dependencies
Bash
pip install -r requirements.txt
2. Run the CLI Benchmark Simulation
Bash
python scripts/demo_runner.py
3. Launch the Live Telemetry Dashboard
Bash
uvicorn tools.dashboard.server:app --host 127.0.0.1 --port 8050 --reload
Open http://127.0.0.1:8050/ in your browser to inspect real-time ship-to-rail transfers and test partial eFTI adoption rates (0% to 100%).
4. Run the Automated Test Suite
Bash
pytest -v
License
Licensed under the Apache License, Version 2.0. See LICENSE for details.
