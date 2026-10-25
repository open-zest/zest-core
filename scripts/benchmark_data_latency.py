"""
Project ZeST - Data Latency Benchmark Simulation Script
Simulates the operational impact of data latency on seaport terminal dwell time,
comparing legacy post-berth polling (t+48h) against Project ZeST feed-forward eFTI token exchange (t-14d).
Self-contained discrete-event engine implemented with standard library priority queue.
"""

import heapq
import random
import statistics

RANDOM_SEED = 42
TOTAL_CONTAINERS = 1500
CORRIDORS = ["ZONE_A_DUI", "ZONE_B_VRN", "ZONE_C_POZ", "ZONE_D_VIE", "ZONE_E_LYS", "ZONE_F_BUD"]

class DiscreteEventEngine:
    def __init__(self):
        self.now = 0.0
        self.events = []
        self._eid = 0

    def schedule(self, delay, callback, *args):
        self._eid += 1
        heapq.heappush(self.events, (self.now + delay, self._eid, callback, args))

    def run(self):
        while self.events:
            time, _, callback, args = heapq.heappop(self.events)
            self.now = time
            callback(*args)

def run_simulation(mode="legacy", data_lag_hours=48.0):
    random.seed(RANDOM_SEED)
    engine = DiscreteEventEngine()
    dwell_times = []
    rehandles = []

    def finish_container(arrival_time, moves):
        dwell = engine.now - arrival_time
        dwell_times.append(dwell)
        rehandles.append(moves)

    def process_container(cid, zone):
        arrival_time = engine.now
        lift_time = random.uniform(0.025, 0.035)

        if mode == "legacy":
            data_resolution = max(0.0, data_lag_hours + random.gauss(0, 4.0))
            extra_moves = random.choices([1, 2, 3], weights=[0.50, 0.35, 0.15])[0]
            dig_time = extra_moves * 0.083
            rail_slot_wait = random.uniform(4.0, 10.0)
            total_delay = lift_time + data_resolution + dig_time + rail_slot_wait
            engine.schedule(total_delay, finish_container, arrival_time, extra_moves)
        else:
            direct_transfer_time = lift_time + random.uniform(0.15, 0.35)
            engine.schedule(direct_transfer_time, finish_container, arrival_time, 0)

    for i in range(TOTAL_CONTAINERS):
        zone = random.choice(CORRIDORS)
        engine.schedule(i * 0.002, process_container, i, zone)

    engine.run()

    return {
        "mode": mode,
        "mean_dwell_h": round(statistics.mean(dwell_times), 2),
        "p95_dwell_h": round(sorted(dwell_times)[int(len(dwell_times) * 0.95)], 2),
        "mean_rehandles": round(statistics.mean(rehandles), 2)
    }

if __name__ == "__main__":
    legacy = run_simulation(mode="legacy", data_lag_hours=48.0)
    zest = run_simulation(mode="zest_feedforward", data_lag_hours=0.0)

    print("=" * 72)
    print("PROJECT ZeST: DATA LATENCY BENCHMARK RESULTS (1,500 TEU CORRIDOR)")
    print("=" * 72)
    print(f"Legacy (t+48h Data Lag):   Mean Dwell: {legacy['mean_dwell_h']}h | p95 Tail: {legacy['p95_dwell_h']}h | Re-handles: {legacy['mean_rehandles']} moves/box")
    print(f"ZeST (t-14d Feed-Forward): Mean Dwell: {zest['mean_dwell_h']}h  | p95 Tail: {zest['p95_dwell_h']}h  | Re-handles: {zest['mean_rehandles']} moves/box")
    print("-" * 72)
    dwell_reduction = round((1 - zest['mean_dwell_h'] / legacy['mean_dwell_h']) * 100, 1)
    rehandle_reduction = round((1 - zest['mean_rehandles'] / legacy['mean_rehandles']) * 100, 1)
    print(f"Impact: {dwell_reduction}% Mean Dwell Reduction | {rehandle_reduction}% Digging Elimination")
    print("=" * 72)
