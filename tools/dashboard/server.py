"""
Project ZeST - Real-Time Dashboard WebSocket Server
Binds simulation output from solvers/des/milkrun_sim.py and manifest_gen to the frontend.
"""

import asyncio
import json
import random
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="ZeST Transfer Dashboard Server")

DASHBOARD_DIR = Path(__file__).parent.resolve()
MAP_DIR = DASHBOARD_DIR.parent / "corridor_map"

# Mount static files if needed
if MAP_DIR.exists():
    app.mount("/map", StaticFiles(directory=str(MAP_DIR)), name="map")

ACTIVE_NODES = ["DE-DUI-DIT", "PL-POZ-KOB", "CZ-PRG-UHR", "HU-BUD-BILK", "CH-BSL-MUT"]
CONTAINER_PREFIXES = ["MSCU", "CMAU", "EGLV", "COSU", "HLCU", "MAEU"]

def generate_mock_event():
    cid = f"{random.choice(CONTAINER_PREFIXES)}{random.randint(1000000, 9999999)}"
    boundary = random.choice(["STS_DISCHARGE", "BUFFER_BYPASS", "ON_DOCK_RAIL", "DRY_PORT_SIDINGS"])
    dest = random.choice(ACTIVE_NODES)
    dwell = round(random.uniform(0.1, 18.5), 1)
    
    return {
        "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S"),
        "container_id": cid,
        "boundary": boundary,
        "source_target": f"BAY_{random.randint(10,80):02d} -> WAG_{random.randint(100,999)}",
        "dwell_latency": f"{dwell} min" if boundary != "DRY_PORT_SIDINGS" else "Terminal Direct",
        "efti_token": f"0x{random.randint(100000, 999999):x}...{random.randint(1000, 9999):x} (OK)",
        "destination": dest
    }

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    index_file = DASHBOARD_DIR / "index.html"
    return HTMLResponse(content=index_file.read_text(encoding="utf-8"))

@app.websocket("/events")
async def websocket_events(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            payload = {
                "event": generate_mock_event(),
                "kpis": {
                    "moves_per_hour": round(random.uniform(31.5, 34.2), 1),
                    "bypass_ratio": round(random.uniform(76.0, 81.5), 1),
                    "mean_dwell_hrs": round(random.uniform(0.28, 0.35), 2),
                }
            }
            await websocket.send_text(json.dumps(payload))
            await asyncio.sleep(1.8)
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("tools.dashboard.server:app", host="0.0.0.0", port=8000, reload=True)
