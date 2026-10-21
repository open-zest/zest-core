# Open-ZeST: Technical Architecture & Discrete-Event Benchmark Summary
**Reference Architecture:** Open Zero-Sorting Terminal (ZeST) Core Engine  
**Module:** `solvers/des/milkrun_sim.py` | `solvers/zestow/zone_stow.py`  
**License:** MIT

---

### Abstract
Inland intermodal rail freight terminals frequently act as in-process sorting buffers due to container arrival entropy and decoupling from maritime vessel stowage sequences. Traditional operations incur severe dwell penalties and multiple yard rehandles while assembling multi-destination trains. 

The Open-ZeST framework models a dynamic pull-staging architecture using discrete-event simulation (SimPy). By shifting grouping logic to dynamic transfer buffers and synchronized rail milk-runs, the system decouples port-rail throughput from carrier pre-stowage dependencies. Even under data-asymmetric arrival profiles (manifest ingestion at pilot boarding or post-cast-off), the architecture eliminates terminal sorting bottlenecks.

---

### Baseline vs. ZeST Benchmark Results
Simulated across a calibrated multi-zone European rail corridor comprising **1,500 containers** (2,840.0 TEU, 31,192.68 metric tonnes) routing across six corridor destination zones (Duisburg, Verona, Poznań, Vienna, Lyon, Budapest):

| Performance Metric | Traditional Multi-Zone Yard Baseline | Open-ZeST Dynamic Staging | Variance (%) |
| :--- | :--- | :--- | :--- |
| **Mean Dwell Time** | 57.39 hours | **4.43 hours** | **-92.28%** |
| **95th Percentile (p95) Dwell** | 170.72 hours | **6.86 hours** | **-95.98%** |
| **Terminal Rehandles per Container** | 1.46 | **0.00** | **-100.00%** |
| **Staging Ingestion Prerequisite** | Carrier Pre-Sort Required | Manifest Ingestion (Real-Time) | Decoupled |

---

### Mathematical & Simulation Formulation
* **Manifest Schemas:** Strongly-typed Pydantic v2 schemas (`schemas/manifest_models.py`) enforcing ISO 6346 validation, verified gross mass (`vgm_kg`), ADR/IMDG hazard classifications, and multi-node delivery routing.
* **Corridor Topologies:** Discrete-event resource queues modeling dual-spreader rail-mounted gantry (RMG) cycling, buffer yard staging tracks, and scheduled milk-run departures.
* **Verification:** Fully reproducible test suite executed via `pytest tests/test_benchmark.py`.
