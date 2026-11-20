# Discrete-Event Simulation Methodology (SimPy)

To quantify the operational impact of *Data-Precedes-Physical* manifest synchronization, Project ZeST models container movement from vessel discharge through yard staging to single-stack rail departure using **Python 3.11** and **SimPy**.

## Simulation Modules (`solvers/`)

* **`dwell_sim.py` (Terminal Dwell Model):** Simulates container arrival, customs/regulatory clearance latency, yard stacking, and release gating under both legacy arrival-triggered clearance and T-5 pre-arrival handshakes.
* **`zone_stow.py` (Zone-Block Stowage Heuristic):** Models vessel bay/zone grouping so pre-cleared containers discharge in rail-corridor sequence, eliminating unproductive yard shuffles.
* **`milkrun_sim.py` (Inland Rail Milk-Run Model):** Models European single-stack intermodal rail departures, siding capacity, and the downstream cascade when missed customs clearance causes a container to miss its assigned rail slot.

## Benchmark Results (1,500-Box Corridor Baseline)

| Metric | Legacy Arrival-Triggered Flow | ZeST Pre-Arrival (T-5 Handshake) | Operational Impact |
| :--- | :--- | :--- | :--- |
| **Mean Container Dwell** | **57.39 hours** | **4.43 hours** | **92.3% reduction** in terminal dwell |
| **Unproductive Yard Re-Handles** | High (reactive dig-outs) | **0 re-handles** | Direct quay-to-rail transfer for pre-cleared zones |
| **10% Port Capacity Deficit Stress Test** | Queues compound exponentially; rail slots missed | Throughput preserved via pre-sequenced release | Recovers effective capacity without civil works |

## Reproducing the Benchmarks

All simulations are deterministic, unit-tested, and open source:

```bash
# Run validation tests
pytest

# Launch the interactive Streamlit digital twin
streamlit run app.py
