import os
import webbrowser

def build_preview():
    flow_file = "docs/diagrams/data_vs_physical_flow.mmd"
    arch_file = "docs/diagrams/transition_architecture.mmd"

    with open(flow_file, "r") as f:
        flow_src = f.read()
    with open(arch_file, "r") as f:
        arch_src = f.read()

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Project ZeST - System Architecture Verification</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({{startOnLoad: true, theme: 'default'}});</script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 40px; background: #fafbfc; color: #24292e; }}
        .card {{ background: #ffffff; border: 1px solid #e1e4e8; border-radius: 6px; padding: 24px; margin-bottom: 32px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }}
        h1 {{ border-bottom: 1px solid #eaecef; padding-bottom: 12px; }}
        h2 {{ color: #0366d6; margin-top: 0; }}
    </style>
</head>
<body>
    <h1>Project ZeST: Architecture Verification View</h1>
    <div class="card">
        <h2>1. Data Flow vs. Physical Flow (Advance eFTI Tokenization)</h2>
        <pre class="mermaid">
{flow_src}
        </pre>
    </div>
    <div class="card">
        <h2>2. Transition Points: Legacy Baseline vs. ZeST Architecture</h2>
        <pre class="mermaid">
{arch_src}
        </pre>
    </div>
</body>
</html>"""

    out_path = os.path.abspath("docs/diagrams/preview.html")
    with open(out_path, "w") as f:
        f.write(html)
    print(f"Generated preview at: {out_path}")
    webbrowser.open(f"file://{out_path}")

if __name__ == "__main__":
    build_preview()
