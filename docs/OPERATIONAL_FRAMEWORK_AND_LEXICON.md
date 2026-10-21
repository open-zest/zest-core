# Project ZeST: Operational Framework, Phases & Core Lexicon

---

# Part I: The 6 Operational Phases of Project ZeST

[ Phase 1 ]  Contract-Inception Pre-Manifest & Federated Tokenization (eFTI CDS)
│
▼
[ Phase 2 ]  ZB-CSPP: Coarse Zone-Block Origin Vessel Stowage (IMO Intact GM)
│
▼
[ Phase 3 ]  Predictive Resource Orchestration & TEN-T Slot Reservation
│
▼
[ Phase 4 ]  Zero-Switching & Zero-Sort Terminal Operations (Direct Ramp-to-Rail)
│
▼
[ Phase 5 ]  Scheduled Linear Rail Conveyor & Siding Set-Out Milk Runs
│
▼
[ Phase 6 ]  Decoupled Micro-Layer Drayage & Dynamic Final-Mile Delivery

### Phase 1: Contract-Inception Pre-Manifest & Federated Tokenization
* **Factory Physics Analogy:** Electronic Kanbans generated at customer order release.
* **Timing:** $T - 45\text{ to } 14$ days (At cargo origin packing / loading in Asia).
* **Operational Mechanism:**
  * Leveraging the moment a shipping contract is let: destination addresses are locked at origin booking.
  * Proprietary shipping rates and BCO identities stay private inside carrier TMS/TOS.
  * Single-use cryptographic tokens (`[Container_ID, VGM_kg, Hazmat, Destination_Zone_Code, ETA_Window]`) are exposed via open **EU eFTI (2020/1056)** Common Data Set (CDS) APIs.
  * Uncleared non-Union goods are assigned **NCTS T1 bond status**, legally decoupling customs inspection from the seaport berth.
* **Module:** `schemas/manifest_models.py` & `schemas/openmanifest.v1.json`.

### Phase 2: ZB-CSPP — Coarse Zone-Block Origin Vessel Stowage
* **Factory Physics Analogy:** Group Technology & Pre-Sequenced Work-In-Progress (WIP) kitting.
* **Timing:** $T - 14$ days to vessel departure.
* **Operational Mechanism:**
  * Partitioning the vessel stowage plan into **4 to 6 coarse regional delivery blocks** matching the downstream TEN-T rail network.
  * Containers allocated into contiguous bays and vertical tiers strictly aligned with inland drop-off sequence.
  * Vertical Center-of-Gravity (VCG) heuristic ensures strict compliance with **IMO Intact Stability criteria** ($GM \ge 0.15\text{ m}$, trim, bending moments, and hull shear stress).
* **Module:** `solvers/zestow/zone_stow.py` & `solvers/zestow/stow_pipeline.py`.

### Phase 3: Predictive Just-In-Time (JIT) Resource Orchestration
* **Factory Physics Analogy:** Heijunka (load leveling) and takt-time line balancing.
* **Timing:** Ocean transit window ($T - 30\text{ to } 0$ days).
* **Operational Mechanism:**
  * During the 14-to-45-day ocean transit, aggregate arrival volumes per corridor zone are mathematically fixed.
  * European downstream operators perform advance resource reservation:
    * Quay cranes dedicated at gateway berths.
    * Rail flatcars positioned on on-dock tracks.
    * Mainline electric locomotives and **TEN-T timetable slots** locked in with national rail infrastructure managers (e.g., DB InfraGO, ProRail).
    * Eliminates both equipment starvation and expensive idle buffer capacity at the quay.

### Phase 4: Zero-Switching & Zero-Sort Terminal Operations
* **Factory Physics Analogy:** Single-Piece Continuous Flow (elimination of WIP buffer inventory).
* **Timing:** Gateway seaport arrival ($T = 0\text{ to } 12$ hours).
* **Operational Mechanism:**
  * **Direct Ramp-to-Rail:** Quay cranes discharge containers from pre-stowed zone blocks directly onto waiting on-dock rail wagons or transfer AGVs.
  * **Customs Offline Fall-out Bay:** Uncleared goods roll under NCTS T1 bond. Flagged containers are diverted offline to a separate inspection bay—never acting as an inline gate that blocks the STS crane or train departure.
  * **Outcome:** Terminal dwell collapses from **57.4 hours to 4.4 hours** (-92.3%), and yard digging drops from **1.46 re-handles/TEU to exactly 0.0**.
* **Module:** `solvers/des/dwell_sim.py`.

