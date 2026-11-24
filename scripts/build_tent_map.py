import csv
import xml.etree.ElementTree as ET
from pathlib import Path
import folium

DATA_DIR = Path("data/maps")
OUT_HTML = Path("docs/assets/maps/zest_tent_network.html")
OUT_HTML.parent.mkdir(parents=True, exist_ok=True)

# 1. Base map (OpenStreetMap — free, no API key required)
m = folium.Map(
    location=[48.5, 11.5],
    zoom_start=5,
    tiles="OpenStreetMap",
    control_scale=True,
)

# 2. Toggleable Layer Groups
fg_catchments = folium.FeatureGroup(name="11 Seaport Catchment Zones (Voronoi)", show=False)
fg_corridors = folium.FeatureGroup(name="TEN-T Rail Corridors (18 Spines)", show=True)
fg_overreach = folium.FeatureGroup(name="Legacy North-Range Overreach", show=False)
fg_rad_300 = folium.FeatureGroup(name="OTR Radius: 300 km (Breakeven)", show=False)
fg_rad_150 = folium.FeatureGroup(name="OTR Radius: 150 km (Single-Day)", show=True)
fg_borders = folium.FeatureGroup(name="Rail Border Crossings (14 Chokepoints)", show=False)
fg_seaports = folium.FeatureGroup(name="Seaport Gateways (17)", show=True)
fg_dryports = folium.FeatureGroup(name="Inland Dry Ports", show=True)

# Core European Inland Dry Ports (aligned to CSV catchments + ZeST benchmark zones)
DRY_PORTS = [
    ("Duisburg (DIT / D3T)", 51.4344, 6.7623, "ZONE_A_DUI — Rhine-Ruhr Intermodal Hub"),
    ("Verona (Quadrante Europa)", 45.4150, 10.9450, "ZONE_B_VER — Brenner / North Italy Hub"),
    ("Poznań (CLIP Swarzędz)", 52.4064, 17.0785, "ZONE_C_POZ — Poland East-West Hub"),
    ("Vienna (WienCont)", 48.1650, 16.4750, "ZONE_D_VIE — Danube / CEE Gateway"),
    ("Lyon (Terminal de Vénissieux)", 45.7080, 4.8860, "ZONE_E_LYO — Rhône-Alpes Hub"),
    ("Budapest (BILK)", 47.3920, 19.0850, "ZONE_F_BUD — Central/SE Europe Hub"),
    ("Munich (München-Riem)", 48.1480, 11.6960, "Bavaria / Alpine Rail Hub"),
    ("Milan (Melzo / RHM)", 45.4980, 9.4230, "Lombardy Intermodal Hub"),
    ("Madrid (Coslada Dry Port)", 40.4238, -3.5613, "Iberian Central Dry Port"),
    ("Zaragoza (tmZ / PLAZA)", 41.6488, -0.8891, "Ebro Corridor Dry Port"),
    ("Prague (Uhříněves / METRANS)", 50.0300, 14.6000, "Czech Rail Hub"),
    ("Bratislava / Dunajská Streda", 47.9928, 17.6121, "Slovakia Automotive Rail Hub"),
    ("Belgrade (Nelt / Dobanovci)", 44.8260, 20.2250, "Western Balkans Hub"),
    ("Zagreb (Jankomir)", 45.8000, 15.8600, "Croatia Inland Rail Hub"),
    ("Graz (Cargo Center Graz)", 46.9420, 15.4320, "Styria / Adriatic Rail Hub"),
    ("Ostrava (Paskov)", 49.7300, 18.2900, "Silesia / Northern CEE Hub"),
    ("Basel (Frenkendorf / Kleinhüningen)", 47.5830, 7.5890, "Swiss Rhine-Alpine Hub"),
    ("Curtici / Arad (Railport Arad)", 46.3420, 21.3060, "Romania Western Border Dry Port"),
]

