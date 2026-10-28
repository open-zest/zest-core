# PR: Multi-Ship Port & Rail Container Transfer Dashboard & Schemas

## Summary
Implements the multi-ship quayside-to-rail transfer architecture for Project ZeST, targeting high-throughput ULCV calls (15,000–24,000 TEU aggregate manifests) and tracking eFTI regulatory data tokens across modal transition boundaries.

## Changes Included
1. **Relational Schemas (`schemas/sql/schema_port_rail_transfer.sql`)**:
   - `vessel_calls`: Manages berth schedules and ULCV manifest registrations.
   - `container_manifest`: Models ISO BIC units, VGM weights, hazard classes, and EU Reg 2020/1056 eFTI hashes.
   - `modal_transition_events`: Range-partitioned telemetry event ledger for quayside discharge, bypass loading, and dry-port siding drop-offs.
   - `rail_rake_consists` & `wagon_slot_assignments`: Tracks on-dock train rake capacity, wagon UIC slots, and axle loads.

2. **Analytical Performance Queries (`tools/dashboard/queries.sql`)**:
   - Quayside direct-rail bypass ratio and dwell latency analysis.
   - Downstream dry-port inbound pipeline metrics for RFC North Sea - Mediterranean / 3SI routes.

3. **Responsive Interface & Telemetry (`tools/dashboard/`)**:
   - `index.html`: Responsive Tailwind CSS interface visualizing quayside discharge, rail bypass pockets, dry-port sidings, and a real-time event stream.
   - `server.py`: FastAPI server streaming container telemetry over WebSockets and linking to the interactive NSRM corridor map (`tools/corridor_map/corridor_nsrm_map.html`).

## Testing & Verification
- Validated SQL schema syntax and partition boundaries.
- Tested FastAPI WebSocket stream on `http://localhost:8000`.
- Verified map linkage to `tools/corridor_map/build_map.py` outputs.
- Existing pytest suite passes clean (`pytest tests/`).

## Target Reviewers
- Technical Core Team (Open Logistics Foundation / ALICE)
- Intermodal Europe 2026 Showcase Lead