### Phase 5: Scheduled Linear Rail Conveyor & Siding Set-Out Milk Runs
* **Factory Physics Analogy:** Synchronous inter-facility transport conveyor.
* **Timing:** Inland transit along TEN-T corridors ($T + 3\text{ to } 24$ hours).
* **Operational Mechanism:**
  * Trains depart on scheduled timetable slots without waiting for massive 740-meter train classification ("The Train Length Fallacy").
  * Railcars are arranged in corridor drop-off order (e.g., Duisburg rear, Verona center, Poznań front).
  * **15-Minute Siding Drop-Off:** At each inland dry port, the train sets out rear wagons into an offline siding in 15 minutes, decoupling without yard humping or complex switching engines.
  * The mainline locomotive continues uninterrupted, clearing passenger rail corridors and cutting transit time into Poznań by **24.75 hours**.
* **Module:** `solvers/des/milkrun_sim.py`.

### Phase 6: Decoupled Micro-Layer Drayage & Dynamic Final-Mile Delivery
* **Factory Physics Analogy:** High-frequency, single-piece final delivery.
* **Timing:** Final 30-mile radius from inland dry port to consignee ($T + 24\text{ to } 48$ hours).
* **Operational Mechanism:**
  * Dry ports operate as **Packet Routers** at the network edge.
  * Over-The-Road (OTR) trucking is restricted to high-turnaround short-hauls (30-mile / 50-km radius around the dry port), eliminating multi-day highway driver exhaustion and emissions.
  * Dynamic dispatch accounts for live urban traffic, dock appointments, and receiver receiving hours.
  * Total container handling is reduced to **2 clean lifts** (Ship-to-Rail at gateway, Rail-to-Truck at dry port), collapsing the rail-vs-truck economic breakeven distance from **550 km down to 195 km**.

---

# Part II: Complete Master Lexicon of Project ZeST

### 1. Brand, Project & Architectural Paradigms
* **Project ZeST (Zero-Sort Transport):** Overarching operational architecture eliminating coastal terminal dwell by harmonizing origin vessel stowage with inland rail corridor topology.
* **Zero-Switching Terminal Operations:** Direct ramp-to-rail container transfers bypassing terminal classification yards, flat switching, and humping entirely.
* **The Transit Paradox:** Ultra-large vessels travel at 18–22 knots and unit trains sustain 60–80 km/h, yet freight dwells for 3 to 7 days in seaport storage yards.
* **The Information Inversion:** Cargo physically moving ahead of actionable digital data; manifest information arrives 12–72 hours *after* discharge despite being locked in at cargo packing 14–45 days earlier in Asia.
* **Packet-Switched Freight:** Translating TCP/IP networking to intermodal logistics—containers as data packets, TEN-T rail lines as fiber backbones, dry ports as coarse packet routers.
* **The ATM Federated Trust Architecture:** Decentralized governance where proprietary commercial data stays inside private carrier TMS/TOS, while single-use cryptographic tokens provide physical routing coordinates.
* **Step-Down Dynamic Transformer:** Buffering mechanism converting ocean mega-batches (15,000–24,000 TEUs) directly into scheduled rail medium-batches (80–100 TEUs) without terminal yard congestion.

### 2. The Three Core Lean Pillars
* **Pillar One — Contract-Inception Aggregate Journey Pre-Planning:** Pre-planning multimodal transit across the entire 15,000–24,000 TEU shipload simultaneously during the 14-to-45-day ocean voyage.
* **Pillar Two — Network-Defined Coarse Zone Stowage & Load/Unload Sequencing:** Using European rail delivery topology to define vessel stowage granularity into 4 to 6 coarse regional delivery blocks, while satisfying IMO Intact Stability criteria.
* **Pillar Three — Predictive Just-In-Time (JIT) Resource Allocation Planning:** Advance scheduling and positioning of quay cranes, flatcars, electric locomotives, TEN-T timetable slots, and drayage trucks during ocean transit.

### 3. Factory Physics & Flow Principles
* **The Train Length Fallacy (Batch Size vs. System Velocity):** Using static 740-meter train length as an efficiency proxy; mega-batches inflate dwell, destroy flow velocity, and compound mainline timetable risks.
* **Time as Lost Capital:** Grounding logistics efficiency in factory physics—stationary inventory lingering at docks represents non-recoverable capital loss and pure waste (*Muda*).
* **Manufacturing Quality "Fall-Out" Analogy:** Treating customs inspections like automotive assembly line rework: diverting flagged units to an offline rework bay under NCTS T1 bond so the primary ramp-to-rail conveyor never stalls.
* **Blind Batching:** Discharging mega-vessels in sequences optimized solely for quay crane moves, dumping containers randomly into congested storage yards.
* **Single-Piece Continuous Flow:** Slashing intermediate buffer stacks to achieve continuous velocity from the ship's hold directly onto waiting rail flatcars.
* **Zero Container Digging / Zero Re-handles:** Eliminating unproductive yard crane movements for buried container retrieval (reducing from 1.46 re-handles/TEU to exactly 0.0).
* **Aggregate Corridor Takt Velocity & Mean Flow Latency:** Primary objective functions replacing static train length and terminal crane moves per hour.

