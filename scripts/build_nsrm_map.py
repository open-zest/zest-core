#!/usr/bin/env python3
"""
Project ZeST - Pan-European NSRM & TEN-T Packet-Switched Corridor Map Visualizer
Replicates the exact visual styling, DivIcon markers, curved multi-waypoint lines,
and popup tables from tools/corridor_map/build_map.py (with zero Python dependencies).
"""

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT_DIR / "schemas" / "nsrm_topology.json"
OUTPUT_HTML = ROOT_DIR / "docs" / "nsrm_packet_network_map.html"


def build_nsrm_sdn_map(json_path: Path = SCHEMA_PATH, output_path: Path = OUTPUT_HTML) -> Path:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data_json_str = json.dumps(data, indent=2)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project ZeST - Pan-European Packet-Switched Corridor Map</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        html, body, #map {{
            height: 100%;
            width: 100%;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        .leaflet-div-icon {{
            background: transparent !important;
            border: none !important;
        }}
        .zest-legend {{
            position: fixed;
            bottom: 24px;
            left: 24px;
            width: 370px;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.95);
            color: #111;
            padding: 14px 16px;
            border-radius: 8px;
            border: 1px solid #ccc;
            font-size: 12px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.25);
        }}
        .zest-legend h4 {{
            margin: 0 0 6px 0;
            font-size: 14px;
            color: #00838F;
            border-bottom: 2px solid #00838F;
            padding-bottom: 4px;
        }}
        .legend-row {{
            display: flex;
            align-items: center;
            margin: 6px 0;
            font-size: 11.5px;
            color: #333;
        }}
        .legend-icon-box {{
            width: 36px;
            display: flex;
             justify-content: center;
            align-items: center;
            margin-right: 8px;
            flex-shrink: 0;
        }}
    </style>
