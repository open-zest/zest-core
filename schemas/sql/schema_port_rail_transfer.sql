-- Enable UUID and cryptographic extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Enum types for modal states and eFTI validation
CREATE TYPE vessel_call_status AS ENUM ('PLANNED', 'BERTHED', 'DISCHARGING', 'COMPLETED', 'DEPARTED');
CREATE TYPE transfer_boundary AS ENUM ('STS_DISCHARGE', 'BUFFER_BYPASS', 'ON_DOCK_RAIL', 'MAINLINE_TRANSIT', 'DRY_PORT_SIDINGS');
CREATE TYPE efti_auth_status AS ENUM ('PENDING', 'VALIDATED', 'FLAGGED', 'CLEARED');

-- 1. Vessel Call Schedule & Manifest Registry
CREATE TABLE IF NOT EXISTS vessel_calls (
    call_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vessel_name VARCHAR(100) NOT NULL,
    imo_number VARCHAR(10) NOT NULL,
    call_sign VARCHAR(20),
    berth_id VARCHAR(20) NOT NULL,
    eta TIMESTAMPTZ NOT NULL,
    etd TIMESTAMPTZ NOT NULL,
    total_manifest_teu INT NOT NULL CHECK (total_manifest_teu BETWEEN 1000 AND 25000),
    status vessel_call_status NOT NULL DEFAULT 'PLANNED',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 2. Core Container Inventory & eFTI Token Attributes
CREATE TABLE IF NOT EXISTS container_manifest (
    container_id VARCHAR(11) PRIMARY KEY, -- BIC ISO 6346 (e.g., MSCU1234567)
    call_id UUID NOT NULL REFERENCES vessel_calls(call_id) ON DELETE CASCADE,
    iso_size_type VARCHAR(4) NOT NULL,   -- e.g., '45G1', '22G1'
    teu_factor NUMERIC(3,1) NOT NULL,     -- 1.0, 2.0, 2.25
    gross_mass_kg NUMERIC(8,2) NOT NULL,
    verified_gross_mass BOOLEAN NOT NULL DEFAULT TRUE,
    hazard_class VARCHAR(10) DEFAULT NULL, -- IMDG class if applicable
    discharge_bay_slot VARCHAR(10) NOT NULL, -- Stownet bay-row-tier (e.g., '0420482')
    
    -- EU Regulation 2020/1056 (eFTI) Regulatory Stream
    efti_dataset_id VARCHAR(64) NOT NULL,
    efti_token_hash VARCHAR(64) NOT NULL,
    efti_platform_id VARCHAR(50) NOT NULL,
    customs_status efti_auth_status NOT NULL DEFAULT 'PENDING',
    final_inland_node VARCHAR(20) NOT NULL, -- e.g., 'NL-RTM-MVII', 'DE-DUI-DIT', 'HU-BUD-BILK'
    target_departure_train_id VARCHAR(50) DEFAULT NULL,
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_container_call_dest ON container_manifest(call_id, final_inland_node);
CREATE INDEX IF NOT EXISTS idx_container_efti ON container_manifest(efti_dataset_id, efti_token_hash);

-- 3. Transition Event Log: STS Discharge -> Rail Bypass -> Siding Set-Out
CREATE TABLE IF NOT EXISTS modal_transition_events (
    event_id BIGSERIAL,
    event_time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    container_id VARCHAR(11) NOT NULL REFERENCES container_manifest(container_id),
    boundary transfer_boundary NOT NULL,
    source_loc VARCHAR(30) NOT NULL,   -- e.g., 'STS_CRANE_04', 'AGV_LANE_02', 'RAIL_TRACK_3'
    target_loc VARCHAR(30) NOT NULL,   -- e.g., 'BUFFER_A', 'WAGON_WAG_982341_S1', 'SIDING_B2'
    dwell_latency_seconds INT NOT NULL DEFAULT 0,
    equipment_id VARCHAR(30) NOT NULL, -- e.g., 'QC-14', 'RMG-02', 'LOCO-189-992'
    efti_validated_at_gate BOOLEAN NOT NULL DEFAULT FALSE,
    operator_notes TEXT DEFAULT NULL,
    PRIMARY KEY (event_id, event_time)
) PARTITION BY RANGE (event_time);

-- Monthly partition for Nov 2026
CREATE TABLE IF NOT EXISTS modal_transition_events_2026_11 PARTITION OF modal_transition_events
    FOR VALUES FROM ('2026-11-01 00:00:00+00') TO ('2026-12-01 00:00:00+00');

-- 4. On-Dock & Mainline Rail Consist Composition
CREATE TABLE IF NOT EXISTS rail_rake_consists (
    consist_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    train_service_code VARCHAR(30) NOT NULL, -- e.g., 'NSRM-SHUTTLE-DUI-04'
    track_id VARCHAR(20) NOT NULL,
    destination_dry_port VARCHAR(30) NOT NULL, -- 'Duisburg DIT', 'Poznan Kobylnica', etc.
    target_departure TIMESTAMPTZ NOT NULL,
    actual_departure TIMESTAMPTZ DEFAULT NULL,
    max_teu_capacity INT NOT NULL DEFAULT 96,
    max_trailing_load_tons NUMERIC(7,2) NOT NULL DEFAULT 2200.0,
    consist_status VARCHAR(20) NOT NULL DEFAULT 'LOADING'
);

-- 5. Rail Wagon Slot Allocations
CREATE TABLE IF NOT EXISTS wagon_slot_assignments (
    slot_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    consist_id UUID NOT NULL REFERENCES rail_rake_consists(consist_id) ON DELETE CASCADE,
    wagon_uic_number VARCHAR(16) NOT NULL, -- UIC 12-digit wagon number
    wagon_slot_index INT NOT NULL,         -- Wagon position in rake (1 to 32)
    slot_section VARCHAR(2) NOT NULL,      -- 'A', 'B', 'C' platform pockets
    container_id VARCHAR(11) UNIQUE REFERENCES container_manifest(container_id),
    assigned_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    loaded_at TIMESTAMPTZ DEFAULT NULL,
    axle_load_tons NUMERIC(4,2) DEFAULT NULL
);