### 4. Mathematical & Queueing Formulations
* **Little's Law for Container Terminals ($\text{WIP} = \text{Throughput} \times \text{Cycle Time}$):** Demonstrating that driving destination dwell toward zero directly collapses yard Work-in-Progress (WIP) inventory proportionally without reducing throughput.
* **Kingman's Formula for Terminal Wait Times ($W_q \approx \left(\frac{\sigma_a^2 + \sigma_s^2}{2}\right) \left(\frac{\rho}{1 - \rho}\right) t_s$):** Proving why traditional terminals operating at high utilization ($\rho > 0.85$) with high service variance ($\sigma_s^2$) from stack digging suffer exponential queue explosions.
* **ZB-CSPP (Zone-Block Container Stowage Planning Problem):** Mathematical optimization balancing coarse destination zone bay-clustering against IMO intact stability limits.
* **Vertical Center-of-Gravity (VCG) Heuristic:** Rule-based stowage allocation placing heavier containers in lower hold tiers to preserve metacentric height while maintaining contiguous zone blocks.
* **IMO Intact Stability Threshold ($GM \ge 0.15\text{ m}$):** Statutory maritime stability constraint enforced across metacentric height ($GM$), trim, shear forces, and bending moments.

### 5. Corridor Topology & Rail Operations
* **Macro Layer (Linear Heavy Rail Conveyor Belt):** Deterministic, scheduled heavy-rail backbone moving large container blocks across regional distances.
* **Micro Layer (Distributed Local Drayage):** Decoupled short-haul trucking restricted to a 30-mile (50-km) radius around inland dry ports, operating as high-frequency single-piece flow.
* **Linear Corridor Milk-Run Train Operation:** Scheduled train service where railcars are arranged in corridor drop-off sequence (nearest dry port at the rear, farthest at the head).
* **15-Minute Offline Siding Set-Out:** Rapid mechanical decoupling of rear railcars into an inland dry port siding within 15 minutes, allowing the mainline train to proceed without crane unstacking or blocking passenger paths.
* **Over-Granularity Penalty:** Vessel instability, restow penalties, and loading complexity caused by attempting micro-sorting (e.g., individual ZIP code or specific customer warehouse) at origin.
* **Under-Granularity Penalty:** Seaport yard congestion and sorting chaos caused by macro-sorting that is too broad (e.g., stowing an entire continent into a single unsegregated block).
* **Two Clean Lifts:** Slashing total container handlings from 4–6 down to exactly 2: Ship-to-Rail at the gateway, and Rail-to-Truck at the inland dry port.
* **Collapsing the Rail-vs-Truck Breakeven:** Reducing the economic breakeven threshold between intermodal rail and direct trucking from 550 km down to 195 km.

### 6. Regulatory, Customs & European Policy Vocabularies
* **The EU 7-Year Budget Hard Window (Post-2027 MFF & CEF 3):** The decisive policy negotiation window for the Post-2027 Multiannual Financial Framework (MFF 2028–2034) and Connecting Europe Facility (CEF 3 Transport), preceded by the 2027 Annual EU Budget Conciliation in Nov–Dec 2026.
* **eFTI Common Data Set (CDS) Tokenization:** Compliance with EU Regulation 2020/1056 ahead of the mandatory July 9, 2027 compliance deadline, enabling certified digital freight exchange across all 27 EU Member States.
* **eFTI4EU Integration:** Direct interoperability with national eFTI implementations for electronic consignment notes (e-CMR) and rail consignment notes (CIM) without paper checks at borders.
* **Static B2A vs. Dynamic B2B Orchestration:** Elevating eFTI from a passive regulatory filing mechanism into an active operational coordination engine.
* **NCTS T1 In-Bond Rail Transit:** Deferring customs control to inland dry ports, allowing non-Union goods to transfer directly onto trains under T1 transit bonds without quay-side friction.
* **SOLAS VGM (Verified Gross Mass):** Chapter VI Regulation 2 compliance enforcing certified container gross mass boundaries (tare + payload) directly inside data tokens.
* **DTLF & EMDS Architecture:** Alignment with Digital Transport and Logistics Forum and European Mobility Data Space standards for federated data governance.