</head>
<body>
    <div id="map"></div>

    <div class="zest-legend">
        <h4>Project ZeST: EU Rail-to-Packet Topology</h4>
        <div class="legend-row">
            <div class="legend-icon-box">
                <div style="background-color: #D50000; width: 18px; height: 18px; border-radius: 4px; border: 2px solid #FFF; box-shadow: 0 0 4px rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center;">
                    <div style="width: 5px; height: 5px; background-color: #FFF; border-radius: 50%;"></div>
                </div>
            </div>
            <div><b>Deep-Sea Port (Ingress BGP Router):</b> T-5 eFTI Demux</div>
        </div>
        <div class="legend-row">
            <div class="legend-icon-box">
                <div style="background-color: #0288D1; width: 26px; height: 13px; border-radius: 8px; border: 2px solid #FFF; box-shadow: 0 0 4px rgba(0,0,0,0.5);"></div>
            </div>
            <div><b>Core Megahub (MPLS Label Switch):</b> Zero-Shunt Switching</div>
        </div>
        <div class="legend-row">
            <div class="legend-icon-box">
                <div style="background-color: #2E7D32; width: 13px; height: 13px; border-radius: 50%; border: 2px solid #FFF; box-shadow: 0 0 4px rgba(0,0,0,0.5);"></div>
            </div>
            <div><b>Inland Dry Port (Egress Switch):</b> 195 km Breakeven Halo</div>
        </div>
        <div class="legend-row">
            <div class="legend-icon-box">
                <div style="background-color: #FFAB00; width: 18px; height: 18px; border-radius: 50%; border: 2px solid #D50000; box-shadow: 0 0 5px rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold; color: #000;">!</div>
            </div>
            <div><b>TEN-T Choke Point:</b> 2035+ Civil Gap vs. ZeST SDN Fix</div>
        </div>
    </div>

    <script>
        const data = {data_json_str};

        // Exact OpenStreetMap default from tools/corridor_map/build_map.py + Terrain option
        const osmTiles = L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            maxZoom: 19,
            attribution: '&copy; OpenStreetMap contributors'
        }});

        const terrainTiles = L.tileLayer(
            'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{{z}}/{{y}}/{{x}}',
            {{ attribution: 'Tiles &copy; Esri', maxZoom: 18 }}
        );

        const map = L.map('map', {{
            center: data.center || [50.0, 11.5],
            zoom: data.zoom_start || 5,
            layers: [osmTiles],
            zoomControl: true
        }});
        L.control.scale().addTo(map);

        const layerLines = L.layerGroup().addTo(map);
        const layerHalos = L.layerGroup().addTo(map);
        const layerNodes = L.layerGroup().addTo(map);
        const layerChokes = L.layerGroup().addTo(map);

        // 1. Render Curved Multi-Waypoint Transit Lines (Exact build_map.py style)
        (data.lines || []).forEach(line => {{
            const meta = line.meta || {{}};
            const popupHtml = `
            <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; min-width: 265px;">
                <h4 style="margin: 0 0 6px 0; color: ${{line.color}};">${{line.name}}</h4>
                <table style="width: 100%; font-size: 12px; border-collapse: collapse; line-height: 1.45;">
                    <tr><td style="color: #666;">Corridor:</td><td><b>${{meta.rfc || 'N/A'}}</b></td></tr>
                    <tr><td style="color: #666;">SDN Role:</td><td><b style="color:#00838F;">${{meta.sdn_role || 'Optical Trunk'}}</b></td></tr>
                    <tr><td style="color: #666;">Capacity:</td><td><b>${{meta.capacity || 'N/A'}}</b></td></tr>
                    <tr><td style="color: #666;">Signaling:</td><td>${{meta.signaling || 'N/A'}}</td></tr>
                    <tr><td style="color: #666;">Traction:</td><td>${{meta.traction || 'N/A'}}</td></tr>
                    <tr><td style="color: #666;">Max Length:</td><td>${{meta.max_length || 'N/A'}}</td></tr>
                    <tr><td style="color: #666;">P400 Gauge:</td><td>${{meta.p400 || 'N/A'}}</td></tr>
                </table>
            </div>
            `;

            L.polyline(line.coords, {{
                color: line.color,
                weight: line.weight || 4,
                opacity: line.opacity || 0.85
            }})
            .bindTooltip(line.name)
            .bindPopup(popupHtml, {{ maxWidth: 330 }})
            .addTo(layerLines);
        }});

        // 2. Render Downstream Catchment Zones (Exact build_map.py Circle style)
        (data.nodes || []).forEach(node => {{
            if (node.radius_km) {{
                const zColor = node.zone_color || "#1976D2";
                L.circle([node.lat, node.lon], {{
                    radius: node.radius_km * 1000,
                    color: zColor,
                    fill: true,
                    fillColor: zColor,
                    fillOpacity: 0.15,
                    weight: 1.5,
                    dashArray: "4, 6"
                }})
                .bindTooltip(`Hinterland Catchment: ${{node.zone_label || node.zone}}`)
                .addTo(layerHalos);
            }}
        }});

        // 3. Render Nodes with Exact DivIcon HTML from build_map.py
        (data.nodes || []).forEach(node => {{
            let zoneHeader = "";
            if (node.zone && !["ORIGIN_GATEWAY", "CORRIDOR_JUNCTION", "CORRIDOR_SIDING"].includes(node.zone)) {{
                const bg = node.zone_color || (node.type === "seaport" ? "#D50000" : node.type === "bottleneck" ? "#D50000" : "#333");
                zoneHeader = `
                <div style="background-color: ${{bg}}; color: #fff; padding: 3px 6px; border-radius: 3px; font-size: 11px; font-weight: bold; margin-bottom: 6px; display: inline-block;">
                    ZeST Node: ${{node.zone}}
                </div>
                `;
            }}

            const popupContent = `
            <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; min-width: 260px;">
                ${{zoneHeader}}
                <div style="border-bottom: 2px solid #00838F; padding-bottom: 4px; margin-bottom: 8px;">
                    <span style="font-size: 10px; text-transform: uppercase; letter-spacing: 1px; color: #888;">${{node.type.replace('_', ' ')}}</span>
                    <h3 style="margin: 2px 0 0 0; font-size: 14px; color: #111;">${{node.name}}</h3>
                </div>
                <table style="width: 100%; font-size: 12px; color: #333; line-height: 1.5;">
                    <tr><td style="color: #666;">Capacity/Vol:</td><td><b>${{node.throughput}}</b></td></tr>
                    <tr><td style="color: #666;">SDN / Role:</td><td><b>${{node.intermodal}}</b></td></tr>
                    <tr><td style="color: #666;">Dwell / Fix:</td><td><span style="color: #D32F2F; font-weight: bold;">${{node.dwell}}</span></td></tr>
                    <tr><td style="color: #666;">Facility Type:</td><td>${{node.role}}</td></tr>
                </table>
            </div>
            `;

            let iconHtml = "";
            let iconSize = [14, 14];
            let iconAnchor = [7, 7];

            if (node.type === "seaport") {{
                iconHtml = `
                <div style="background-color: #D50000; width: 22px; height: 22px; border-radius: 4px; border: 2px solid #FFF; box-shadow: 0 0 6px rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center;">
                    <div style="width: 6px; height: 6px; background-color: #FFF; border-radius: 50%;"></div>
                </div>
                `;
                iconSize = [22, 22];
                iconAnchor = [11, 11];
            }} else if (node.type === "multi_line_oval") {{
                const badgeColor = node.zone_color || "#1976D2";
                iconHtml = `
                <div style="background-color: ${{badgeColor}}; width: 30px; height: 16px; border-radius: 10px; border: 2px solid #FFF; box-shadow: 0 0 6px rgba(0,0,0,0.5);"></div>
                `;
                iconSize = [30, 16];
                iconAnchor = [15, 8];
            }} else if (node.type === "bottleneck") {{
                iconHtml = `
                <div style="background-color: #FFAB00; width: 20px; height: 20px; border-radius: 50%; border: 2px solid #D50000; box-shadow: 0 0 6px rgba(0,0,0,0.6); display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 12px; color: #000;">!</div>
                `;
                iconSize = [20, 20];
                iconAnchor = [10, 10];
            }} else {{
                const badgeColor = node.zone_color || "#2E7D32";
                iconHtml = `
                <div style="background-color: ${{badgeColor}}; width: 14px; height: 14px; border-radius: 50%; border: 2px solid #FFF; box-shadow: 0 0 4px rgba(0,0,0,0.5);"></div>
                `;
                iconSize = [14, 14];
                iconAnchor = [7, 7];
            }}

            const marker = L.marker([node.lat, node.lon], {{
                icon: L.divIcon({{
                    iconSize: iconSize,
                    iconAnchor: iconAnchor,
                    html: iconHtml
                }})
            }})
            .bindTooltip(`${{node.name}} (${{node.zone || node.type}})`)
            .bindPopup(popupContent, {{ maxWidth: 320 }});

            if (node.type === "bottleneck") {{
                marker.addTo(layerChokes);
            }} else {{
                marker.addTo(layerNodes);
            }}
        }});

        L.control.layers(
            {{
                "OpenStreetMap (Yesterday's Default)": osmTiles,
                "Physical Shaded Terrain (Esri Topo)": terrainTiles
            }},
            {{
                "1. Pan-EU Corridor Lines (Curved)": layerLines,
                "2. 195 km Breakeven Catchment Halos": layerHalos,
                "3. Seaports, Core Switches & Dry Ports": layerNodes,
                "4. TEN-T Choke Points vs ZeST Fix": layerChokes
            }},
            {{ collapsed: false }}
        ).addTo(map);
    </script>
</body>
</html>
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_path


if __name__ == "__main__":
    out = build_nsrm_sdn_map()
    print(f"[ZeST Map Visualizer] Success: Saved Pan-European NSRM map to {out}")
