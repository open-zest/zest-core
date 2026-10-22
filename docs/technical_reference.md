# Project ZeST: Technical Reference & Specification
**Repository:** `open-zest/zest-core` | **Python Baseline:** 3.11.13 | **Pytest:** 9.1.1

## 1. Architecture Overview
`zest-core` provides the core data schemas, synthetic manifest generation, deterministic benchmark evaluation, and discrete-event stochastic queuing models for zero-rehandle rail freight networks.

zest-core/
├── schemas/
│   └── manifest_models.py      # Pydantic v2 schemas: Manifest, Tokens, Zones, Ports
├── solvers/
│   ├── des/
│   │   └── milkrun_sim.py      # SimPy stochastic DES & deterministic corridor benchmark
│   └── generators/
│       └── manifest_gen.py     # Deterministic synthetic manifest generator (1,500 boxes)
├── scripts/
│   └── demo_runner.py          # Unified Rotterdam showcase runner script
└── tests/
├── test_benchmark.py       # Core stowage and baseline dwell assertions
├── test_corridor.py        # 6-zone corridor siding set-out benchmarks
├── test_manifest_generator.py # Manifest generation, TEU conversion, & zone allocation
└── test_simpy_queuing.py   # Stochastic crane contention and queuing delay tests

## 2. Core Modules & Engine Specifications

### 2.1 Pydantic Data Models (`schemas/manifest_models.py`)
* `CorridorManifest` / `VesselManifest`: Root container manifest supporting Pydantic computed properties (`total_teu`, `total_vgm_tonnes`, `total_payload_mass_tonnes`) and `zone_distribution_summary()`.
* `ContainerToken`: Container units bound with `customs_status` (`NCTS_T1_BOND`, `CUSTOMS_HOLD`), `destination_zone`, `cryptographic_token`, and tare-adjusted TEU ratings.
* `DestinationZoneCode`: Explicit six-corridor Dry Port registry:
  * `ZONE_A_DUISBURG` (Duisburg Hub)
  * `ZONE_B_VERONA` (Verona Quadrante)
  * `ZONE_C_POZNAN` (Poznań Franowo)
  * `ZONE_D_VIENNA` (Vienna Freudenau)
  * `ZONE_E_LYON` (Lyon Saint-Exupéry)
  * `ZONE_F_BUDAPEST` (Budapest BILK)

### 2.2 Discrete-Event Simulator (`solvers/des/milkrun_sim.py`)
* `StochasticMilkRunSimulator`: Built on `simpy.Environment`, modeling terminal crane resources (`simpy.Resource(capacity=zone.crane_capacity)`) per dry port siding.
* Dwell service times follow exponential handling distributions ($\lambda = 1 / 3.5\text{h}$) to evaluate true siding queue delays under peak contention.
* `execute_corridor_benchmark()`: Produces comparative corridor delivery profiles across all 6 destination dry ports.

## 3. Verification & Execution
To verify the full regression suite across all 7 unit and integration tests:

```bash
source .venv/bin/activate
pytest
To run the live Rotterdam corridor demonstration:
Bash
python scripts/demo_runner.py
