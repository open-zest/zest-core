# Project ZeST: Intermodal Europe 2026 Rotterdam Briefing
**Zero-rehandle Siding Transit for European Gateway Freight Networks**

## Executive Benchmark Summary
* **Benchmark Size:** 1,500 Containers | 2,840.0 TEU | 31,192.68 Tonnes Gross Mass
* **Intermediate Shunting Rehandles:** 0
* **Traditional Baseline Dwell:** 57.39 hours
* **ZeST Direct-Siding Set-Out:** 4.43 hours
* **SimPy Dynamic Turnaround:** 3.55 hours mean operational dwell under crane contention

## Corridor Performance Comparison
* **Duisburg (`ZONE_A_DUI`):** Traditional 57.39h vs. ZeST 4.43h (-92.3%)
* **Verona (`ZONE_B_VRN`):** Traditional 84.50h vs. ZeST 14.80h (-82.5%)
* **Poznań (`ZONE_C_POZ`):** Traditional 81.20h vs. ZeST 13.50h (-83.4%)
* **Vienna (`ZONE_D_VIE`):** Traditional 89.00h vs. ZeST 15.20h (-82.9%)
* **Lyon (`ZONE_E_LYS`):** Traditional 76.40h vs. ZeST 11.90h (-84.4%)
* **Budapest (`ZONE_F_BUD`):** Traditional 98.70h vs. ZeST 18.40h (-81.4%)

## Architectural Pillars
1. **Cryptographic Tokens:** Deterministic pre-sort based on immutable container hashes before vessel offload.
2. **Direct-Siding Drop-Off:** Set-out operations at dry port sidings without hump classification.
3. **Stochastic Operational Validation:** SimPy discrete-event engine modeling terminal crane resource contention over 168.0h continuous operation.
