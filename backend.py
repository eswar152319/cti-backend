# backend.py
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import random
import uvicorn

app = FastAPI()

# allow your frontend (localhost:3000) to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Dummy Threat Data ===
sample_indicators = [
    "198.51.100.23", "203.0.113.15", "malicious-site.com",
    "phishing.example.net", "45.77.88.11", "192.0.2.5",
    "ransomware.badactor.org", "8.8.8.8", "133.45.66.77",
    "suspicious-download.io", "sqlinjection.test", "b0tnet.cc",
    "zero-day-exploit.net", "malwarehost.in", "exfil.domain.xyz",
    "trojan.fakeupdate.com", "adware.ads.example", "darkweb.shop",
    "bruteforce.attacker.com", "crypto-miner.node"
]

def generate_alerts():
    alerts = []
    for ind in sample_indicators:
        alerts.append({
            "indicator": ind,
            "source": random.choice(["OTX", "AbuseIPDB", "VirusTotal"]),
            "type": random.choice(["IP", "Domain", "Hash"]),
            "cve": random.choice(["CVE-2024-1234", "CVE-2023-5678", None]),
            "risk_score": random.randint(10, 100),
            "state": random.choice(["Open", "Investigating", "Mitigated"]),
            "geo": random.choice(["US", "RU", "CN", "IN", "DE", "BR"]),
        })
    return alerts

@app.get("/alerts")
async def get_alerts():
    return {"alerts": generate_alerts()}

@app.post("/block")
async def block_indicator(indicator: str = Body(..., embed=True)):
    # simulate blocking
    return {"status": "blocked", "indicator": indicator}

# run: uvicorn backend:app --reload
if __name__ == "__main__":
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)
