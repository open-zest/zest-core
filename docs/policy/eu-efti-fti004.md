# Tuning the eFTI Registry of Identifiers (FTI004) for EU Intermodal Velocity

**Submitted to:** European Commission (DG MOVE) — *Have Your Say* Call for Evidence (November 2026)  
**Legal Basis:** Regulation (EU) 2020/1056 (eFTI) & Implementing Regulation (EU) 2024/1942  
**Author:** James P. Reefe, Lead Architect — Project ZeST (`open-zest/zest-core`)

---

## Executive Position

Enriching the eFTI registry of identifiers (**FTI004**) with takeover and delivery location metadata for road smart enforcement is a high-value step toward contactless verification ahead of the **9 July 2027** full application of Regulation (EU) 2020/1056.

However, indexing FTI004 exclusively around road vehicle registration numbers risks baking a **road-centric blind spot** into Europe’s digital freight backbone. In combined transport, a single ISO container or intermodal transport unit (ITU) moves across vessel, port terminal, rail wagon, and multiple drayage trucks. Adding four lightweight, **optional** intermodal fields while the **eFTI XML Schemas V1.0.0 Beta** remain open for amendment unlocks rail-port-road synchronization across the TEN-T network with zero additional burden on road-only SMEs.

---

## Proposed FTI004 Schema Extensions (Optional / Non-Breaking)

| Proposed FTI004 Field | Standard / Format | Gate Lookup Function | Intermodal Value Unlocked |
| :--- | :--- | :--- | :--- |
| `intermodalUnitId` | ISO 6346 (BIC) / EN 13044 (ILU) | Indexes the UIL by container/swap-body ID alongside truck plates. | Preserves continuous regulatory identity across maritime → rail → drayage transfers. |
| `transportModeChain` | UN/ECE Rec. 19 (`1, 2, 3, 8`) | Flags multimodal / Combined Transport operations at registry level. | Automated verification of Combined Transport road-leg exemptions without roadside stops. |
| `transferTerminalLocode` | UN/LOCODE (5-char + terminal) | Identifies the port or inland rail ramp where mode handoff occurs. | Correlates pre-arrival clearance with port and rail terminal windows. |
| `upstreamRefPointer` | DCSA 3.0 eBL / CIM-SMGS / MRN hash | Non-sensitive pointer linking maritime/customs pre-arrival data to the UIL. | Enables **Data-Precedes-Physical** release before vessel discharge or train assembly. |

---

## Case Study: Port of Constanța & the Black Sea / Orient–East-Med Corridor

The highest marginal return on an intermodal FTI004 registry lies at high-growth Eastern European gateways where physical rail infrastructure cannot expand fast enough to absorb geopolitical and Middle Corridor volume shifts:

* **Volume Surge:** As the largest port on the Black Sea, Constanța has absorbed record throughput (exceeding 92.5 million tonnes and 776,590 TEUs in recent peak years) across Black Sea transit, Middle Corridor flows, and the emerging Rail-2-Sea axis.
* **Physical Rail Constraints:** Across Romania’s CFR network, average freight train speeds have hovered near 15.9 km/h with extensive rolling-stock modernization still underway. Along the broader TEN-T Orient/East-Med corridor, roughly half of rail sections still restrict 740-meter freight trains and over 85% lack operational ETCS.
* **The "Warehouses on Wheels" Trap:** When consignment and regulatory data arrive fragmented—or physically with the carrier—containers dwell on port sidings awaiting manual clearance. Rail operators face strict slot restrictions to avoid turning trains into mobile storage, pushing missed rail volume onto congested road arteries.
* **The Digital Lever:** Registering container-level FTI004 pointers prior to vessel berthing (T-5 / pre-gate) allows Member State Gates to complete risk-targeting before discharge, enabling terminals to transfer cleared units directly from quay to rail without yard re-handling.

---

## Open-Source Simulation Evidence

Discrete-event terminal and rail-corridor simulations in [`open-zest/zest-core`](https://github.com/open-zest/zest-core) test *Data-Precedes-Physical* synchronization under realistic port-rail constraints:

* **57.39 h → 4.43 h** simulated mean container dwell (1,500-box corridor baseline vs. T-5 pre-arrival handshake).
* **0 yard re-handles** via zone-sequenced quay-to-rail transfer once clearance precedes physical discharge.
* **Vendor-neutral architecture** built in Python, Pydantic v2, and SimPy, aligned with DCSA 3.0 eBL and eFTI XML V1.0.0 Beta.
