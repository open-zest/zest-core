#!/usr/bin/env python3
"""
Project ZeST - Pure Data-Driven 12-Swimlane Evolution Renderer
All domain data, phase geometry, and persona themes (Panasonic VSM, Google SDN, EU TEN-T)
live strictly in schemas/swimlane_phases.json.
"""

import argparse
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SCHEMA = ROOT_DIR / "schemas" / "swimlane_phases.json"
DEFAULT_OUTPUT = ROOT_DIR / "docs" / "zest_swimlane_evolution.html"


def build_swimlane_html(json_path: Path = DEFAULT_SCHEMA, output_path: Path = DEFAULT_OUTPUT) -> Path:
    with open(json_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    schema_json_str = json.dumps(schema, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{schema["metadata"]["title"]}</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            padding: 10px 18px;
            background: #0f172a;
            color: #f8fafc;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        .top-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #334155;
            padding-bottom: 8px;
            margin-bottom: 10px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .title-block h1 {{ margin: 0; font-size: 17px; color: #38bdf8; }}
        .title-block p {{ margin: 2px 0 0 0; font-size: 11px; color: #94a3b8; }}
        .toolbar {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
        .style-switcher, .zoom-controls {{
            display: flex;
            align-items: center;
            background: #1e293b;
            padding: 3px;
            border-radius: 7px;
            border: 1px solid #475569;
            gap: 3px;
        }}
        .style-btn {{
            background: transparent;
            color: #cbd5e1;
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 11.5px;
            font-weight: 700;
            cursor: pointer;
        }}
        .style-btn:hover {{ color: #ffffff; background: #334155; }}
        .style-btn.active-panasonic {{ background: #f59e0b; color: #0f172a; }}
        .style-btn.active-google {{ background: #1a73e8; color: #ffffff; }}
        .style-btn.active-eu {{ background: #003399; color: #ffcc00; border: 1px solid #ffcc00; }}
        .zoom-btn {{
            background: #334155;
            color: #f8fafc;
            border: none;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11.5px;
            font-weight: 700;
            cursor: pointer;
        }}
        .zoom-btn:hover {{ background: #0284c7; }}
        .zoom-label {{ font-size: 11px; font-weight: 600; color: #38bdf8; min-width: 44px; text-align: center; }}
        .controls {{ display: flex; gap: 5px; flex-wrap: wrap; }}
        .tab-btn {{
            background: #1e293b;
            color: #cbd5e1;
            border: 1px solid #475569;
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            cursor: pointer;
        }}
        .tab-btn:hover {{ background: #334155; color: #fff; }}
        .tab-btn.active {{ background: #0284c7; color: #fff; border-color: #38bdf8; }}
        .stage-container {{
            background: #ffffff;
            border-radius: 8px;
            padding: 8px 10px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.45);
            margin-bottom: 16px;
            overflow: auto;
        }}
        .stage-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #0f172a;
            color: #fff;
            padding: 6px 14px;
            border-radius: 5px;
            margin-bottom: 6px;
        }}
        .stage-header .phase-name {{ font-size: 13.5px; font-weight: 700; color: #38bdf8; }}
        .stage-header .phase-kpi {{
            font-size: 11px;
            font-weight: 600;
            color: #f8fafc;
            background: #1e293b;
            padding: 3px 10px;
            border-radius: 4px;
            border: 1px solid #334155;
        }}
        .svg-viewport {{ width: 100%; overflow: auto; display: flex; justify-content: center; align-items: flex-start; }}
        svg.swimlane-svg {{
            width: 100%;
            max-height: 78vh;
            height: auto;
            display: block;
            border: 1px solid #94a3b8;
            transform-origin: top center;
        }}
        .callout-card {{
            width: 100%;
            height: 100%;
            border-radius: 7px;
            padding: 6px 10px;
            box-shadow: 0 3px 8px rgba(0,0,0,0.22);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        .callout-panasonic {{ background: rgba(30, 64, 175, 0.94); border: 1.5px solid #1e3a8a; color: #ffffff; }}
        .callout-panasonic .callout-title {{ color: #fef08a; border-bottom: 1px solid rgba(254, 240, 138, 0.35); }}
        .callout-panasonic .callout-line {{ color: #f8fafc; }}
        .callout-google {{ background: rgba(255, 255, 255, 0.97); border: 1.5px solid #1a73e8; border-left: 5px solid #1a73e8; color: #202124; }}
        .callout-google .callout-title {{ color: #1a73e8; border-bottom: 1px solid #dadce0; }}
        .callout-google .callout-line {{ color: #3c4043; }}
        .callout-eu {{ background: rgba(0, 51, 153, 0.95); border: 1.5px solid #ffcc00; border-left: 5px solid #ffcc00; color: #ffffff; }}
        .callout-eu .callout-title {{ color: #ffcc00; border-bottom: 1px solid rgba(255, 204, 0, 0.4); }}
        .callout-eu .callout-line {{ color: #f1f5f9; }}
        .callout-title {{ font-size: 10.2px; font-weight: 700; margin-bottom: 3px; line-height: 1.2; padding-bottom: 2px; }}
        .callout-line {{ font-size: 9.2px; line-height: 1.26; margin: 1px 0; word-wrap: break-word; overflow-wrap: break-word; }}
        @media print {{
            body {{ background: #fff; color: #000; padding: 0; }}
            .toolbar {{ display: none; }}
            .stage-container {{ page-break-after: always; box-shadow: none; padding: 0; }}
            svg.swimlane-svg {{ max-height: none !important; width: 100% !important; }}
        }}
    </style>
</head>
<body>
    <div class="top-bar">
        <div class="title-block">
            <h1 id="main-title"></h1>
            <p id="main-subtitle"></p>
        </div>
        <div class="toolbar">
            <div class="style-switcher" id="persona-controls"></div>
            <div class="zoom-controls">
                <button class="zoom-btn" onclick="adjustZoom(-15)">−</button>
                <span class="zoom-label" id="zoom-readout">Fit</span>
                <button class="zoom-btn" onclick="adjustZoom(15)">+</button>
                <button class="zoom-btn" onclick="resetZoom()" style="font-weight:500;">Reset</button>
            </div>
            <div class="controls" id="tab-controls"></div>
        </div>
    </div>

    <div id="diagrams-root"></div>

    <script>
        const schema = {schema_json_str};
        const canvasCfg = schema.metadata.canvas;
        const LANE_H = canvasCfg.lane_height;
        const SVG_W = canvasCfg.svg_width;
        const SVG_H = schema.lanes.length * LANE_H;
        const LABEL_COL_W = canvasCfg.label_col_width;
        const BOX_H = canvasCfg.box_height;

        let currentStyle = Object.keys(schema.personas)[0];
        let currentMode = "phase_4";
        let currentZoom = 100;

        function adjustZoom(delta) {{
            currentZoom = Math.min(220, Math.max(55, currentZoom + delta));
            applyZoom();
        }}

        function resetZoom() {{
            currentZoom = 100;
            applyZoom();
        }}

        function applyZoom() {{
            document.getElementById("zoom-readout").textContent = currentZoom === 100 ? "Fit" : currentZoom + "%";
            document.querySelectorAll("svg.swimlane-svg").forEach(svg => {{
                svg.style.maxHeight = currentZoom === 100 ? "78vh" : "none";
                svg.style.width = currentZoom + "%";
            }});
        }}

        window.addEventListener("wheel", (e) => {{
            if (e.ctrlKey || e.metaKey) {{
                e.preventDefault();
                adjustZoom(e.deltaY < 0 ? 10 : -10);
            }}
        }}, {{ passive: false }});

        function getLaneTheme(laneIdx, defaultLane, pCfg) {{
            if (!pCfg.laneThemes) {{
                return {{
                    bg: defaultLane.bg,
                    label_bg: defaultLane.label_bg,
                    textColor: defaultLane.dark ? "#ffffff" : "#0f172a",
                    borderColor: "#cbd5e1"
                }};
            }}
            if (pCfg.laneThemes[String(laneIdx)]) return pCfg.laneThemes[String(laneIdx)];
            return laneIdx % 2 === 0 ? pCfg.laneThemes.even : pCfg.laneThemes.odd;
        }}

        function getLinkStyle(type, pCfg) {{
            const styles = {{
                "data":        {{ color: "#2563eb", width: 1.8, dash: "" }},
                "pink_ctrl":   {{ color: pCfg.ctrlLinkColor, width: 2.3, dash: pCfg.ctrlLinkDash || "" }},
                "phys":        {{ color: "#1e3a8a", width: 2.2, dash: "" }},
                "phys_heavy":  {{ color: "#dc2626", width: 3.0, dash: "" }},
                "phys_fast":   {{ color: "#059669", width: 3.2, dash: "" }},
                "phys_yellow": {{ color: pCfg.secondaryRailColor, width: 2.5, dash: "" }},
                "phys_dashed": {{ color: "#d97706", width: 2.0, dash: "5,4" }}
            }};
            return styles[type] || styles["phys"];
        }}

        function renderPhaseSVG(phase) {{
            const pCfg = schema.personas[currentStyle];
            let svg = `<svg class="swimlane-svg" viewBox="0 0 ${{SVG_W}} ${{SVG_H}}" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">`;

            svg += `
            <defs>
                <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%">
                    <feDropShadow dx="1" dy="2" stdDeviation="2" flood-opacity="0.22"/>
                </filter>
                <marker id="arrow-data" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb"/>
                </marker>
                <marker id="arrow-pink_ctrl" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1 L 10 5 L 0 9 z" fill="${{pCfg.ctrlLinkColor}}"/>
                </marker>
                <marker id="arrow-phys" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e3a8a"/>
                </marker>
                <marker id="arrow-phys_heavy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626"/>
                </marker>
                <marker id="arrow-phys_fast" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
                </marker>
                <marker id="arrow-phys_yellow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1 L 10 5 L 0 9 z" fill="${{pCfg.secondaryRailColor}}"/>
                </marker>
                <marker id="arrow-phys_dashed" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1 L 10 5 L 0 9 z" fill="#d97706"/>
                </marker>
            </defs>`;

            schema.lanes.forEach((lane, i) => {{
                const y = i * LANE_H;
                const theme = getLaneTheme(i, lane, pCfg);
                const lines = (pCfg.laneNames[i] || lane.name).split("\\n");

                svg += `<rect x="0" y="${{y}}" width="${{LABEL_COL_W}}" height="${{LANE_H}}" fill="${{theme.label_bg}}" stroke="#64748b" stroke-width="0.8"/>`;
                svg += `<rect x="${{LABEL_COL_W}}" y="${{y}}" width="${{SVG_W - LABEL_COL_W}}" height="${{LANE_H}}" fill="${{theme.bg}}" stroke="${{theme.borderColor}}" stroke-width="0.7"/>`;

                lines.forEach((lineText, idx) => {{
                    const ty = y + (lines.length === 1 ? 28 : (idx === 0 ? 20 : 34));
                    svg += `<text x="${{LABEL_COL_W - 8}}" y="${{ty}}" text-anchor="end" fill="${{theme.textColor}}" font-size="9.6" font-weight="${{idx === 0 ? '700' : '500'}}">${{lineText}}</text>`;
                }});
            }});

            const boxMap = {{}};
            phase.boxes.forEach(b => {{
                const y = b.lane * LANE_H + (LANE_H - BOX_H) / 2;
                const mappedText = (pCfg.boxTextMap && pCfg.boxTextMap[b.text]) || b.text;
                const widthAdjust = mappedText.length > 13 ? Math.max(b.w, mappedText.length * 6.5 + 14) : b.w;
                boxMap[b.id] = {{
                    ...b,
                    w: widthAdjust,
                    displayText: mappedText,
                    y: y,
                    h: BOX_H,
                    cx: b.x + widthAdjust / 2,
                    cy: y + BOX_H / 2
                }};
            }});

            phase.links.forEach(lk => {{
                const src = boxMap[lk.from];
                const dst = boxMap[lk.to];
                if (!src || !dst) return;

                const st = getLinkStyle(lk.type, pCfg);
                let d = "";

                if (lk.orth === "h") {{
                    const x1 = src.cx < dst.cx ? src.x + src.w : src.x;
                    const x2 = src.cx < dst.cx ? dst.x : dst.x + dst.w;
                    d = `M ${{x1}} ${{src.cy}} L ${{x2}} ${{dst.cy}}`;
                }} else if (lk.orth === "v") {{
                    const y1 = src.cy < dst.cy ? src.y + src.h : src.y;
                    const y2 = src.cy < dst.cy ? dst.y : dst.y + dst.h;
                    d = `M ${{src.cx}} ${{y1}} L ${{dst.cx}} ${{y2}}`;
                }} else if (lk.orth === "vh") {{
                    const y1 = src.cy < dst.cy ? src.y + src.h : src.y;
                    const x2 = src.cx < dst.cx ? dst.x : dst.x + dst.w;
                    d = `M ${{src.cx}} ${{y1}} L ${{src.cx}} ${{dst.cy}} L ${{x2}} ${{dst.cy}}`;
                }} else if (lk.orth === "hv") {{
                    const x1 = src.cx < dst.cx ? src.x + src.w : src.x;
                    const y2 = src.cy < dst.cy ? dst.y : dst.y + dst.h;
                    d = `M ${{x1}} ${{src.cy}} L ${{dst.cx}} ${{src.cy}} L ${{dst.cx}} ${{y2}}`;
                }} else if (lk.orth === "v_up") {{
                    d = `M ${{src.cx}} ${{src.y}} L ${{src.cx}} 24`;
                }} else {{
                    const y1 = src.cy < dst.cy ? src.y + src.h : src.y;
                    const y2 = src.cy < dst.cy ? dst.y : dst.y + dst.h;
                    d = `M ${{src.cx}} ${{y1}} L ${{dst.cx}} ${{y2}}`;
                }}

                const dashAttr = st.dash ? `stroke-dasharray="${{st.dash}}"` : "";
                svg += `<path d="${{d}}" fill="none" stroke="${{st.color}}" stroke-width="${{st.width}}" ${{dashAttr}} marker-end="url(#arrow-${{lk.type}})"/>`;

                if (lk.label) {{
                    const mx = (src.cx + dst.cx) / 2 + 5;
                    const my = (src.cy + dst.cy) / 2;
                    svg += `<rect x="${{mx - 4}}" y="${{my - 9}}" width="${{lk.label.length * 5.4 + 8}}" height="13" rx="3" fill="rgba(255,255,255,0.94)" stroke="${{st.color}}" stroke-width="0.8"/>`;
                    svg += `<text x="${{mx}}" y="${{my}}" fill="${{st.color}}" font-size="8.8" font-weight="700">${{lk.label}}</text>`;
                }}
            }});

            Object.values(boxMap).forEach(b => {{
                const st = pCfg.boxStyles[b.style] || pCfg.boxStyles["std"];
                svg += `<rect x="${{b.x}}" y="${{b.y}}" width="${{b.w}}" height="${{b.h}}" rx="${{st.rx}}" fill="${{st.fill}}" stroke="${{st.stroke}}" stroke-width="1.5" filter="url(#shadow)"/>`;
                svg += `<text x="${{b.cx}}" y="${{b.cy + 3.5}}" text-anchor="middle" fill="${{st.text}}" font-size="10.2" font-weight="${{st.weight}}">${{b.displayText}}</text>`;
            }});

            const activeCallouts = (pCfg.callouts && pCfg.callouts[phase.id]) ? pCfg.callouts[phase.id] : (phase.callouts || []);
            activeCallouts.forEach(c => {{
                const linesHtml = c.lines.map(ln => `<div class="callout-line">${{ln}}</div>`).join("");
                svg += `
                <foreignObject x="${{c.x}}" y="${{c.y * (LANE_H / 50)}}" width="${{c.w + 18}}" height="${{c.h + 14}}">
                    <div xmlns="http://www.w3.org/1999/xhtml" class="callout-card callout-${{currentStyle}}">
                        <div class="callout-title">${{c.title}}</div>
                        ${{linesHtml}}
                    </div>
                </foreignObject>`;
            }});

            svg += `
            <g filter="url(#shadow)">
                <rect x="922" y="60" width="146" height="72" rx="6" fill="${{pCfg.badgeBg}}" stroke="${{pCfg.badgeBorder}}" stroke-width="1.8"/>
                <text x="995" y="79" text-anchor="middle" fill="#e2e8f0" font-size="9.5" font-weight="600">${{pCfg.badgeHeader1}}</text>
                <text x="995" y="92" text-anchor="middle" fill="#e2e8f0" font-size="9.5" font-weight="600">${{pCfg.badgeHeader2}}</text>
                <text x="995" y="113" text-anchor="middle" fill="${{pCfg.badgeValColor}}" font-size="15.5" font-weight="800">${{phase.breakeven}}</text>
                <text x="995" y="125" text-anchor="middle" fill="#cbd5e1" font-size="8.2">${{phase.breakeven_sub}}</text>
            </g></svg>`;
            return svg;
        }}

        function setStyle(styleKey) {{
            currentStyle = styleKey;
            const pCfg = schema.personas[currentStyle];
            document.getElementById("main-title").textContent = pCfg.title;
            document.getElementById("main-subtitle").textContent = pCfg.subtitle;

            Object.keys(schema.personas).forEach(k => {{
                const btn = document.getElementById("btn-style-" + k);
                btn.className = "style-btn" + (k === styleKey ? " active-" + k : "");
            }});
            selectView(currentMode);
        }}

        function selectView(mode) {{
            currentMode = mode;
            const root = document.getElementById("diagrams-root");
            root.innerHTML = "";

            document.querySelectorAll(".tab-btn").forEach(btn => {{
                btn.classList.toggle("active", btn.dataset.mode === mode);
            }});

            const phasesToRender = mode === "all" ? schema.phases : schema.phases.filter(p => p.id === mode);
            phasesToRender.forEach(p => {{
                const card = document.createElement("div");
                card.className = "stage-container";
                card.innerHTML = `
                    <div class="stage-header">
                        <div class="phase-name">${{p.tab_label}} — [${{currentStyle.toUpperCase()}} VIEW]</div>
                        <div class="phase-kpi">${{p.dwell_kpi}}</div>
                    </div>
                    <div class="svg-viewport">${{renderPhaseSVG(p)}}</div>
                `;
                root.appendChild(card);
            }});
            applyZoom();
        }}

        const personaBar = document.getElementById("persona-controls");
        Object.entries(schema.personas).forEach(([key, cfg]) => {{
            const b = document.createElement("button");
            b.className = "style-btn";
            b.id = "btn-style-" + key;
            b.textContent = cfg.button_label;
            b.onclick = () => setStyle(key);
            personaBar.appendChild(b);
        }});

        const ctrlBar = document.getElementById("tab-controls");
        schema.phases.forEach(p => {{
            const b = document.createElement("button");
            b.className = "tab-btn";
            b.dataset.mode = p.id;
            b.textContent = p.tab_label;
            b.onclick = () => selectView(p.id);
            ctrlBar.appendChild(b);
        }});

        const allBtn = document.createElement("button");
        allBtn.className = "tab-btn";
        allBtn.dataset.mode = "all";
        allBtn.textContent = "Show All 4 Phases";
        allBtn.onclick = () => selectView("all");
        ctrlBar.appendChild(allBtn);

        setStyle(currentStyle);
    </script>
</body>
</html>
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build ZeST 12-Swimlane Evolution HTML from JSON config.")
    parser.add_argument("--config", type=Path, default=DEFAULT_SCHEMA, help="Path to swimlane JSON schema")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Path to output HTML file")
    args = parser.parse_args()
    out = build_swimlane_html(args.config, args.output)
    print(f"[ZeST Swimlane Renderer] Success: Built {out} from {args.config}")
