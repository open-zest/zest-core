import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from solvers.generators.manifest_gen import generate_synthetic_manifest
from solvers.des.milkrun_sim import StochasticMilkRunSimulator, execute_corridor_benchmark

def run_rotterdam_corridor_showcase():
    print("=" * 80)
    print("Project ZeST: Intermodal Europe 2026 Rotterdam Corridor Showcase")
    print("=" * 80)
    
    # 1. Generate standard 1,500 container corridor manifest
    print("\n[1/3] Generating synthetic vessel manifest (1,500 containers)...")
    manifest = generate_synthetic_manifest(total_containers=1500, seed=42)
    print(f"      Total Containers: {len(manifest.containers)}")
    print(f"      Total TEU:        {manifest.total_teu}")
    print(f"      Total VGM Mass:   {manifest.total_vgm_tonnes:,.2f} tonnes")
    print(f"      Net Cargo Mass:   {manifest.total_payload_mass_tonnes:,.2f} tonnes")

    # 2. Run deterministic benchmark comparisons
    print("\n[2/3] Evaluating corridor dwell benchmarks...")
    bench = execute_corridor_benchmark(manifest)
    print(f"      Traditional Dwell Baseline: {bench['baseline_dwell_hours']:.2f} hours")
    print(f"      ZeST Delivery Dwell:        {bench['zest_dwell_hours']:.2f} hours")
    print(f"      Total Shunting Rehandles:   {bench['rehandles']}")

    # 3. Execute stochastic SimPy queuing run
    print("\n[3/3] Simulating stochastic terminal resource contention (SimPy)...")
    simulator = StochasticMilkRunSimulator(manifest, random_seed=42)
    metrics = simulator.run_simulation(duration=168.0)
    
    mean_dwell = sum(metrics["dwell_times"]) / max(len(metrics["dwell_times"]), 1)
    mean_delay = sum(metrics["queue_delays"]) / max(len(metrics["queue_delays"]), 1)
    max_delay = max(metrics["queue_delays"]) if metrics["queue_delays"] else 0.0

    print(f"      Simulated Operational Hours: 168.0 hrs (7-day window)")
    print(f"      Mean Dynamic Dwell:          {mean_dwell:.2f} hours")
    print(f"      Mean Crane Queue Wait:       {mean_delay:.2f} hours")
    print(f"      Max Observed Siding Delay:   {max_delay:.2f} hours")
    print("\n" + "=" * 80)
    print("Corridor simulation completed successfully. Ready for presentation.")
    print("=" * 80)

if __name__ == "__main__":
    run_rotterdam_corridor_showcase()
