# European & UK Intermodal Corridor Reference

All European rail corridors modeled in Project ZeST operate **single-stack** container trains (constrained by overhead electrification and loading gauge). Because physical train capacity cannot simply be stacked higher, corridor throughput depends on protecting rail slot timing and eliminating port-side dwell.

## Priority Corridor Matrix

| Corridor / Axis | Anchor Gateways | Primary Physical Constraint | Digital Synchronization Lever |
| :--- | :--- | :--- | :--- |
| **Orient / East-Med & Black Sea** | Port of Constanța, Trieste, Koper | CFR rail modernization (~15.9 km/h avg freight speed), ~50% of corridor restricts 740m trains, over 85% lacks operational ETCS | T-5 pre-arrival FTI004 container pointers to prevent "warehouses on wheels" siding lockups. |
| **Baltic–Adriatic & Three Seas** | Port of Gdańsk (Baltic Hub), Klaipėda, Koper | Rapid TEU volume surges outpacing inland marshalling capacity and cross-border gauge/handover friction | Container-level UIL continuity across port-to-rail handoffs (aligned with live eFTI4EU port pilots). |
| **Rhine–Alpine / North Sea** | Rotterdam, Antwerp-Bruges, Hamburg | High yard utilization, 10%+ peak port capacity deficits, and tight inland rail/barge windows | Zone-block vessel stowage paired with pre-cleared quay-to-rail dispatch. |
| **UK Deepwater & Cross-Channel** | Felixstowe, London Gateway, Southampton | UK–EU post-July 2027 eFTI border friction and Network Rail / GBR slot scarcity against the 40%-by-2040 rail growth target | Alignment of UK Electronic Trade Documents Act (ETDA) / eBL workflows with EU eFTI Gate lookups. |

## Modeling Scope

Each corridor entry maps directly to parameter profiles in `zest-core` (`solvers/dwell_sim.py` and `solvers/milkrun_sim.py`), allowing terminal operators and policy teams to stress-test pre-arrival clearance against local rail-slot scarcity.