# High-Friction Rail Border Crossings (voltage, gauge, signaling, customs/eFTI)
BORDER_CROSSINGS = [
    ("Emmerich–Zevenaar (NL/DE)", 51.8350, 6.2420, "Betuweroute bottleneck; 1.5kV DC / 15kV AC & signaling handoff"),
    ("Brenner (AT/IT)", 47.0050, 11.5060, "Alpine gradient; 15kV AC / 3kV DC voltage & signaling swap"),
    ("Chiasso (CH/IT)", 45.8330, 9.0310, "Gotthard southern gate; Swiss/Italian voltage & customs handoff"),
    ("Basel Bad / Muttenz (DE/CH)", 47.5670, 7.6070, "Rhine-Alpine non-EU customs & transit formalities"),
    ("Portbou / Cerbère (ES/FR)", 42.4260, 3.1590, "Mediterranean Iberian (1668 mm) to standard (1435 mm) gauge break"),
    ("Irún / Hendaye (ES/FR)", 43.3390, -1.7890, "Atlantic Corridor Iberian-to-standard gauge break"),
    ("Frankfurt (Oder) (DE/PL)", 52.3410, 14.5500, "15kV AC / 3kV DC swap & crew/language handoff"),
    ("Passau (DE/AT)", 48.5740, 13.4510, "Rhine-Danube corridor operational & crew handoff"),
    ("Hegyeshalom (AT/HU)", 47.9120, 17.1520, "15kV AC / 25kV AC voltage swap; high-volume CEE rail gate"),
    ("Štúrovo / Szob (SK/HU)", 47.8000, 18.7200, "Danube north-bank freight corridor border"),
    ("Spielfeld-Straß (AT/SI)", 46.7070, 15.6350, "15kV AC / 3kV DC swap; Baltic-Adriatic pinch point"),
    ("Curtici–Lőkösháza (RO/HU)", 46.3420, 21.3060, "Constanța corridor locomotive/crew handoff & border checks"),
    ("Subotica–Kelebia (RS/HU)", 46.1660, 19.6160, "EU external border; customs, phytosanitary & eFTI/ICS2 checks"),
    ("Małaszewicze–Brest (PL/BY)", 52.0230, 23.5160, "EU external border + 1520 mm broad-to-standard gauge transshipment"),
]

for name, lat, lon, desc in DRY_PORTS:
    folium.CircleMarker(
        location=[lat, lon],
        radius=5,
        color="#1e3a8a",
        fill=True,
        fill_color="#3b82f6",
        fill_opacity=0.95,
        popup=folium.Popup(f"<b>{name}</b><br>{desc}", max_width=260),
        tooltip=name,
    ).add_to(fg_dryports)

    # 150 km single-day drayage ring
    folium.Circle(
        location=[lat, lon],
        radius=150_000,
        color="#2563eb",
        weight=1.2,
        opacity=0.65,
        fill=True,
        fill_color="#3b82f6",
        fill_opacity=0.07,
        tooltip=f"{name} — 150 km OTR",
    ).add_to(fg_rad_150)

    # 300 km breakeven ring (dashed, off by default)
    folium.Circle(
        location=[lat, lon],
        radius=300_000,
        color="#d97706",
        weight=1.0,
        opacity=0.6,
        dash_array="5, 5",
        fill=True,
        fill_color="#f59e0b",
        fill_opacity=0.04,
        tooltip=f"{name} — 300 km Breakeven",
    ).add_to(fg_rad_300)

for name, lat, lon, desc in BORDER_CROSSINGS:
    folium.RegularPolygonMarker(
        location=[lat, lon],
        number_of_sides=4,
        rotation=45,
        radius=7,
        color="#991b1b",
        weight=1.5,
        fill=True,
        fill_color="#f59e0b",
        fill_opacity=0.95,
        popup=folium.Popup(f"<b>Border Chokepoint: {name}</b><br>{desc}", max_width=280),
        tooltip=f"Border: {name}",
    ).add_to(fg_borders)


def parse_coords(coord_text: str):
    coords = []
    for token in coord_text.strip().split():
        parts = token.split(",")
        if len(parts) >= 2:
            coords.append((float(parts[1]), float(parts[0])))
    return coords


