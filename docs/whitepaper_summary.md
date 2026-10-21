# Open-ZeST: Eliminating Inland Intermodal Friction
### Open-Source Discrete-Event Simulation & Dynamic Staging Architecture

#### The Problem
European intermodal rail is throttled by in-process yard sorting. Ocean carriers treat stowage as an isolated maritime problem, forcing inland rail terminals to operate as massive, slow sorting buffers. Traditional multi-zone corridor operations suffer average dwell times exceeding **57.4 hours** and an average of **1.46 crane rehandles per container**, turning intermodal terminals into bottlenecks.

#### The Core Technical Finding
**Carrier pre-sorting is not required to achieve zero-rehandle rail dispatch.** 
Even when manifests arrive mid-voyage or upon pilot boarding, dynamic zone-based pull staging (`solvers/zestow`) decouples terminal dispatch from maritime stows. By shifting sorting logic to dynamic buffering at inland transfer nodes (rail milk-runs), inland rail corridors achieve continuous flow.

#### Benchmark Verification
Simulated across a calibrated mixed corridor (1,500 containers, 2,840.0 TEU, 31,192.68 metric tonnes) distributing across Zone A (Duisburg), Zone B (Verona), Zone C (Poznań), Zone D (Vienna), Zone E (Lyon), and Zone F (Budapest):

| Operational Metric | Traditional Baseline | Open-ZeST Framework | Net Improvement |
| :--- | :--- | :--- | :--- |
| **Mean Dwell Time** | 57.39 hours | **4.43 hours** | **-92.3%** |
| **p95 Dwell Time** | 170.72 hours | **6.86 hours** | **-96.0%** |
| **Average Rehandles** | 1.46 per box | **0.00** | **100% eliminated** |
| **Data Prerequisite** | Full Pre-Sort Required | None (Dynamic Intake) | Decoupled |

#### Pan-European Cohesion & Strategic Autonomy
- **Leveling the Periphery:** High-speed intermodal velocity cannot be restricted to the Rhine-Alpine corridor. Legacy yards across the Baltics, Visegrád Four, Romania/Black Sea, and Greece cannot wait decades for multi-billion-euro concrete rebuilds. Algorithmic dispatch provides an immediate software-driven upgrade path.
- **Dual-Use Resilience:** Sub-5-hour rail turnaround directly reinforces European defense logistics and supply chain autonomy across the Baltic-Black-Aegean corridors.
