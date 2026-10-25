# Project ZeST (Zero-Sort Transport)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Architecture: Event-Driven eFTI](https://img.shields.io/badge/eFTI-EU%202020%2F1056-green.svg)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32020R1056)

**Project ZeST** applies lean mass-production manufacturing controls and event-driven data orchestration to global intermodal logistics. By recognizing that **data flow must precede physical container flow**, ZeST resolves the rate-limiting step of freight interchange: structural asynchronous data latency.

Traditional port terminal operating systems (TOS) operate under a reactive polling model where manifest and customs data lag physical vessel berthing by 12 to 48 hours ($t+48\text{h}$). This information lag forces inbound containers into high-density storage buffer yards, requiring 1.4 to 1.6 unproductive digging re-handles per box and inflating terminal dwell to 55+ hours.

ZeST replaces this queue-inducing state lag with **Feed-Forward Determinism**: single-use cryptographic routing tokens emitted at origin contract let ($t-14\text{d}$) orchestrate direct ramp-to-rail transfers, collapsing terminal dwell to **4.43 hours** with **zero yard digging**.

---

## The Operational IT Lingo Map

To bridge maritime operations with enterprise distributed systems, ZeST maps physical terminal concepts directly to standard IT systems architecture:

| Operational Maritime Concept | IT Architecture & Systems Equivalent | Technical Mechanism & System Impact |
| :--- | :--- | :--- |
| **Intermodal ISO Container** | **Packet Payload** | Physical encapsulated unit carrying state, Verified Gross Mass (VGM), and routing metadata. |
| **Terminal Yard Buffer** | **Unindexed Memory Thrashing** | High-cost temporary storage allocation caused by missing routing index keys at runtime. |
| **Direct Ramp-to-Rail Transfer** | **Zero-Copy Stream Transfer** | Direct hardware pipeline execution bypassing intermediate caching or re-buffering steps. |
| **Customs Inspection Hold** | **Dead-Letter Queue (DLQ)** | Out-of-band exception routing under NCTS T1 bond, preventing mainline pipeline stalls. |
| **Port Community System (Portbase)** | **Message Broker / Service Bus** | Asynchronous integration fabric coordinating multi-party event streams. |

---

## eFTI Single-Use Token Specification (EU 2020/1056)

ZeST utilizes the **ATM Federated Trust Model** to guarantee commercial confidentiality. Freight rates, client identities, and profit margins never leave private carrier databases. Downstream terminal operating systems and rail dispatchers receive only non-commercial cryptographic routing tokens:

```json
{
  "$schema": "[https://json-schema.org/draft/2020-12/schema](https://json-schema.org/draft/2020-12/schema)",
  "title": "eFTISingleUseRoutingToken",
  "type": "object",
  "properties": {
    "container_id": {
      "type": "string",
      "pattern": "^[A-Z]{4}[0-9]{7}$",
      "description": "Standard BIC code format (e.g., MSKU1234567)"
    },
    "iso_type": {
      "type": "string",
      "pattern": "^[A-Z0-9]{4}$",
      "description": "ISO 6346 size and type code (e.g., 45G1)"
    },
    "vgm_kg": {
      "type": "integer",
      "minimum": 2000,
      "maximum": 35000,
      "description": "Verified Gross Mass in kilograms"
    },
    "zone_token": {
      "type": "string",
      "description": "Coarse corridor zone destination (ZONE_A_DUI through ZONE_F_BUD)"
    },
    "hazmat_class": {
      "type": "string",
      "nullable": true,
      "description": "IMDG hazard class classification"
    },
    "customs_ncts_status": {
      "type": "string",
      "enum": ["CLEARED_T1", "PENDING_INSPECTION", "EXEMPT", "DLQ_HOLD"],
      "description": "NCTS transit protocol state"
    },
    "departure_ts": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 UTC timestamp of origin departure"
    },
    "pre_clearance_hash": {
      "type": "string",
      "pattern": "^0x[a-fA-F0-9]{64}$",
      "description": "SHA-256 Zero-Knowledge proof of regulatory compliance"
    }
  },
  "required": [
    "container_id",
    "iso_type",
    "vgm_kg",
    "zone_token",
    "customs_ncts_status",
    "departure_ts",
    "pre_clearance_hash"
  ]
}
Discrete-Event Simulation Benchmarks
Validated using the open-source discrete-event simulation engine across 1,500 containers over the Port of Rotterdam (Maasvlakte II) to RFC North Sea–Mediterranean corridor:
========================================================================
PROJECT ZeST: DATA LATENCY BENCHMARK RESULTS (1,500 TEU CORRIDOR)
========================================================================
Legacy (t+48h Data Lag):   Mean Dwell: 54.9h | p95 Tail: 62.11h | Re-handles: 1.62 moves/box
ZeST (t-14d Feed-Forward): Mean Dwell: 4.43h | p95 Tail:  6.86h | Re-handles: 0.00 moves/box
------------------------------------------------------------------------
Performance Impact:        91.9% Dwell Reduction | 100.0% Digging Elimination
========================================================================
Quickstart & Verification
Bash
# Clone the repository
git clone [https://github.com/open-zest/zest-core.git](https://github.com/open-zest/zest-core.git)
cd zest-core

# Run test suite
pytest

# Execute the full corridor demonstration runner
python scripts/demo_runner.py

# Run the data-latency benchmark simulation
python scripts/benchmark_data_latency.py
License
This project is licensed under the MIT License - see the LICENSE file for details.
