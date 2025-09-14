# backend.py
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="CTI Backend (demo)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for local demo - tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy base indicators (20 items)
SAMPLE = [
    "198.51.100.23", "203.0.113.15", "malicious-site.com", "phishing.example.net",
    "45.77.88.11", "192.0.2.5", "ransomware.badactor.org", "8.8.8.8",
    "133.45.66.77", "suspicious-download.io", "sqlinjection.test", "b0tnet.cc",
    "zero-day-exploit.net", "malwarehost.in", "exfil.domain.xyz",
    "trojan.fakeupdate.com", "adware.ads.example", "darkweb.shop",
    "bruteforce.attacker.com", "crypto-miner.node"
]

def score_by_rule(indicator):
    # simple heuristic scoring (demo)
    score = 50
    if any(ch in indicator for ch in [".exe", "malware", "ransom", "trojan"]):
        score += 30
    if indicator.count(".") >= 2:
        score += 5
    if indicator.isdigit() or indicator.replace(".", "").isdigit():
        score += 10
    # clamp
    return max(1, min(99, score + random.randint(-10, 10)))

def generate_alerts():
    alerts = []
    for i, ind in enumerate(SAMPLE):
        alerts.append({
            "id": i+1,
            "indicator": ind,
            "source": random.choice(["OTX","AbuseIPDB","VT","Internal"]),
            "type": "IP" if ind.replace(".","").isdigit() else "Domain",
            "cve": random.choice([None, "CVE-2024-1234", "CVE-2023-5678"]),
            "risk_score": score_by_rule(ind),
            "state": random.choice(["open","investigating","mitigated"]),
            "enrichment": {
                "first_seen": f"2025-09-{10 + (i % 20)}",
                "country": random.choice(["US","CN","RU","IN","BR","DE"]),
                "asn": 1000 + i,
                "whois": {"registrar": "DemoRegistrar", "age_days": 200 + i},
                "campaigns": ["APT-X"] if i % 5 == 0 else []
            }
        })
    return alerts

@app.get("/alerts")
async def get_alerts(top: int = 20):
    alerts = generate_alerts()
    return {"alerts": alerts[:top]}

class PlaybookRequest(BaseModel):
    indicator: str
    action: str

@app.post("/playbook/execute")
async def execute_playbook(req: PlaybookRequest):
    # In real product: call firewall, SIEM, orchestration APIs etc.
    # Here we simulate success
    return {"status":"ok", "indicator": req.indicator, "action": req.action}

@app.post("/block")
async def block_indicator(indicator: str = Body(..., embed=True)):
    return {"status": "blocked", "indicator": indicator}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)
