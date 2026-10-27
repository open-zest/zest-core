import base64
import json
import urllib.request
import os

def render_mmd_to_svg(mmd_path, output_svg_path):
    if not os.path.exists(mmd_path):
        print(f"Error: {mmd_path} does not exist.")
        return False
        
    with open(mmd_path, "r", encoding="utf-8") as f:
        diagram_code = f.read()

    # Encode mermaid syntax for mermaid.ink service
    graph_obj = {
        "code": diagram_code,
        "mermaid": {
            "theme": "default"
        }
    }
    encoded_json = json.dumps(graph_obj).encode("utf-8")
    b64_str = base64.urlsafe_b64encode(encoded_json).decode("ascii")
    
    url = f"https://mermaid.ink/svg/{b64_str}"
    
    try:
        req = urllib.request.Request(
            url, 
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req) as response:
            svg_data = response.read().decode("utf-8")
            
        with open(output_svg_path, "w", encoding="utf-8") as out:
            out.write(svg_data)
            
        print(f"Exported: {output_svg_path}")
        return True
    except Exception as e:
        print(f"Failed to fetch SVG from service for {mmd_path}: {e}")
        return False

def main():
    os.makedirs("docs/diagrams/exports", exist_ok=True)
    
    diagrams = [
        ("docs/diagrams/data_vs_physical_flow.mmd", "docs/diagrams/exports/data_vs_physical_flow.svg"),
        ("docs/diagrams/transition_architecture.mmd", "docs/diagrams/exports/transition_architecture.svg"),
    ]
    
    for src, dest in diagrams:
        render_mmd_to_svg(src, dest)

if __name__ == "__main__":
    main()
