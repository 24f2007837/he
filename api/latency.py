from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Embedded telemetry data from q-vercel-latency.json
TELEMETRY_DATA = [
  {"region": "apac", "service": "payments", "latency_ms": 214.35, "uptime_pct": 98.377, "timestamp": 20250301},
  {"region": "apac", "service": "catalog", "latency_ms": 134.68, "uptime_pct": 97.717, "timestamp": 20250302},
  {"region": "apac", "service": "catalog", "latency_ms": 227.42, "uptime_pct": 97.123, "timestamp": 20250303},
  {"region": "apac", "service": "checkout", "latency_ms": 169.01, "uptime_pct": 97.375, "timestamp": 20250304},
  {"region": "apac", "service": "support", "latency_ms": 163.57, "uptime_pct": 98.685, "timestamp": 20250305},
  {"region": "apac", "service": "recommendations", "latency_ms": 204.04, "uptime_pct": 97.819, "timestamp": 20250306},
  {"region": "apac", "service": "analytics", "latency_ms": 130.99, "uptime_pct": 98.443, "timestamp": 20250307},
  {"region": "apac", "service": "recommendations", "latency_ms": 223.39, "uptime_pct": 99.168, "timestamp": 20250308},
  {"region": "apac", "service": "payments", "latency_ms": 124.19, "uptime_pct": 98.036, "timestamp": 20250309},
  {"region": "apac", "service": "support", "latency_ms": 205.05, "uptime_pct": 98.345, "timestamp": 20250310},
  {"region": "apac", "service": "support", "latency_ms": 201.94, "uptime_pct": 98.581, "timestamp": 20250311},
  {"region": "apac", "service": "support", "latency_ms": 175.77, "uptime_pct": 98.233, "timestamp": 20250312},
  {"region": "emea", "service": "support", "latency_ms": 213.93, "uptime_pct": 98.99, "timestamp": 20250301},
  {"region": "emea", "service": "checkout", "latency_ms": 190.58, "uptime_pct": 98.378, "timestamp": 20250302},
  {"region": "emea", "service": "checkout", "latency_ms": 185.37, "uptime_pct": 98.895, "timestamp": 20250303},
  {"region": "emea", "service": "support", "latency_ms": 134.64, "uptime_pct": 97.154, "timestamp": 20250304},
  {"region": "emea", "service": "recommendations", "latency_ms": 191.01, "uptime_pct": 97.521, "timestamp": 20250305},
  {"region": "emea", "service": "checkout", "latency_ms": 158.44, "uptime_pct": 99.446, "timestamp": 20250306},
  {"region": "emea", "service": "catalog", "latency_ms": 139.92, "uptime_pct": 98.46, "timestamp": 20250307},
  {"region": "emea", "service": "recommendations", "latency_ms": 164.26, "uptime_pct": 98.97, "timestamp": 20250308},
  {"region": "emea", "service": "checkout", "latency_ms": 124.12, "uptime_pct": 98.351, "timestamp": 20250309},
  {"region": "emea", "service": "support", "latency_ms": 224.64, "uptime_pct": 98.2, "timestamp": 20250310},
  {"region": "emea", "service": "catalog", "latency_ms": 192.48, "uptime_pct": 97.905, "timestamp": 20250311},
  {"region": "emea", "service": "catalog", "latency_ms": 118.87, "uptime_pct": 99.014, "timestamp": 20250312},
  {"region": "amer", "service": "checkout", "latency_ms": 224.52, "uptime_pct": 99.243, "timestamp": 20250301},
  {"region": "amer", "service": "support", "latency_ms": 203.51, "uptime_pct": 98.156, "timestamp": 20250302},
  {"region": "amer", "service": "payments", "latency_ms": 120.92, "uptime_pct": 99.068, "timestamp": 20250303},
  {"region": "amer", "service": "analytics", "latency_ms": 126.54, "uptime_pct": 98.17, "timestamp": 20250304},
  {"region": "amer", "service": "support", "latency_ms": 226.56, "uptime_pct": 98.356, "timestamp": 20250305},
  {"region": "amer", "service": "checkout", "latency_ms": 143.37, "uptime_pct": 97.489, "timestamp": 20250306},
  {"region": "amer", "service": "support", "latency_ms": 205.95, "uptime_pct": 98.333, "timestamp": 20250307},
  {"region": "amer", "service": "catalog", "latency_ms": 103.42, "uptime_pct": 99.134, "timestamp": 20250308},
  {"region": "amer", "service": "catalog", "latency_ms": 202.01, "uptime_pct": 99.007, "timestamp": 20250309},
  {"region": "amer", "service": "analytics", "latency_ms": 230.37, "uptime_pct": 99.331, "timestamp": 20250310},
  {"region": "amer", "service": "checkout", "latency_ms": 103.61, "uptime_pct": 99.403, "timestamp": 20250311},
  {"region": "amer", "service": "checkout", "latency_ms": 170.34, "uptime_pct": 98.126, "timestamp": 20250312}
]

df = pd.DataFrame(TELEMETRY_DATA)

@app.post("/api/latency")
async def analyze_latency(request: Request):
    body = await request.json()
    regions = body.get("regions", [])
    threshold_ms = body.get("threshold_ms", 180)
    
    response = {}
    for r in regions:
        sub = df[df['region'] == r]
        if sub.empty:
            response[r] = {
                "avg_latency": 0.0,
                "p95_latency": 0.0,
                "avg_uptime": 0.0,
                "breaches": 0
            }
        else:
            avg_latency = float(sub['latency_ms'].mean())
            p95_latency = float(np.percentile(sub['latency_ms'], 95))
            avg_uptime = float(sub['uptime_pct'].mean())
            breaches = int((sub['latency_ms'] > threshold_ms).sum())
            response[r] = {
                "avg_latency": avg_latency,
                "p95_latency": p95_latency,
                "avg_uptime": avg_uptime,
                "breaches": breaches
            }
    return response