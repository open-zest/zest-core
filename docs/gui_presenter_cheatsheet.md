# Project ZeST — 1-Page Executive GUI Presenter Cheat Sheet
**Intermodal Europe 2026 (Rotterdam) • Master Telemetry & Architecture Launcher**

---

## 1. Quick Launch & Server Command
```bash
source .venv/bin/activate
uvicorn tools.dashboard.server:app --host 127.0.0.1 --port 8050 --reload
```
- **Main Dashboard:** `[http://127.0.0.1:8050/](http://127.0.0.1:8050/)`
- **Header Quick-Launch Tabs (Open in New Tab):**
  - `🗺️ EU Map` (`/map`) — Pan-EU / UK (to Scotland) / IT (to Palermo) + 3SI Catchment Zones (`ZONE_A`–`ZONE_F`)
  - `🏊 3-in-1 Swimlane` (`/swimlane`) — Switchable **Panasonic VSM**, **Google SDN**, and **EU TEN-T** storyboards
  - `⚙️ Process Flow` (`/process`) — 3-part Dual-Stream Block Diagrams (End-to-End, Seaport Ingress, Dry-Port Egress)
  - `⚓ ΔGM Proof` (`/hydrostatics`) — 4th-Tensor Origin-Port Stowage Brief (ΔGM = ±1.32 cm stability proof)
  - `📋 Cheat Sheet` (`/cheatsheet`) — Printable HTML version of this 1-page guide

---

## 2. The 90-Second Demo Choreography (5 Clicks)

| Step | Control to Click / Drag | What Changes on Screen | Core Talking Point |
| :--- | :--- | :--- | :--- |
| **1. Baseline Contrast** | **View Switcher** (Top Right): Click `Stacked View` ➔ `Legacy Only` ➔ `ZeST Only` | Toggles the **Red Legacy Bufferbloat** panel (84.5% yard stack, 1.65 digs/box) vs. **Green ZeST Cut-Through Switch** (0.31h quayside, 0.00 digs). | *"Legacy ports store containers in 5-high concrete stacks because customs & rail pins arrive late—that's router bufferbloat. ZeST resolves the eFTI header 5 days out at sea so the crane drops straight onto the AGV-to-rail loop."* |
| **2. The Day-1 Rollout Proof** | **Partial eFTI Slider (α_eFTI)**: Click `0% Legacy` ➔ `25% Pilot` ➔ `50% Hybrid` ➔ `100% Full SDN` | Watch **Pillar 3 (Offshore Queue Collapse)** jump non-linearly and the bottom **Live Packet Table** split between green (`CUT_THROUGH_AGV`) and amber (`FALLBACK_STACK`). | *"You don't need 100% industry adoption on Day 1. Because port queuing is hyperbolic (M/Ek/c), **just 50% Partial eFTI adoption collapses Maascenter offshore anchorage waiting time by 47.1%** (saving 46.5 fleet hours per wave)."* |
| **3. Ship-to-Berth Drilldown** | **Section 1 Vessel Strip**: Click `BERTH_Q01 (MSC AMELIA)` or `BERTH_Q04 (EVER ALOT T-120h)` | Outlines the vessel card in cyan and filters the **Live Packet Table** solely to that vessel's containers. | *"While EVER ALOT is still 120 hours out approaching Suez, 98.4% of its eFTI headers and UIC wagon slots are already locked. At berth, gross vessel turnaround drops **28.7% (54.0h ➔ 38.5h)**."* |
| **4. 740m Takt Rail Consist** | **Section 4 Left (`ON-DOCK RAIL SIDINGS`)**: Click `TRK-04 (Target: ZONE_C_POZ)` | Filters packet stream to Track 04 (36 UIC wagons, 740m rake) showing **96.8% MINLP fill** vs. 71.0% legacy fill. | *"Because VGM weights are known at T-5 days, our MINLP solver packs 740m rakes to 96.8% axle capacity without a single yard re-handle, departing on passenger-grade Takt slots."* |
| **5. East-West EU Parity & Air Pullback** | **Section 4 Right (`CATCHMENT ZONES`)**: Click `ZONE_B_VRN (Venlo 195km)` or `ZONE_F_BUD (Curtici)` | Filters packets by hinterland hub; highlights **15-min siding set-outs** and **Air Diverted Tonnes**. Click `Reset Filter` when done. | *"Eliminating the €250–€400 port re-handling tax collapses rail break-even from **540 km to 195 km**, and cutting transit variance from σ=±6.8d to **σ less than 24h** pulls $4.50/kg air cargo back onto $0.25/kg rail."* |

---

## 3. Stakeholder-Specific Pivot Guide (Who Cares About What)

- **Portbase / Port of Rotterdam (Iwan Vanderwolf) & Smartport (Sophie Broere):**
  - **Focus:** Section 1 **Partial eFTI Slider (α_eFTI)** + Pillar 2 (**Gross Berth Time -28.7%**) + Pillar 3 (**-71.1% Anchorage Queue Collapse**).
  - **Key Hook:** Zero concrete capex—28% virtual quay wall expansion and elimination of AGV starvation (15.4% ➔ 1.1%) purely by binding Portbase Secure Chain / eFTI tokens at T-120h.
- **Fraunhofer IML (Clausen, Prasse, Wolf, Leveling) & ALICE:**
  - **Focus:** Click `🏊 3-in-1 Swimlane` (toggle *Panasonic VSM* vs. *Google SDN*) + `⚙️ Process Flow` + Section 4 **MINLP 740m Rake Utilization (96.8%)**.
  - **Key Hook:** Physical Internet packet switching—replacing 24h hump-yard classification with origin-port 4th-tensor block stowage and 15-minute dry-port siding set-outs.
- **Google Cloud / OSPO (Hans Thalbauer):**
  - **Focus:** Stacked SDN Data Plane view + Live Cryptographic Header Table (`0x9f...` eFTI hash) + `🏊 3-in-1 Swimlane` (*Google SDN Lens*).
  - **Key Hook:** The seaport is a Layer-2 packet switch suffering from bufferbloat; `openmanifest.v1` separates the T-5 Control Plane from the T=0 Physical Forwarding Plane.
- **EU DG MOVE / TRAN Committee MEPs (CEF III / 3SI Corridor Parity):**
  - **Focus:** Click `🗺️ EU Map` + Section 4 Catchment Zones (`ZONE_C_POZ` Poznań/Sławków, `ZONE_D_VIE` Prague, `ZONE_F_BUD` Budapest/Curtici).
  - **Key Hook:** Western & Eastern EU parity—extending Rotterdam's zero-dwell advantage across RFC 1, RFC 8, and Three Seas Initiative (3SI) hubs while cutting CO₂ by 97% vs. air freight.
- **Ocean Carriers / Naval Architects / Terminal Planners:**
  - **Focus:** Click `⚓ ΔGM Proof` (`/hydrostatics`).
  - **Key Hook:** Adding the 4th Tensor (Destination Rail Zone Zr) at the Asian origin port causes only **ΔGM = ±1.32 cm** (well inside the ±5.0 cm noise floor) with zero restows and 96.4% shear-force margin.
