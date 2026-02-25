# AI Legal Assistant Subnet

**Subnet #5 — Bittensor Ideathon**

A decentralized legal advisory platform on Bittensor. Miners compete to provide the most accurate legal analysis across multiple jurisdictions. Validators verify legal references and advice quality against authoritative legal databases. Rewards ($TAO) are distributed via Yuma Consensus.

## Quick Start (For Judges)

```bash
# 1. Clone & enter directory
git clone https://github.com/yt2025id-lab/bittensor-legal.git
cd bittensor-legal

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn main:app --reload --port 8000

# 4. Open in browser
open http://localhost:8000
```

### What You'll See

- **Interactive Web UI** at `http://localhost:8000` — click any of the 3 demo scenarios
- **Swagger API Docs** at `http://localhost:8000/docs` — test all endpoints interactively
- **ReDoc** at `http://localhost:8000/redoc` — clean API reference

### Demo Scenarios

| # | Scenario | Task Type |
|---|----------|-----------|
| 1 | Cross-border IP infringement — US/EU jurisdiction | Legal Analysis |
| 2 | Smart contract dispute — DeFi protocol liability | Contract Review |
| 3 | Data privacy compliance — GDPR vs CCPA assessment | Compliance Check |

Each demo broadcasts a legal challenge to 6 simulated miners, scores their analysis through 3-4 validators, and distributes TAO rewards via Yuma Consensus.

## Features

- 6 specialized legal AI miners (LegalBERT, StatuteNet, CaseLaw-GPT, etc.)
- 3-4 validators with legal database verification pipelines
- Multi-jurisdiction legal analysis with citation references
- Real-time scoring: citation accuracy, relevance, completeness, latency
- TAO reward distribution via Yuma Consensus
- Full miner/validator CRUD, leaderboard, and network status APIs

## Folder Structure

```
main.py                  # FastAPI entry point
legal/
  __init__.py
  ai.py                  # AI legal analysis engine (3 demo scenarios, 6 miners)
  db.py                  # In-memory DB (miners, validators, challenges)
  models.py              # Pydantic data models
  routes.py              # 20+ API endpoints
static/
  index.html             # Interactive demo UI
  app.js                 # Frontend logic
  style.css              # Dark theme styling
overview.md              # Full technical documentation
pitchdeck/               # Pitch deck materials
SUBNET_PROPOSAL.md       # Detailed subnet design proposal
```

## Scoring Formula

```
final_score = (0.40 × citation_accuracy + 0.25 × relevance
             + 0.15 × completeness + 0.10 × latency + 0.10 × consistency)
             × 1.5 if precedent-setting case correctly identified
```

## Subnet Parameters

- **Subnet ID:** 5 | **Tempo:** 360 blocks (~72 min) | **Max UIDs:** 256
- **Emission Split:** Owner 18% | Miners 41% | Validators+Stakers 41%

## Miner Tasks

| Task | Weight | Description |
|------|--------|-------------|
| Legal Analysis | 50% | Case analysis with jurisdiction-specific legal reasoning |
| Contract Review | 30% | Smart contract and legal document review |
| Compliance Check | 20% | Regulatory compliance assessment across frameworks |

## License

MIT

## Documentation

- [`SUBNET_PROPOSAL.md`](SUBNET_PROPOSAL.md) — Full technical subnet design proposal
- [`overview.md`](overview.md) — Problem/solution, architecture, mechanism design
- [`pitchdeck/`](pitchdeck/) — Pitch deck and demo video script
