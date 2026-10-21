"""
tests/test_manifest_generator.py
================================
Regression tests for synthetic manifest generator and schema compliance.
"""

from solvers.generators.manifest_gen import generate_synthetic_manifest
from schemas.manifest_models import DestinationZoneCode, VesselManifest


def test_synthetic_manifest_generation():
    count = 250
    manifest = generate_synthetic_manifest(total_containers=count, seed=123)

    assert isinstance(manifest, VesselManifest)
    assert len(manifest.containers) == count
    assert manifest.total_teu > count  # High-cube mix ensures TEU > raw box count
    assert manifest.total_payload_mass_tonnes > 0.0

    # Ensure all 6 inland corridor zones receive volume
    dist = manifest.zone_distribution_summary()
    assert len(dist) == len(DestinationZoneCode)
    for zone, qty in dist.items():
        assert qty > 0


def test_token_and_vgm_invariants():
    manifest = generate_synthetic_manifest(total_containers=50, seed=99)
    for c in manifest.containers:
        # Strict SHA-256 validation (64 hex characters)
        assert len(c.cryptographic_token) == 64
        # SOLAS VGM bounds
        assert 2000.0 < c.vgm_kg <= 36000.0
