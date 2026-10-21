"""
Project ZeST: Zone-Block Container Ship Position Problem (ZB-CSPP)
Heuristic partitioner mapping destination rail zones to vessel bays.
"""

from typing import List, Dict


class ZoneStowageOptimizer:
    def __init__(self, num_bays: int = 12, max_tier: int = 8):
        self.num_bays = num_bays
        self.max_tier = max_tier
        # Assign corridor sequence: earlier drop zones mapped to aft/forward distinct blocks
        self.bay_allocations = {
            f"ZONE_{i}": [2 * i - 1, 2 * i] for i in range(1, 7)
        }

    def allocate_manifest(self, manifest_tokens: List[Dict]) -> Dict[str, List[Dict]]:
        stowage_plan = {b: [] for b in range(1, self.num_bays + 1)}
        
        # Sort heavy containers to bottom tiers to maintain GM >= 0.15m
        sorted_manifest = sorted(manifest_tokens, key=lambda x: x["vgm_kg"], reverse=True)

        for token in sorted_manifest:
            target_bays = self.bay_allocations.get(token["destination_zone_code"], [1])
            assigned = False
            for bay in target_bays:
                if len(stowage_plan[bay]) < self.max_tier:
                    stowage_plan[bay].append(token)
                    assigned = True
                    break
            if not assigned:
                # Overflow bay fallback
                stowage_plan[1].append(token)

        return stowage_plan

    @staticmethod
    def verify_stability(stowage_plan: Dict[int, List[Dict]]) -> bool:
        """Verifies center-of-mass heuristic: lower tiers must carry heavier containers."""
        for bay, tiers in stowage_plan.items():
            weights = [c["vgm_kg"] for c in tiers]
            if weights != sorted(weights, reverse=True):
                return False
        return True
    