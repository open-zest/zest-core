-- 1. STS Quayside Discharge Rate vs. Rail Direct-Bypass Pipeline
SELECT 
    vc.vessel_name,
    COUNT(cm.container_id) AS total_manifest_discharged,
    COUNT(wsa.container_id) AS direct_rail_loaded,
    ROUND((COUNT(wsa.container_id)::NUMERIC / NULLIF(COUNT(cm.container_id), 0)) * 100, 2) AS yard_bypass_ratio_pct,
    ROUND(AVG(mte.dwell_latency_seconds) / 60.0, 2) AS avg_transfer_dwell_minutes
FROM vessel_calls vc
JOIN container_manifest cm ON vc.call_id = cm.call_id
LEFT JOIN modal_transition_events mte ON cm.container_id = mte.container_id 
    AND mte.boundary = 'ON_DOCK_RAIL'
LEFT JOIN wagon_slot_assignments wsa ON cm.container_id = wsa.container_id
WHERE vc.status IN ('BERTHED', 'DISCHARGING')
GROUP BY vc.vessel_name;

-- 2. Inland Dry-Port Siding Inbound Pipeline (RFC North Sea - Med / East)
SELECT 
    rc.destination_dry_port,
    rc.train_service_code,
    rc.target_departure,
    COUNT(wsa.container_id) AS allocated_containers,
    SUM(cm.teu_factor) AS total_teu,
    SUM(cm.gross_mass_kg) / 1000.0 AS gross_tonnage,
    COUNT(CASE WHEN cm.customs_status = 'CLEARED' THEN 1 END) AS efti_cleared_units
FROM rail_rake_consists rc
JOIN wagon_slot_assignments wsa ON rc.consist_id = wsa.consist_id
JOIN container_manifest cm ON wsa.container_id = cm.container_id
WHERE rc.consist_status IN ('LOADING', 'DISPATCH_READY')
GROUP BY rc.destination_dry_port, rc.train_service_code, rc.target_departure
ORDER BY rc.target_departure ASC;
