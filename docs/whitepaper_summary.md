# Project ZeST: Executive Whitepaper Summary
**Zero-rehandle Siding Transit for European Gateway Freight Networks**

## Executive Summary
Project ZeST (Zero-rehandle Siding Transit) introduces an open-source algorithmic and operational framework that replaces traditional hub-and-spoke hump marshalling with pre-sorted, direct-siding rail milk-runs. By pre-sorting container flows at deep-sea gateway discharge using cryptographic container tokens, ZeST eliminates intermediate shunting yards and enables rapid siding drop-offs across major European dry-port corridors.

## Core Validated Metrics (Rotterdam 1,500-Box Corridor Benchmark)
Across the six primary trans-European rail freight corridors (Duisburg, Verona, Poznań, Vienna, Lyon, Budapest):

* **Baseline Hump-and-Spoke Dwell:** 57.39 hours (mean yard staging, inspection, and classification delay)
* **ZeST Deterministic Dwell:** 4.43 hours (direct siding set-out)
* **Dynamic Siding Dwell (SimPy DES):** 3.55 hours mean operational turnaround under stochastic crane resource contention over a 168.0-hour window
* **Intermediate Shunting Rehandles:** 0 (100% elimination of mid-corridor re-marshalling)
* **Modeled Corridor Volume:** 1,500 containers / 2,840.0 TEU / 31,192.68 gross metric tonnes (25,748.68 net payload tonnes)

## Key Architectural Pillars
1. **Cryptographic Container Tokens:** Immutable SHA-256 tokens binding Verified Gross Mass (VGM), ISO size-type (40HC, 40GP, 20GP), NCTS T1 customs transit clearance, and destination centroids before vessel discharge.
2. **Deterministic Sequence-Ordered Block Trains:** Wagon blocks loaded in exact inverse sequence of corridor dry ports, enabling locomotives to set out wagons at sidings without breaking train continuity.
3. **Stochastic Terminal Queuing (SimPy Engine):** Dynamic discrete-event simulation evaluating crane resource limits, siding queue wait times, and stochastic handling variability.
