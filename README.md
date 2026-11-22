# Project ZeST (`zest-core`)

**Open-source architecture and discrete-event simulation for European & UK intermodal freight velocity.**

Project ZeST (*Zero-Sort Transport*) demonstrates how **Data-Precedes-Physical** manifest synchronization—anchored to **EU eFTI (Regulation 2020/1056)**, **DCSA 3.0 eBL**, and **UCC NCTS T1** transit bonds—eliminates coastal port yard dwell, prevents crane re-handling, and unlocks inland rail capacity across TEN-T and UK corridors without waiting a decade for new concrete.

* **Live Site & Documentation:** [https://open-zest.web.app](https://open-zest.web.app)
* **License:** Apache 2.0 (Vendor-Neutral Reference Implementation)
* **Lead Architect:** James P. Reefe

---

## Live Pillars on `open-zest.web.app`

* **Series 1 — Europe's Intermodal Reset:** [open-zest.web.app/series](https://open-zest.web.app/series/)
  * *Part 1:* Load-Balancing Europe's Intermodal Seaports as Virtual Capacity
  * *Part 2:* The Suez-to-Gibraltar Arc — Voyage Velocity Over Mega-Vessel Size
* **Corridor Reference Map:** [open-zest.web.app/maps/corridor-reference-map](https://open-zest.web.app/maps/corridor-reference-map/)
* **EU Policy & eFTI FTI004 Annex:** [open-zest.web.app/policy/eu-efti-fti004](https://open-zest.web.app/policy/eu-efti-fti004/)
* **System Architecture:** [open-zest.web.app/architecture/data-precedes-physical](https://open-zest.web.app/architecture/data-precedes-physical/)
* **Interactive Process Exhibit (12-Swimlane PDCA):** [open-zest.web.app/exhibits/swimlane-process-evolution.html](https://open-zest.web.app/exhibits/swimlane-process-evolution.html)
* **Simulation Methodology:** [open-zest.web.app/methodology/discrete-event-simulation](https://open-zest.web.app/methodology/discrete-event-simulation/)

---

## Core Simulation Benchmarks

| Metric | Legacy Blind Batching (Post-Berth EDI) | ZeST T-5 Pre-Cleared Cut-Through | Delta |
| :--- | :--- | :--- | :--- |
| **Mean Coastal Container Dwell** | ~57.0 hours | ~4.5 hours | **-92.1%** |
| **Yard Crane Re-Handles / TEU** | 2–5 digs | 0 (Direct Quay-to-Rail) | **-100%** |
| **Rail vs. Truck Breakeven** | ~550 km | ~195 km | **-64.5%** |

---

## Local Quickstart

```bash
# 1. Run the test suite
pytest -v

# 2. Preview documentation locally (includes docs/drafts/)
mkdocs serve

# 3. Validate production build (strict mode)
mkdocs build --strict
Repository Structure
solvers/ — SimPy discrete-event terminal/rail simulations and zone-block stowage heuristics
schemas/ — Pydantic v2 eFTI (FTI004) and pre-arrival manifest models
scripts/ — Corridor benchmark runners and diagram generators
tests/ — Automated verification suite for schemas, vessel stability, and SimPy dwell models
docs/ — MkDocs Material source for open-zest.web.app
