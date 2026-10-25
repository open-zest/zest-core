"""
Reads schemas/system_architecture.json and outputs a GitHub-ready Mermaid diagram.
"""

import json
from pathlib import Path

SCHEMA_PATH = Path("schemas/system_architecture.json")
OUTPUT_PATH = Path("docs/architecture_diagram.md")


def generate_mermaid():
    if not SCHEMA_PATH.exists():
        print(f"Error: {SCHEMA_PATH} not found.")
        return

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    lines = ["```mermaid", "graph TD"]

    # Subgraphs by layer
    for layer in data["layers"]:
        l_id = layer["id"]
        l_name = layer["name"]
        lines.append(f"    subgraph {l_id}[\"{l_name}\"]")
        for block in data["blocks"]:
            if block["layer"] == l_id:
                b_id = block["id"]
                b_name = block["name"]
                lines.append(f"        {b_id}[\"{b_name}\"]")
        lines.append("    end")

    lines.append("")

    # Edge flows
    for flow in data["flows"]:
        src = flow["source"]
        tgt = flow["target"]
        lbl = flow.get("content") or flow.get("condition") or flow["type"]

        if flow["type"] == "DATA_TOKEN":
            lines.append(f"    {src} -. \"{lbl}\" .-> {tgt}")
        else:
            lines.append(f"    {src} == \"{lbl}\" ==> {tgt}")

    lines.append("```")
    output = "\n".join(lines)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"Rendered architecture diagram to {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_mermaid()
