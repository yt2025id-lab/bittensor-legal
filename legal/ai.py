"""
Simulates Bittensor subnet behavior:
- Multiple miners respond to each legal query with different quality levels
- Validators verify every citation against legal databases
- Yuma Consensus scores and ranks miners
- TAO rewards distributed proportionally
"""

import random
import hashlib
import time

# --- Simulated Miners on the Subnet ---

MINERS = [
    {"uid": 12, "hotkey": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY", "model": "LegalBERT-v3-Pro", "tier": "high"},
    {"uid": 45, "hotkey": "5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty", "model": "StatuteGPT-2.1", "tier": "high"},
    {"uid": 78, "hotkey": "5DAAnrj7VHTznn2AWoezFAmRWVzaqLNFc2rCH5QPAHvReKwz", "model": "CaseLaw-LLM-7B", "tier": "medium"},
    {"uid": 103, "hotkey": "5HGjWAeFDfFCWPsjFQdVV2Msvz2XtMktvgocEZcCj68kUMaw", "model": "JurisMind-Base", "tier": "medium"},
    {"uid": 156, "hotkey": "5CiPPseXPECbkjWCa6MnjNokrgYjMqmKndv2rSneWj6VRzPh", "model": "LawBot-v1-Lite", "tier": "low"},
    {"uid": 201, "hotkey": "5GNJqTPyNqANBkUVMN1LPPrxXnFouWA2MRQg3gKrUYgwQk5e", "model": "GenericLLM-Finetune", "tier": "low"},
]

VALIDATORS = [
    {"uid": 5, "hotkey": "5Ec4AhPUwPeyTFyuhGuBbD224mY85LKLMSqSSo33JYWCazU4", "name": "LegalVerify-Alpha", "stake": 15420.5},
    {"uid": 18, "hotkey": "5FLSigC9HGRKVhB9FiEo4Y3koPsNmBmLJbpXg2mp1hXcS59Y", "name": "CitationCheck-Pro", "stake": 12800.3},
    {"uid": 32, "hotkey": "5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK1iQ7qUsSWFc", "name": "JurisValidator-v2", "stake": 9350.7},
]

# --- Legal knowledge base per case type ---

LEGAL_KNOWLEDGE = {
    "tenant_rights": {
        "high": [
            {
                "statute": "California Civil Code §1950.5",
                "source_url": "https://law.cornell.edu/wex/security_deposit",
                "real": True,
                "relevance": 0.95,
            },
            {
                "statute": "New York General Obligations Law §7-108",
                "source_url": "https://www.nysenate.gov/legislation/laws/GOB/7-108",
                "real": True,
                "relevance": 0.92,
            },
            {
                "statute": "Uniform Residential Landlord and Tenant Act (URLTA) §2.101",
                "source_url": "https://law.cornell.edu/uniform/vol7#702",
                "real": True,
                "relevance": 0.88,
            },
            {
                "statute": "Fair Housing Act, 42 U.S.C. §3604",
                "source_url": "https://law.cornell.edu/uscode/text/42/3604",
                "real": True,
                "relevance": 0.60,
            },
        ],
        "medium": [
            {
                "statute": "California Civil Code §1950.5",
                "source_url": "https://law.cornell.edu/wex/security_deposit",
                "real": True,
                "relevance": 0.95,
            },
            {
                "statute": "General landlord-tenant statute",
                "source_url": "https://law.cornell.edu/wex/landlord-tenant_law",
                "real": True,
                "relevance": 0.70,
            },
        ],
        "low": [
            {
                "statute": "California Civil Code §1950.5",
                "source_url": "https://law.cornell.edu/wex/security_deposit",
                "real": True,
                "relevance": 0.95,
            },
            {
                "statute": "Tenant Protection Act §42-301(b)",
                "source_url": "https://law.cornell.edu/fake/statute",
                "real": False,  # HALLUCINATED citation
                "relevance": 0.0,
            },
        ],
        "summaries": {
            "high": (
                "Under most state landlord-tenant laws, a landlord is required to return "
                "the security deposit within a specific timeframe after move-out (typically "
                "14-30 days depending on jurisdiction). If the landlord withholds the deposit, "
                "they must provide an itemized written statement of deductions. Failure to comply "
                "may entitle the tenant to recover the full deposit plus statutory penalties "
                "(often 2-3x the deposit). Under California Civil Code §1950.5, the deadline is "
                "21 days. Under New York GOL §7-108, it is 14 days with an itemized statement. "
                "The URLTA provides additional protections for tenants in adopting states."
            ),
            "medium": (
                "Landlord-tenant laws generally require the return of security deposits within "
                "a reasonable timeframe. California Civil Code §1950.5 sets a 21-day deadline. "
                "If your landlord fails to return the deposit, you may be entitled to penalties."
            ),
            "low": (
                "Your landlord should return your deposit. There are laws that protect tenants. "
                "You can try to take legal action if they refuse."
            ),
        },
        "recommendations": {
            "high": (
                "1. Send a formal written demand letter via certified mail citing the applicable "
                "state statute and deadline. 2. Document all move-out conditions with timestamped "
                "photos and your original lease agreement. 3. If the landlord does not respond within "
                "the statutory timeframe, file a claim in Small Claims Court — most jurisdictions "
                "allow recovery of 2-3x the deposit as bad faith penalties. 4. Contact your local "
                "tenant rights organization or legal aid for free assistance."
            ),
            "medium": (
                "1. Send a demand letter to your landlord requesting the deposit back. "
                "2. Keep records of your lease and move-out condition. "
                "3. Consider filing in Small Claims Court if they don't respond."
            ),
            "low": (
                "Contact a lawyer or file a complaint about the deposit."
            ),
        },
    },
    "employment_law": {
        "high": [
            {
                "statute": "Fair Labor Standards Act, 29 U.S.C. §207",
                "source_url": "https://law.cornell.edu/uscode/text/29/207",
                "real": True,
                "relevance": 0.97,
            },
            {
                "statute": "California Labor Code §510",
                "source_url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=510",
                "real": True,
                "relevance": 0.90,
            },
            {
                "statute": "29 U.S.C. §216(b) - FLSA Private Right of Action",
                "source_url": "https://law.cornell.edu/uscode/text/29/216",
                "real": True,
                "relevance": 0.88,
            },
        ],
        "medium": [
            {
                "statute": "Fair Labor Standards Act, 29 U.S.C. §207",
                "source_url": "https://law.cornell.edu/uscode/text/29/207",
                "real": True,
                "relevance": 0.97,
            },
            {
                "statute": "DOL Wage and Hour Division guidelines",
                "source_url": "https://www.dol.gov/agencies/whd/overtime",
                "real": True,
                "relevance": 0.75,
            },
        ],
        "low": [
            {
                "statute": "Fair Labor Standards Act, 29 U.S.C. §207",
                "source_url": "https://law.cornell.edu/uscode/text/29/207",
                "real": True,
                "relevance": 0.97,
            },
            {
                "statute": "Federal Overtime Guarantee Act §18-552",
                "source_url": "https://law.cornell.edu/fake/overtime",
                "real": False,  # HALLUCINATED
                "relevance": 0.0,
            },
        ],
        "summaries": {
            "high": (
                "Under the Fair Labor Standards Act (FLSA), 29 U.S.C. §207, non-exempt employees "
                "are entitled to overtime pay at 1.5x their regular rate for hours worked over 40 "
                "in a workweek. Employers who violate this may be liable for back wages plus an "
                "equal amount in liquidated damages under §216(b). California Labor Code §510 "
                "additionally requires overtime for hours over 8 in a single day. The statute of "
                "limitations is 2 years (3 years for willful violations)."
            ),
            "medium": (
                "The FLSA requires overtime pay at 1.5x for hours over 40 per week. "
                "Your employer may owe you back wages. You can file a complaint with the DOL."
            ),
            "low": (
                "You might be owed overtime pay. There are federal laws about this. "
                "Try contacting the labor department."
            ),
        },
        "recommendations": {
            "high": (
                "1. Gather all pay stubs, timesheets, and employment records documenting unpaid "
                "overtime hours. 2. File a wage complaint with your state labor board or the U.S. "
                "DOL Wage and Hour Division. 3. You may also file a private lawsuit under 29 U.S.C. "
                "§216(b) to recover back wages and liquidated damages. 4. Consult an employment "
                "attorney — many offer free consultations for wage theft cases."
            ),
            "medium": (
                "1. Collect your pay stubs and time records. "
                "2. File a complaint with the Department of Labor. "
                "3. Consider consulting an employment lawyer."
            ),
            "low": (
                "Gather your records and talk to a lawyer about the overtime issue."
            ),
        },
    },
    "contract_dispute": {
        "high": [
            {
                "statute": "UCC §2-601 - Buyer's Rights on Improper Delivery",
                "source_url": "https://law.cornell.edu/ucc/2/2-601",
                "real": True,
                "relevance": 0.93,
            },
            {
                "statute": "Restatement (Second) of Contracts §344",
                "source_url": "https://law.cornell.edu/wex/breach_of_contract",
                "real": True,
                "relevance": 0.91,
            },
            {
                "statute": "Hadley v. Baxendale, 9 Exch. 341 (1854)",
                "source_url": "https://www.courtlistener.com",
                "real": True,
                "relevance": 0.85,
            },
        ],
        "medium": [
            {
                "statute": "UCC §2-601",
                "source_url": "https://law.cornell.edu/ucc/2/2-601",
                "real": True,
                "relevance": 0.93,
            },
            {
                "statute": "General contract law principles",
                "source_url": "https://law.cornell.edu/wex/contract",
                "real": True,
                "relevance": 0.65,
            },
        ],
        "low": [
            {
                "statute": "UCC §2-601",
                "source_url": "https://law.cornell.edu/ucc/2/2-601",
                "real": True,
                "relevance": 0.93,
            },
            {
                "statute": "Federal Contract Enforcement Act §99-201",
                "source_url": "https://law.cornell.edu/fake/contract",
                "real": False,  # HALLUCINATED
                "relevance": 0.0,
            },
        ],
        "summaries": {
            "high": (
                "Under the UCC §2-601 and common law contract principles, a breach of contract "
                "occurs when one party fails to perform their obligations without legal excuse. "
                "Remedies include compensatory damages, consequential damages (per Hadley v. "
                "Baxendale), and specific performance. Under the Restatement (Second) of "
                "Contracts §344, the injured party may recover expectation, reliance, or "
                "restitution interest depending on the circumstances."
            ),
            "medium": (
                "A breach of contract occurs when someone doesn't fulfill their end of the deal. "
                "You may be entitled to damages under the UCC and common law principles."
            ),
            "low": (
                "If someone broke a contract with you, you can try to sue them for damages."
            ),
        },
        "recommendations": {
            "high": (
                "1. Review the original contract terms carefully, including dispute resolution "
                "clauses (arbitration, mediation, jurisdiction). 2. Document all evidence of the "
                "breach and calculate your resulting damages. 3. Send a formal demand letter "
                "outlining the breach and requesting specific performance or monetary damages. "
                "4. If unresolved, consider mediation before litigation to save time and costs."
            ),
            "medium": (
                "1. Review your contract for relevant terms. "
                "2. Send a demand letter to the breaching party. "
                "3. Consider mediation or small claims court."
            ),
            "low": (
                "Get a lawyer to review your contract and send a demand letter."
            ),
        },
    },
}


def _generate_query_id(query) -> str:
    raw = f"{query.user_id}-{query.case_type}-{time.time()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _simulate_miner_response(miner: dict, case_type: str) -> dict:
    """Simulate a single miner generating a legal response."""
    tier = miner["tier"]
    knowledge = LEGAL_KNOWLEDGE.get(case_type, LEGAL_KNOWLEDGE["tenant_rights"])

    citations_data = knowledge.get(tier, knowledge["medium"])
    summary = knowledge["summaries"].get(tier, knowledge["summaries"]["medium"])
    recommendation = knowledge["recommendations"].get(tier, knowledge["recommendations"]["medium"])

    # Simulate response latency (better miners are faster)
    latency_map = {"high": random.randint(800, 1500), "medium": random.randint(1200, 2500), "low": random.randint(2000, 4000)}
    latency = latency_map[tier]

    citations = []
    for c in citations_data:
        citations.append({
            "statute": c["statute"],
            "source_url": c["source_url"],
            "verified": c["real"],  # Validators will verify this
            "relevance_score": round(c["relevance"] + random.uniform(-0.05, 0.05), 3),
        })

    return {
        "miner_uid": miner["uid"],
        "miner_hotkey": miner["hotkey"],
        "model_name": miner["model"],
        "summary": summary,
        "citations": citations,
        "recommendation": recommendation,
        "response_time_ms": latency,
    }


def _validate_miner(miner_response: dict, miner_tier: str) -> dict:
    """Simulate validator scoring a miner's response."""
    # Base scores by tier (with some randomness)
    tier_base = {"high": 0.88, "medium": 0.65, "low": 0.35}
    base = tier_base[miner_tier]

    # Check how many citations are real vs hallucinated
    real_citations = sum(1 for c in miner_response["citations"] if c["verified"])
    total_citations = len(miner_response["citations"])
    citation_ratio = real_citations / total_citations if total_citations > 0 else 0

    citation_accuracy = round(min(1.0, citation_ratio + random.uniform(-0.05, 0.05)), 3)
    relevance = round(min(1.0, base + random.uniform(-0.08, 0.08)), 3)
    completeness = round(min(1.0, (base - 0.05) + random.uniform(-0.08, 0.08)), 3)
    jurisdiction = round(min(1.0, (base + 0.02) + random.uniform(-0.06, 0.06)), 3)

    # Latency scoring (faster = better, normalized)
    latency_ms = miner_response["response_time_ms"]
    latency_score = round(max(0.1, min(1.0, 1.0 - (latency_ms - 500) / 4000)), 3)

    # Weighted total: 35% citation + 25% relevance + 15% completeness + 15% jurisdiction + 10% latency
    total = round(
        0.35 * citation_accuracy
        + 0.25 * relevance
        + 0.15 * completeness
        + 0.15 * jurisdiction
        + 0.10 * latency_score,
        4,
    )

    return {
        "citation_accuracy": citation_accuracy,
        "legal_relevance": relevance,
        "completeness": completeness,
        "jurisdiction_accuracy": jurisdiction,
        "latency_score": latency_score,
        "total_score": total,
    }


def run_subnet_query(query):
    """
    Simulates a full Bittensor subnet query cycle:
    1. Query broadcast to all miners
    2. Each miner responds with legal analysis + citations
    3. Validators verify citations and score each response
    4. Yuma Consensus ranks miners and distributes TAO
    5. Best response returned to user
    """
    query_id = _generate_query_id(query)
    case_type = query.case_type.lower().strip()
    block_number = random.randint(3_800_000, 3_900_000)

    # Step 1 & 2: Miners respond
    miner_results = []
    for miner in MINERS:
        response = _simulate_miner_response(miner, case_type)
        scores = _validate_miner(response, miner["tier"])
        miner_results.append({
            "response": response,
            "scores": scores,
            "tier": miner["tier"],
        })

    # Step 3: Sort by total score (Yuma Consensus ranking)
    miner_results.sort(key=lambda x: x["scores"]["total_score"], reverse=True)

    # Step 4: Calculate TAO rewards (top miners get more)
    total_emission = 0.0285  # TAO per query block
    score_sum = sum(r["scores"]["total_score"] for r in miner_results)

    all_results = []
    total_citations_verified = 0
    for rank, result in enumerate(miner_results, 1):
        share = result["scores"]["total_score"] / score_sum if score_sum > 0 else 0
        tao_reward = round(total_emission * share, 6)
        total_citations_verified += sum(
            1 for c in result["response"]["citations"] if c["verified"]
        )
        all_results.append({
            "miner": result["response"],
            "validator_scores": result["scores"],
            "rank": rank,
            "tao_reward": tao_reward,
        })

    best = all_results[0]

    return {
        "query_id": query_id,
        "subnet_uid": 87,
        "block_number": block_number,
        "num_miners_responded": len(MINERS),
        "num_citations_verified": total_citations_verified,
        "best_response": best["miner"],
        "best_score": best["validator_scores"],
        "all_miner_results": all_results,
        "consensus_method": "Yuma Consensus",
    }


def get_subnet_status():
    """Returns current subnet status / dashboard info."""
    block = random.randint(3_800_000, 3_900_000)
    return {
        "subnet_uid": 87,
        "subnet_name": "AI Legal Assistant",
        "current_block": block,
        "total_miners": len(MINERS),
        "total_validators": len(VALIDATORS),
        "active_miners": [
            {
                "uid": m["uid"],
                "hotkey": m["hotkey"][:16] + "...",
                "model": m["model"],
                "tier": m["tier"],
                "avg_score": round({"high": 0.89, "medium": 0.67, "low": 0.38}[m["tier"]] + random.uniform(-0.03, 0.03), 3),
                "total_rewards_tao": round(random.uniform(5, 150), 2),
            }
            for m in MINERS
        ],
        "active_validators": [
            {
                "uid": v["uid"],
                "hotkey": v["hotkey"][:16] + "...",
                "name": v["name"],
                "stake_tao": v["stake"],
                "queries_validated": random.randint(500, 5000),
            }
            for v in VALIDATORS
        ],
        "emission_rate": "0.0285 TAO/block (18% owner, 41% miners, 41% validators)",
        "total_queries_processed": random.randint(12000, 25000),
        "avg_citation_accuracy": round(random.uniform(0.82, 0.91), 3),
    }
