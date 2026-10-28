#!/usr/bin/env python3
"""
Project ZeST - NSRM Corridor Map Visualizer
Loads corridor network topology from JSON and renders an interactive Leaflet map
with tentative downstream ZeST destination zones.
"""

import json
import os
import folium
from folium import DivIcon

def generate_map(
    data_path="tools/corridor_map/corridor_data.json",
    output_path="tools/corridor_map/corridor_nsrm_map.html"
):
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    m = folium.Map(
        location=data.get("center", [51.2, 13.5]),
        zoom_start=data.get("zoom_start", 6),
        tiles="OpenStreetMap",
        control_scale=True
    )

    # 1. Render transit lines
    for line in data.get("lines", []):
        meta = line.get("meta", {})
        popup_html = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; min-width: 260px;">
            <h4 style="margin: 0 0 6px 0; color: {line['color']};">{line['name']}</h4>
            <table style="width: 100%; font-size: 12px; border-collapse: collapse; line-height: 1.4;">
                <tr><td style="color: #666;">Corridor:</td><td><b>{meta.get('rfc', 'N/A')}</b></td></tr>
                <tr><td style="color: #666;">Capacity:</td><td><b>{meta.get('capacity', 'N/A')}</b></td></tr>
                <tr><td style="color: #666;">Signaling:</td><td>{meta.get('signaling', 'N/A')}</td></tr>
                <tr><td style="color: #666;">Traction:</td><td>{meta.get('traction', 'N/A')}</td></tr>
                <tr><td style="color: #666;">Max Length:</td><td>{meta.get('max_length', 'N/A')}</td></tr>
                <tr><td style="color: #666;">P400 Gauge:</td><td>{meta.get('p400', 'N/A')}</td></tr>
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

    # 2. Render Downstream Catchment Zones (Circles around Dry Ports)
    for node in data.get("nodes", []):
        if "radius_km" in node:
            folium.Circle(
                location=[node["lat"], node["lon"]],
                radius=node["radius_km"] * 1000,
                color=node.get("zone_color", "#1976D2"),
                fill=True,
                fill_color=node.get("zone_color", "#1976D2"),
                fill_opacity=0.15,
                weight=1.5,
                dash_array="4, 6",
                tooltip=f"Hinterland Catchment: {node.get('zone_label', node['zone'])}"
            ).add_to(m)

    # 3. Render Nodes
    for node in data.get("nodes", []):
        zone_header = ""
        if "zone" in node and node["zone"] not in ["ORIGIN_GATEWAY", "CORRIDOR_JUNCTION", "CORRIDOR_SIDING"]:
            zone_header = f"""
            <div style="background-color: {node.get('zone_color', '#333')}; color: #fff; padding: 3px 6px; border-radius: 3px; font-size: 11px; font-weight: bold; margin-bottom: 6px; display: inline-block;">
                ZeST Queue: {node['zone']}
            </div>
            """

        popup_content = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; min-width: 250px;">
            {zone_header}
            <div style="border-bottom: 2px solid #00838F; padding-bottom: 4px; margin-bottom: 8px;">
                <span style="font-size: 10px; text-transform: uppercase; letter-spacing: 1px; color: #888;">{node['type'].replace('_', ' ')}</span>
                <h3 style="margin: 2px 0 0 0; font-size: 14px; color: #111;">{node['name']}</h3>
            </div>
            <table style="width: 100%; font-size: 12px; color: #333; line-height: 1.5;">
                <tr><td style="color: #666;">Capacity/Vol:</td><td><b>{node['throughput']}</b></td></tr>
                <tr><td style="color: #666;">Intermodal Role:</td><td>{node['intermodal']}</td></tr>
                <tr><td style="color: #666;">Dwell Impact:</td><td><span style="color: #D32F2F; font-weight: bold;">{node['dwell']}</span></td></tr>
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
            badge_color = node.get("zone_color", "#1976D2")
            icon_html = f"""
            <div style="background-color: {badge_color}; width: 30px; height: 16px; border-radius: 10px; border: 2px solid #FFF; box-shadow: 0 0 6px rgba(0,0,0,0.5);"></div>
            """
            icon_size = (30, 16)
            icon_anchor = (15, 8)
        else:  # single_line_circle
            badge_color = node.get("zone_color", "#2E7D32")
            icon_html = f"""
            <div style="background-color: {badge_color}; width: 14px; height: 14px; border-radius: 50%; border: 2px solid #FFF; box-shadow: 0 0 4px rgba(0,0,0,0.5);"></div>
            """
            icon_size = (14, 14)
            icon_anchor = (7, 7)

        folium.Marker(
            location=[node["lat"], node["lon"]],
            icon=DivIcon(icon_size=icon_size, icon_anchor=icon_anchor, html=icon_html),
            popup=folium.Popup(popup_content, max_width=320),
            tooltip=f"{node['name']} ({node.get('zone', node['type'])})"
        ).add_to(m)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    m.save(output_path)
    print(f"[ZeST Map Visualizer] Success: Saved map to {output_path}")

if __name__ == "__main__":
    generate_map()
