#!/usr/bin/env python3
"""
Project ZeST - Dual-Stream Process Block Diagram Builder
Reads the 3 Mermaid (.mmd) process block diagrams from schemas/diagrams/
and compiles a standalone, print-ready & interactive HTML sheet at docs/zest_process_architecture.html.
Zero external Python dependencies.
"""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DIAGRAM_DIR = ROOT_DIR / "schemas" / "diagrams"
OUTPUT_HTML = ROOT_DIR / "docs" / "zest_process_architecture.html"


def build_diagram_sheet() -> Path:
    d1 = (DIAGRAM_DIR / "01_end_to_end_flow.mmd").read_text(encoding="utf-8")
    d2 = (DIAGRAM_DIR / "02_seaport_ingress_flow.mmd").read_text(encoding="utf-8")
    d3 = (DIAGRAM_DIR / "03_dryport_egress_flow.mmd").read_text(encoding="utf-8")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project ZeST — Dual-Stream Process Block Diagrams</title>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'base',
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            }}
        }});
    </script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f8fafc;
            color: #0f172a;
            margin: 0;
            padding: 28px 36px;
        }}
        .header-bar {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            border-bottom: 3px solid #0288d1;
            padding-bottom: 12px;
            margin-bottom: 24px;
        }}
        .header-bar h1 {{
            margin: 0;
            font-size: 24px;
            color: #0f172a;
        }}
        .header-bar .sub {{
            font-size: 13px;
            color: #475569;
            margin-top: 4px;
        }}
        .kpi-strip {{
            display: flex;
            gap: 12px;
        }}
        .kpi-pill {{
            background: #0f172a;
            color: #fff;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
        }}
        .kpi-pill span {{
            color: #38bdf8;
        }}
        .diagram-card {{
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            padding: 20px 24px;
            margin-bottom: 28px;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06);
            page-break-inside: avoid;
        }}
        .diagram-card h2 {{
            margin: 0 0 6px 0;
            font-size: 18px;
            color: #0369a1;
        }}
        .diagram-card p {{
            margin: 0 0 16px 0;
            font-size: 13px;
            color: #475569;
            line-height: 1.45;
        }}
        .legend-bar {{
            display: flex;
            gap: 20px;
            font-size: 12px;
            background: #f1f5f9;
            padding: 10px 16px;
            border-radius: 6px;
            margin-bottom: 22px;
            border: 1px solid #e2e8f0;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-weight: 600;
        }}
        .swatch {{
            width: 14px;
            height: 14px;
            border-radius: 3px;
            display: inline-block;
        }}
        @media print {{
            body {{ background: #fff; padding: 10px; }}
            .diagram-card {{ box-shadow: none; border: 1px solid #94a3b8; }}
        }}
    </style>
</head>
<body>
    <div class="header-bar">
        <div>
            <h1>Project ZeST: Dual-Stream Packet-Switched Freight Architecture</h1>
            <div class="sub">
                Decoupling the Asynchronous Control Plane (EU eFTI 2020/1056 + NCTS T1 Data Stream) from the Synchronous Physical Container Stream
            </div>
        </div>
        <div class="kpi-strip">
            <div class="kpi-pill">Seaport Dwell: <span>57.39h → 4.43h</span></div>
            <div class="kpi-pill">Yard Re-Handles: <span>2.4 → 0</span></div>
            <div class="kpi-pill">Berth Reduction: <span>20–30%</span></div>
            <div class="kpi-pill">Rail Breakeven: <span>195 km</span></div>
        </div>
    </div>

    <div class="legend-bar">
        <div class="legend-item">
            <span class="swatch" style="background:#ffcdd2; border:1.5px solid #b71c1c;"></span>
            Legacy Store-and-Forward Bottleneck (Coupled Data &amp; Containers)
        </div>
        <div class="legend-item">
            <span class="swatch" style="background:#f3e5f5; border:1.5px dashed #7b1fa2;"></span>
            ZeST Control Plane (T-5 Days Asynchronous Data Stream)
        </div>
        <div class="legend-item">
            <span class="swatch" style="background:#b2dfdb; border:1.5px solid #004d40;"></span>
            ZeST Physical Plane (Zero-Stack Cut-Through Container Stream)
        </div>
        <div class="legend-item">
            <span class="swatch" style="background:#fff9c4; border:1.5px solid #f57f17;"></span>
            Exception / Uncrystallized Tail Isolation (Graceful Degradation)
        </div>
    </div>

    <div class="diagram-card">
        <h2>Diagram 1: End-to-End System Process Flow (Origin Port → Sea Transit → Seaport → Rail Spine → Dry Port)</h2>
        <p>
            <b>Architectural Shift:</b> Legacy intermodal operations wait until physical vessel arrival (<code>T+0</code>) to resolve customs, commercial release, and rail slot allocation—forcing containers into a 57.39-hour stacking buffer. ZeST crystallizes the <b>eFTI + NCTS T1 + Wagon Slot token at T-5 days (120 hours out at sea)</b>, turning the deep-sea port into an optical packet demultiplexer.
        </p>
        <pre class="mermaid">
{d1}
        </pre>
    </div>

    <div class="diagram-card">
        <h2>Diagram 2: Seaport Ingress BGP Router Flow (Quayside STS Crane → Optical Gate → Direct Rail Consist)</h2>
        <p>
            <b>Graceful Degradation &amp; Exception Isolation:</b> Pre-cleared containers follow the bold green cut-through spine directly from the Ship-to-Shore (STS) crane onto single-zone block trains (<code>ZONE_A_DUI</code> through <code>ZONE_F_BUD</code>) with a 0.28h data verification buffer and zero yard re-handles. Any container missing a T-5 token is cleanly shunted to the isolated exception buffer without blocking the main rail transfer spine.
        </p>
        <pre class="mermaid">
{d2}
        </pre>
    </div>

    <div class="diagram-card">
        <h2>Diagram 3: Inland Dry Port Egress Access Switch Flow (Corridor Geofence → Direct Wagon-to-Chassis → 195 km Halo)</h2>
        <p>
            <b>Eliminating Secondary Inland Dwell:</b> When the single-zone block train crosses the <code>T-2h</code> corridor geofence, the ZeST token triggers automated local customs release and dispatches timed slot beacons to regional electric/short-haul trucks. Containers transfer directly from rail wagon to truck chassis (under 30-minute terminal turnaround), collapsing the rail-over-road breakeven distance to <b>195 km</b>.
        </p>
        <pre class="mermaid">
{d3}
        </pre>
    </div>
</body>
</html>
"""

    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    return OUTPUT_HTML


if __name__ == "__main__":
    out = build_diagram_sheet()
    print(f"[ZeST Diagram Builder] Success: Saved 3-part Dual-Stream Architecture Sheet to {out}")
