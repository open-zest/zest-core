#!/usr/bin/env python3
"""
Project ZeST - NSRM Corridor Map Visualizer
Generates an interactive Google Maps-style Leaflet visualization of the
North Sea - Rhine - Mediterranean rail freight corridor.

Nodes:
- Seaports: Square red badge
- Junction / Multi-line Hubs: Blue oval
- Single-line Terminals: Green circle
"""

import os
import folium
from folium import DivIcon

def generate_map(output_path="tools/corridor_map/corridor_nsrm_map.html"):
    # Standard OpenStreetMap tile server: completely free, open, and watermark-free
    m = folium.Map(
        location=[51.4, 5.8],
        zoom_start=7,
        tiles="OpenStreetMap",
        control_scale=True
    )

    # 1. TRANSIT LINES (Corridor Backbone with operational metadata)
    lines = [
        {
            "name": "Betuweroute (Dedicated Freight Spine)",
            "coords": [
                [51.954, 4.041],  # Maasvlakte II
                [51.871, 4.341],  # Waalhaven / Rotterdam Main
                [51.826, 4.602],  # Kijfhoek Marshalling Yard
                [51.865, 5.312],  # Tiel Siding
                [51.936, 6.071],  # Zevenaar (Border Transfer)
                [51.834, 6.241],  # Emmerich
                [51.442, 6.762]   # Duisburg Hub
            ],
            "color": "#00838F",  # Deep Cyan
            "weight": 5,
            "opacity": 0.85,
            "meta": {
                "rfc": "RFC North Sea–Med (RFC 1 / RFC 2 Spine)",
                "capacity": "150–180 freight paths/day",
                "signaling": "ERTMS/ETCS Level 2",
                "traction": "25 kV AC (NL) / 15 kV AC (DE)",
                "max_length": "740 m standard",
                "p400": "Yes (Four-meter pocket wagon capable)"
            }
        },
        {
            "name": "Brabant Route (Diversionary / Secondary)",
            "coords": [
                [51.826, 4.602],  # Kijfhoek
                [51.583, 4.776],  # Breda
                [51.441, 5.478],  # Eindhoven
                [51.370, 6.172],  # Venlo Dry Port
                [51.333, 6.583],  # Viersen / Krefeld
                [51.442, 6.762]   # Duisburg Hub
            ],
            "color": "#E65100",  # Dark Amber
            "weight": 3.5,
            "opacity": 0.75,
            "meta": {
                "rfc": "Connecting Corridor / Diversionary",
                "capacity": "45–60 mixed freight slots/day",
                "signaling": "ATB-EG / PZB90",
                "traction": "1.5 kV DC (NL) / 15 kV AC (DE)",
                "max_length": "650 m (740 m restricted)",
                "p400": "Restricted Profile"
            }
        },
        {
            "name": "Rhine-Alpine Southern Trunk (Duisburg to Basel)",
            "coords": [
                [51.442, 6.762],  # Duisburg
                [50.937, 6.960],  # Cologne Eifeltor
                [50.078, 8.243],  # Mainz / Rhine Valley
                [49.006, 8.403],  # Karlsruhe Hub
                [47.559, 7.588]   # Basel Kleinhüningen
            ],
            "color": "#2E7D32",  # Rail Green
            "weight": 4,
            "opacity": 0.8,
            "meta": {
                "rfc": "RFC 1 / Rhine-Alpine Core Trunk",
                "capacity": "200+ mixed slots/day (Choke Point: Middle Rhine)",
                "signaling": "PZB / LZB / ETCS overlay",
                "traction": "15 kV AC",
                "max_length": "740 m",
                "p400": "Fully Certified"
            }
        }
    ]

    for line in lines:
        popup_html = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; min-width: 260px;">
            <h4 style="margin: 0 0 6px 0; color: {line['color']};">{line['name']}</h4>
            <table style="width: 100%; font-size: 12px; border-collapse: collapse; line-height: 1.4;">
                <tr><td style="color: #666;">Corridor:</td><td><b>{line['meta']['rfc']}</b></td></tr>
                <tr><td style="color: #666;">Capacity:</td><td><b>{line['meta']['capacity']}</b></td></tr>
                <tr><td style="color: #666;">Signaling:</td><td>{line['meta']['signaling']}</td></tr>
                <tr><td style="color: #666;">Traction:</td><td>{line['meta']['traction']}</td></tr>
                <tr><td style="color: #666;">Max Length:</td><td>{line['meta']['max_length']}</td></tr>
                <tr><td style="color: #666;">P400 Gauge:</td><td>{line['meta']['p400']}</td></tr>
            </table>
        </div>
        """
        folium.PolyLine(
            locations=line["coords"],
            color=line["color"],
            weight=line["weight"],
            opacity=line["opacity"],
            tooltip=line["name"],
            popup=folium.Popup(popup_html, max_width=320)
        ).add_to(m)

    # 2. NODES (Seaports, Single-Line Circles, Multi-Line Ovals)
    nodes = [
        {
            "name": "Port of Rotterdam (Maasvlakte II)",
            "type": "seaport",
            "lat": 51.954,
            "lon": 4.041,
            "throughput": "14.5M TEU/yr (EU Gateway #1)",
            "intermodal": "11% rail share (EU target: 20%)",
            "dwell": "Traditional: 52 hrs -> ZeST Target: 12 hrs",
            "role": "Deepwater Gateway / Quayside Departure"
        },
        {
            "name": "Kijfhoek Marshalling Yard",
            "type": "multi_line_oval",
            "lat": 51.826,
            "lon": 4.602,
            "throughput": "43 sorting tracks (Largest in NL)",
            "intermodal": "Spine Sorting Node (Betuwe / Brabant confluence)",
            "dwell": "Sorting latency: 6–14 hrs",
            "role": "Rail Network Switching Hub"
        },
        {
            "name": "Tiel Intermodal Siding",
            "type": "single_line_circle",
            "lat": 51.865,
            "lon": 5.312,
            "throughput": "Secondary Passing / Holding Loop",
            "intermodal": "Single freight track access",
            "dwell": "Operational hold / buffer",
            "role": "Flow-through siding"
        },
        {
            "name": "Venlo Rail Terminal",
            "type": "single_line_circle",
            "lat": 51.370,
            "lon": 6.172,
            "throughput": "400K TEU/yr",
            "intermodal": "Bimodal Inland Gate (Rail/Road)",
            "dwell": "Border dispatch: 4 hrs",
            "role": "Cabooter Inland Dry Port"
        },
        {
            "name": "Duisburg Gateway Terminal (DGT / DIT)",
            "type": "multi_line_oval",
            "lat": 51.442,
            "lon": 6.762,
            "throughput": "4.2M TEU/yr (World's largest inland port)",
            "intermodal": "Trimodal Intermodal Hub (Water/Rail/Road)",
            "dwell": "Inland sorting buffer: 18 hrs",
            "role": "Rhine-Ruhr Central Consolidation Node"
        },
        {
            "name": "Basel Kleinhüningen / Weil am Rhein",
            "type": "multi_line_oval",
            "lat": 47.559,
            "lon": 7.588,
            "throughput": "Swiss Rhine Port Gateway",
            "intermodal": "Trimodal South Portal to AlpTransit / Gotthard",
            "dwell": "Customs / Transshipment: 10 hrs",
            "role": "Alpine Gateway Junction"
        }
    ]

    for node in nodes:
        popup_content = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; min-width: 240px;">
            <div style="border-bottom: 2px solid #00838F; padding-bottom: 4px; margin-bottom: 8px;">
                <span style="font-size: 10px; text-transform: uppercase; letter-spacing: 1px; color: #888;">{node['type'].replace('_', ' ')}</span>
                <h3 style="margin: 2px 0 0 0; font-size: 14px; color: #111;">{node['name']}</h3>
            </div>
            <table style="width: 100%; font-size: 12px; color: #333; line-height: 1.5;">
                <tr><td style="color: #666;">Capacity/Vol:</td><td><b>{node['throughput']}</b></td></tr>
                <tr><td style="color: #666;">Intermodal Role:</td><td>{node['intermodal']}</td></tr>
                <tr><td style="color: #666;">Dwell Transition:</td><td><span style="color: #D32F2F; font-weight: bold;">{node['dwell']}</span></td></tr>
                <tr><td style="color: #666;">Facility Type:</td><td>{node['role']}</td></tr>
            </table>
        </div>
        """

        if node["type"] == "seaport":
            icon_html = """
            <div style="background-color: #D50000; width: 22px; height: 22px; border-radius: 4px; border: 2px solid #FFF; box-shadow: 0 0 6px rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center;">
                <div style="width: 6px; height: 6px; background-color: #FFF; border-radius: 50%;"></div>
            </div>
            """
            icon_size = (22, 22)
            icon_anchor = (11, 11)
        elif node["type"] == "multi_line_oval":
            icon_html = """
            <div style="background-color: #1976D2; width: 30px; height: 16px; border-radius: 10px; border: 2px solid #FFF; box-shadow: 0 0 6px rgba(0,0,0,0.5);"></div>
            """
            icon_size = (30, 16)
            icon_anchor = (15, 8)
        else:  # single_line_circle
            icon_html = """
            <div style="background-color: #2E7D32; width: 14px; height: 14px; border-radius: 50%; border: 2px solid #FFF; box-shadow: 0 0 4px rgba(0,0,0,0.5);"></div>
            """
            icon_size = (14, 14)
            icon_anchor = (7, 7)

        folium.Marker(
            location=[node["lat"], node["lon"]],
            icon=DivIcon(icon_size=icon_size, icon_anchor=icon_anchor, html=icon_html),
            popup=folium.Popup(popup_content, max_width=320),
            tooltip=f"{node['name']} ({node['type'].replace('_', ' ')})"
        ).add_to(m)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    m.save(output_path)
    print(f"[ZeST Map Visualizer] Success: Saved map to {output_path}")

if __name__ == "__main__":
    generate_map()
