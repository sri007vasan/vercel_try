from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/")
async def telemetry(request: Request):
    body = await request.json()
    regions = body.get("regions", [])
    threshold = body.get("threshold_ms", 180)

    # Load telemetry bundle (JSON or CSV you downloaded)
    # For demo: assume it's JSON stored in the repo as telemetry.json
    with open("telemetry.json") as f:
        data = json.load(f)

    results = {}

    for region in regions:
        region_data = [rec for rec in data if rec["region"] == region]

        latencies = np.array([rec["latency_ms"] for rec in region_data])
        uptimes = np.array([rec["uptime"] for rec in region_data])

        avg_latency = float(latencies.mean())
        p95_latency = float(np.percentile(latencies, 95))
        avg_uptime = float(uptimes.mean())
        breaches = int(np.sum(latencies > threshold))

        results[region] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches,
        }

    return results
