# AI Legal Assistant Subnet

## Overview
A decentralized legal advisory platform powered by Bittensor. Legal experts and AI models collaborate to provide accessible, transparent, and affordable legal guidance with on-chain reputation and token incentives.

## Features
- AI-driven legal advice and summaries
- Document review and compliance checking
- Multi-jurisdiction legal reference
- On-chain reputation and validation
- Bittensor subnet integration with $TAO rewards

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python main.py`
3. Submit legal queries via `/advice` endpoint

## Folder Structure
- `main.py`: Entry point (FastAPI)
- `legal/`: Core logic
  - `ai.py`: AI legal analysis engine
  - `models.py`: Data models (LegalQuery, LegalResponse)
  - `routes.py`: API routes
  - `db.py`: Database operations
- `overview.md`: Full project documentation
- `pitchdeck/`: Presentation materials
- `requirements.txt`: Dependencies

## Bittensor Subnet Design
- **Miner:** Analyzes legal queries, generates advice with jurisdiction-specific references
- **Validator:** Verifies accuracy of legal references, assesses advice quality and relevance
- **Incentive:** $TAO rewards based on reference accuracy and user satisfaction

## License
MIT

## Subnet Design Proposal
See [`SUBNET_PROPOSAL.md`](SUBNET_PROPOSAL.md) for the full technical subnet design proposal, including incentive mechanism, miner/validator design, business logic, and go-to-market strategy.

## Full Documentation
See `overview.md` for detailed problem/solution, architecture, and mechanism design.
See `pitchdeck/` for pitch deck, demo video script, and visual guide.
