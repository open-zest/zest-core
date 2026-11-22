# Data-Precedes-Physical Architecture

European intermodal freight rarely fails because cranes are too slow; it fails because regulatory, customs, and commercial clearance arrives **after** the container hits the quay. Project ZeST reverses that sequence by decoupling digital verification from physical arrival.

## Core Design Principles

1. **T-5 Pre-Arrival Handshake:** Container-level identity, customs status, and eFTI Unique Identifying Links (UILs) are registered prior to vessel berthing or train assembly, enabling Member State Gates to complete risk-targeting before discharge.
2. **Equipment-Centric Identity:** Instead of tying compliance records solely to transient road vehicle license plates, ZeST anchors manifest state to the **ISO 6346 (BIC) / EN 13044 (ILU)** unit—preserving continuity across vessel, terminal, single-stack rail wagon, and drayage chassis.
3. **Zero Vendor Lock-In:** All schemas are implemented in open-source **Python and Pydantic v2** (`schemas/manifest_models.py`), aligning directly with **DCSA 3.0 eBL** and the public **eFTI XML Schemas V1.0.0 Beta**.

## End-to-End Token Handoff

| Stage | Timing | Data Trigger | Operational Outcome |
| :--- | :--- | :--- | :--- |
| **1. Pre-Arrival** | T-5 Days to T-24 Hours | DCSA 3.0 eBL + customs MRN linked to optional FTI004 `intermodalUnitId` & `upstreamRefPointer` | Authorities pre-clear low-risk cargo before vessel arrival. |
| **2. Zone-Block Stowage** | Vessel Approach | Terminal assigns discharge sequence by verified inland rail corridor | Cleared containers land in direct-transfer zones with **0 yard re-handles**. |
| **3. Rail Assembly** | Quay to Siding | Pre-cleared units load directly onto 740m European single-stack intermodal trains | Eliminates "warehouses on wheels" siding dwell and protects scarce TEN-T rail slots. |
| **4. Final Drayage** | Inland Ramp | FTI004 `transportModeChain` confirms Combined Transport leg eligibility | Contactless verification at port and road gates without stopping compliant trucks. |

## Reference Implementation

Source schemas and validation tests live in [`open-zest/zest-core`](https://github.com/open-zest/zest-core) (`schemas/` and `solvers/zone_stow.py`).

---

## Interactive Process Exhibit

* **[12-Swimlane End-to-End Process Evolution (PDCA Maturity Roadmap)](../exhibits/swimlane-process-evolution.html)** — Interactive 4-phase diagram comparing Legacy Baseline (750 km) through Full ZeST Origin Pre-Sorted Cut-Through (195 km) across Lean VSM, Cloud/SDN, and EU TEN-T views.

---

## Interactive Process Exhibit

* **[12-Swimlane End-to-End Process Evolution (PDCA Maturity Roadmap)](../exhibits/swimlane-process-evolution.html)** — Interactive 4-phase diagram comparing Legacy Baseline (750 km) through Full ZeST Origin Pre-Sorted Cut-Through (195 km) across Lean VSM, Cloud/SDN, and EU TEN-T views.

---

## Interactive Process Exhibit

* **[12-Swimlane End-to-End Process Evolution (PDCA Maturity Roadmap)](../exhibits/swimlane-process-evolution.html)** — Interactive 4-phase diagram comparing Legacy Baseline (750 km) through Full ZeST Origin Pre-Sorted Cut-Through (195 km) across Lean VSM, Cloud/SDN, and EU TEN-T views.
