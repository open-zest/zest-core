"""
Project ZeST: Zone-Block Container Ship Position Problem (ZB-CSPP)
Heuristic partitioner mapping destination rail zones to vessel bays.
"""

from typing import List, Dict, Any


class ZoneStowageOptimizer:
    def __init__(self, num_bays: int = 12, max_tier: int = 8):
        self.num_bays = num_bays
        self.max_tier = max_tier
        self.bay_allocations = {
            f"ZONE_{i}": [2 * i - 1, 2 * i] for i in range(1, 7)
        }

    @staticmethod
    def _extract_weight(token: Dict[str, Any]) -> float:
        if "transport_equipment" in token and "vgm_kg" in token["transport_equipment"]:
            return float(token["transport_equipment"]["vgm_kg"])
        return float(token.get("vgm_kg", 0.0))

    @staticmethod
    def _extract_zone(token: Dict[str, Any]) -> str:
        if "zest_corridor_routing" in token and "destination_zone_code" in token["zest_corridor_routing"]:
            return str(token["zest_corridor_routing"]["destination_zone_code"])
        return str(token.get("destination_zone_code", "ZONE_1"))

    def allocate_manifest(self, manifest_tokens: List[Dict[str, Any]]) -> Dict[int, List[Dict[str, Any]]]:
        stowage_plan: Dict[int, List[Dict[str, Any]]] = {b: [] for b in range(1, self.num_bays + 1)}
        
        sorted_manifest = sorted(
            manifest_tokens,
            key=self._extract_weight,
            reverse=True
        )

        for token in sorted_manifest:
            target_zone = self._extract_zone(token)
            target_bays = self.bay_allocations.get(target_zone, [1])
            assigned = False
            for bay in target_bays:
                if len(stowage_plan[bay]) < self.max_tier:
                    stowage_plan[bay].append(token)
                    assigned = True
                    break
            if not assigned:
                for bay in range(1, self.num_bays + 1):
                    if len(stowage_plan[bay]) < self.max_tier:
                        stowage_plan[bay].append(token)
                        assigned = True
                        break

        return stowage_plan

    def verify_stability(self, stowage_plan: Dict[int, List[Dict[str, Any]]]) -> bool:
        for bay, tiers in stowage_plan.items():
            weights = [self._extract_weight(c) for c in tiers]
            if weights != sorted(weights, reverse=True):
                return False
        return True