def load_kml_lines(kml_path: Path, target_fg, color: str, weight: float, dash: str = None):
    if not kml_path.exists():
        return
    tree = ET.parse(kml_path)
    root = tree.getroot()
    ns = {"kml": "http://www.opengis.net/kml/2.2"}

    for pm in root.findall(".//kml:Placemark", ns):
        name_el = pm.find("kml:name", ns)
        desc_el = pm.find("kml:description", ns)
        name = name_el.text.strip() if name_el is not None and name_el.text else "Corridor"
        desc = desc_el.text.strip() if desc_el is not None and desc_el.text else ""

        for line in pm.findall(".//kml:LineString/kml:coordinates", ns):
            if line.text:
                coords = parse_coords(line.text)
                if coords:
                    kwargs = dict(
                        locations=coords,
                        color=color,
                        weight=weight,
                        opacity=0.85,
                        tooltip=name,
                        popup=folium.Popup(f"<b>{name}</b><br>{desc}", max_width=300),
                    )
                    if dash:
                        kwargs["dash_array"] = dash
                    folium.PolyLine(**kwargs).add_to(target_fg)


def load_kml_polygons(kml_path: Path, target_fg):
    if not kml_path.exists():
        return
    tree = ET.parse(kml_path)
    root = tree.getroot()
    ns = {"kml": "http://www.opengis.net/kml/2.2"}
    palette = [
        "#0ea5e9", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899",
        "#14b8a6", "#f97316", "#6366f1", "#84cc16", "#06b6d4", "#ef4444"
    ]

    for idx, pm in enumerate(root.findall(".//kml:Placemark", ns)):
        name_el = pm.find("kml:name", ns)
        desc_el = pm.find("kml:description", ns)
        name = name_el.text.strip() if name_el is not None and name_el.text else "Catchment"
        desc = desc_el.text.strip() if desc_el is not None and desc_el.text else ""
        color = palette[idx % len(palette)]

        for ring in pm.findall(".//kml:Polygon//kml:outerBoundaryIs//kml:coordinates", ns):
            if ring.text:
                coords = parse_coords(ring.text)
                if coords:
                    folium.Polygon(
                        locations=coords,
                        color=color,
                        weight=1.5,
                        opacity=0.8,
                        fill=True,
                        fill_color=color,
                        fill_opacity=0.15,
                        tooltip=name,
                        popup=folium.Popup(f"<b>{name}</b><br>{desc}", max_width=300),
                    ).add_to(target_fg)


def load_seaports_csv(csv_path: Path):
    if not csv_path.exists():
        return
    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("Port Name", "").strip()
            lat = row.get("Latitude", "").strip()
            lon = row.get("Longitude", "").strip()
            if not (name and lat and lon):
                continue

            popup_html = f"""
            <div style="font-family: sans-serif; font-size: 12px; line-height: 1.4;">
                <b>{name}</b><br>
                <b>Domain:</b> {row.get('Domain', '')}<br>
                <b>Carrier / Equity:</b> {row.get('Carrier Equity', '')}<br>
                <b>EU Rail Corridor:</b> {row.get('EU Rail Corridor', '')}<br>
                <b>Dry-Port Catchments:</b> {row.get('Inland Dry-Port Catchments', '')}<br>
                <b>Vessel Time Saved:</b> {row.get('Vessel Round-Trip Saved', '')}<br>
                <b>Key Shippers:</b> {row.get('Key Shippers', '')}
            </div>
            """
            folium.Marker(
                location=[float(lat), float(lon)],
                icon=folium.Icon(color="darkblue", icon="anchor", prefix="fa"),
                popup=folium.Popup(popup_html, max_width=340),
                tooltip=name,
            ).add_to(fg_seaports)


# Load all 4 files
load_kml_polygons(DATA_DIR / "zest_eu_11_catchment_zones.kml", fg_catchments)
load_kml_lines(DATA_DIR / "zest_rail_corridors_complete_lines.kml", fg_corridors, color="#1e293b", weight=2.5)
load_kml_lines(DATA_DIR / "zest_legacy_overreach_lines.kml", fg_overreach, color="#dc2626", weight=2.2, dash="6, 6")
load_seaports_csv(DATA_DIR / "zest_seaports_complete_17_gateways.csv")

# Add layers in visual z-order
for fg in [fg_catchments, fg_rad_300, fg_rad_150, fg_corridors, fg_overreach, fg_seaports, fg_dryports, fg_borders]:
    fg.add_to(m)

folium.LayerControl(collapsed=False).add_to(m)
m.save(str(OUT_HTML))
print(f"Saved map to {OUT_HTML}")
