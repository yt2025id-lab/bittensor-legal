# AI Legal Assistant — Subnet Design Proposal

> **Bittensor Subnet Ideathon 2026**
> Team: AI Legal Assistant | Twitter: @Ozan_OnChain | Discord: ozan_onchain

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Incentive & Mechanism Design](#2-incentive--mechanism-design)
3. [Miner Design](#3-miner-design)
4. [Validator Design](#4-validator-design)
5. [Business Logic & Market Rationale](#5-business-logic--market-rationale)
6. [Go-To-Market Strategy](#6-go-to-market-strategy)

---

## 1. Executive Summary

**AI Legal Assistant** is a Bittensor subnet that creates a competitive marketplace for legal AI models. Miners build and operate legal reasoning models that answer legal queries with accurate statute citations, case law references, and jurisdiction-specific guidance. Validators verify every citation against authoritative legal databases and score responses for accuracy, relevance, and completeness. The best legal AI models earn $TAO emissions, producing a permissionless system that democratizes access to quality legal guidance.

**Digital Commodity Produced:** Verified, citation-accurate legal advice and analysis.

**Proof of Intelligence:** Every miner must demonstrate genuine legal reasoning capability — producing accurate, well-cited legal analysis that withstands validator verification. Random or fabricated citations score zero. The only path to rewards is building genuinely capable legal AI.

---

## 2. Incentive & Mechanism Design

### 2.1 Emission and Reward Logic

| Recipient | Share | Description |
|-----------|-------|-------------|
| Subnet Owner | 18% | Funds legal database licensing, development, and security audits |
| Miners | 41% | Distributed proportionally via Yuma Consensus performance scores |
| Validators + Stakers | 41% | Proportional to stake and bond strength |

### 2.2 Incentive Alignment

**For Miners:**
- Higher citation accuracy + better legal reasoning = higher weights = more $TAO.
- Multi-dimensional scoring (citation accuracy, relevance, completeness, jurisdiction correctness) prevents gaming single metrics.
- No score cap — models that handle complex multi-jurisdiction cases earn bonus multipliers.

**For Validators:**
- Bond growth tied to honest, independent evaluation via commit-reveal.
- Validators who maintain high-quality legal databases and independently verify citations build stronger EMA bonds.

**For Stakers:**
- Legal services have massive real-world demand ($1T+ global market). API revenue increases alpha token value.

### 2.3 Mechanisms to Discourage Adversarial Behavior

| Threat | Defense Mechanism |
|--------|-------------------|
| **Miners fabricating citations** | Validators verify every citation against legal databases (Cornell LII, CourtListener, government statute databases); fabricated citations score 0 |
| **Miners returning generic/template responses** | Challenges include jurisdiction-specific edge cases; generic responses miss jurisdiction nuances and score low |
| **Miners copying from free legal websites** | Strict 12s timeout; validators include novel hypothetical scenarios not found online |
| **Colluding validators** | Yuma Consensus clipping — outlier weights clipped to stake-weighted median |
| **Weight-copying validators** | Commit-reveal (1 tempo delay); stale weights misalign with changing miner performance |
| **Model stagnation** | Anti-monopoly decay: 2% reward decrease per tempo after 30 tempos as top miner |

### 2.4 Proof of Intelligence

1. **Domain expertise required:** Legal reasoning requires understanding statutes, precedents, jurisdiction hierarchies, and legal principles.
2. **Verifiable citations:** Every statute and case law reference can be verified against authoritative databases.
3. **Jurisdiction complexity:** Legal advice varies dramatically by jurisdiction — models must handle US federal, state, EU, UK, and other legal systems.
4. **Novel scenario handling:** Validators include hypothetical cases that require genuine legal reasoning, not memorization.

### 2.5 High-Level Algorithm

```
EVERY TEMPO (~72 minutes):

  VALIDATOR LOOP:
    1. GENERATE legal challenges:
       - Sample from curated legal QA datasets (bar exam questions, legal hypotheticals)
       - Specify jurisdiction (e.g., "California", "UK", "EU GDPR")
       - Include case type (tenant rights, employment, contract, IP, criminal)
       - Record known-correct answers and valid citations

    2. DISPATCH to miners via LegalSynapse:
       - case_type, jurisdiction, description, random_seed
       - timeout = 12 seconds

    3. COLLECT miner responses:
       - summary, references (citations), recommendation, jurisdiction_notes

    4. SCORE each response:
       - citation_accuracy = verified_citations / total_citations    [0.0 - 1.0]
       - relevance_score = semantic_similarity(response, ground_truth) [0.0 - 1.0]
       - completeness = coverage of key legal issues                  [0.0 - 1.0]
       - jurisdiction_accuracy = correct_jurisdiction_refs / total    [0.0 - 1.0]
       - latency_score = max(1 - elapsed/12, 0)                     [0.0 - 1.0]

       - final_score = 0.35 * citation_accuracy
                     + 0.25 * relevance_score
                     + 0.15 * completeness
                     + 0.15 * jurisdiction_accuracy
                     + 0.10 * latency_score

    5. UPDATE EMA scores and SUBMIT weights (commit-reveal)

  MINER LOOP:
    1. RECEIVE LegalSynapse
    2. RUN through legal reasoning model
    3. RETURN LegalResponse with summary, citations, recommendation
    4. CONTINUOUSLY fine-tune model on legal corpora

  YUMA CONSENSUS (on-chain):
    1. Aggregate validator weights, clip outliers
    2. Compute miner rankings → emission allocation
    3. Distribute $TAO
```

---

## 3. Miner Design

### 3.1 Miner Tasks

**Task Types (Multiple Incentive Mechanisms):**

| Mechanism | Weight | Description |
|-----------|--------|-------------|
| **Legal Query Analysis** | 50% | Given a legal scenario, provide advice with accurate citations |
| **Citation Verification** | 30% | Given a set of legal claims, provide correct statute/case references |
| **Jurisdiction Classification** | 20% | Determine applicable jurisdiction and relevant regulatory framework |

### 3.2 Input → Output Format (Synapse Protocol)

```python
class LegalSynapse(bt.Synapse):
    # ── Immutable Inputs (set by validator) ──
    task_type: str                    # "query_analysis" | "citation_verification" | "jurisdiction"
    case_type: str                    # "tenant_rights" | "employment" | "contract" | "ip" | "criminal"
    jurisdiction: str                 # "US-CA" | "US-NY" | "UK" | "EU" | "AU"
    description: str                  # Detailed legal scenario
    specific_questions: List[str]     # Specific questions to answer
    random_seed: int

    # ── Mutable Outputs (filled by miner) ──
    summary: Optional[str] = None                  # Legal analysis summary
    references: Optional[List[dict]] = None        # [{citation, source_url, relevance}]
    recommendation: Optional[str] = None           # Actionable legal recommendation
    jurisdiction_notes: Optional[str] = None       # Jurisdiction-specific considerations
    confidence: Optional[float] = None             # Model confidence [0.0 - 1.0]
    applicable_statutes: Optional[List[str]] = None # Relevant statute codes
```

**Example Input:**
```json
{
  "task_type": "query_analysis",
  "case_type": "tenant_rights",
  "jurisdiction": "US-CA",
  "description": "Landlord has not returned $3,200 security deposit after 45 days. Tenant left property in good condition with photo documentation.",
  "specific_questions": [
    "What is the legal deadline for deposit return in California?",
    "What penalties apply for late return?",
    "What is the recommended legal action?"
  ],
  "random_seed": 58291047
}
```

**Example Output:**
```json
{
  "summary": "Under California Civil Code §1950.5, landlords must return security deposits within 21 days of tenant move-out. At 45 days, the landlord is in violation. The tenant is entitled to the full deposit plus potential penalties up to 2x the deposit amount as bad faith damages.",
  "references": [
    {
      "citation": "Cal. Civ. Code § 1950.5(g)(1)",
      "source_url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1950.5.&lawCode=CIV",
      "relevance": "21-day return deadline for security deposits"
    },
    {
      "citation": "Cal. Civ. Code § 1950.5(l)",
      "source_url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1950.5.&lawCode=CIV",
      "relevance": "Bad faith penalty up to 2x deposit amount"
    },
    {
      "citation": "Granberry v. Islay Investments (1995) 9 Cal.4th 738",
      "source_url": "https://www.courtlistener.com/opinion/1279361/granberry-v-islay-investments/",
      "relevance": "Precedent for bad faith deposit retention penalties"
    }
  ],
  "recommendation": "1. Send written demand letter via certified mail citing Cal. Civ. Code § 1950.5. 2. If no response within 14 days, file claim in Small Claims Court (limit $10,000 in CA). 3. Include photo documentation as evidence of property condition.",
  "jurisdiction_notes": "California is a tenant-friendly jurisdiction. Small Claims Court filing fee is approximately $75. No attorney needed for Small Claims.",
  "confidence": 0.91,
  "applicable_statutes": ["Cal. Civ. Code § 1950.5", "Cal. Code Civ. Proc. § 116.220"]
}
```

### 3.3 Performance Dimensions

| Dimension | Weight | Metric | Description |
|-----------|--------|--------|-------------|
| **Citation Accuracy** | 35% | Verified correct / total cited | Every citation checked against legal databases |
| **Legal Relevance** | 25% | Semantic similarity to ground truth | Response addresses the actual legal issues |
| **Completeness** | 15% | Coverage of key legal issues | All relevant statutes and considerations mentioned |
| **Jurisdiction Accuracy** | 15% | Correct jurisdiction references | Citations match the specified jurisdiction |
| **Response Latency** | 10% | `max(1 - elapsed/12s, 0)` | Faster responses score higher |

### 3.4 Miner Hardware Requirements

| Tier | Hardware | Capability |
|------|----------|-----------|
| Entry | RTX 3090, 32GB RAM | Fine-tuned 7B legal LLM (SaulLM, LegalBERT) |
| Mid | A5000/A100 40GB | 13B-30B models with RAG over legal databases |
| High | A100 80GB / H100 | 70B+ models with full legal corpus retrieval |

### 3.5 Recommended Miner Strategy

1. Fine-tune legal-specific LLMs (SaulLM-7B, LegalBERT, Mistral-Legal) on bar exam QA and legal corpora.
2. Implement RAG (Retrieval-Augmented Generation) with vectorized legal databases (statutes, case law).
3. Build jurisdiction-specific adapters for US states, UK, EU regulations.
4. Train citation extraction pipeline to output properly formatted legal references.
5. Continuously update legal corpus with new statutes and case law.

---

## 4. Validator Design

### 4.1 Scoring and Evaluation Methodology

**Ground Truth Sources:**

| Source | Content | Usage |
|--------|---------|-------|
| Cornell LII | US federal and state statutes | Citation verification |
| CourtListener | US case law database | Case citation verification |
| EUR-Lex | EU legislation and case law | EU jurisdiction verification |
| UK Legislation.gov.uk | UK statutes | UK citation verification |
| Bar Exam QA datasets | Legal reasoning questions | Challenge generation |
| Legal hypotheticals (curated) | Novel scenarios with expert answers | Ground truth for scoring |

**Citation Verification Algorithm:**

```python
def verify_citation(citation, jurisdiction):
    """Verify a legal citation against authoritative databases."""

    # 1. Parse citation format
    parsed = parse_legal_citation(citation)  # Extract statute code, case name, year

    # 2. Query appropriate database
    if parsed.type == "statute":
        result = query_statute_db(parsed.code, jurisdiction)
    elif parsed.type == "case_law":
        result = query_case_db(parsed.case_name, parsed.year)

    # 3. Verify existence and relevance
    exists = result is not None
    current = result.is_current() if exists else False  # Not repealed/overturned
    relevant = semantic_similarity(result.text, citation.relevance_claim) > 0.6

    return {
        "exists": exists,       # Citation actually exists
        "current": current,     # Not outdated/repealed
        "relevant": relevant,   # Actually relevant to the claim
        "score": (exists * 0.4 + current * 0.3 + relevant * 0.3)
    }
```

### 4.2 Evaluation Cadence

| Action | Frequency | Description |
|--------|-----------|-------------|
| Challenge dispatch | Every tempo (~72 min) | 1-2 legal challenges per miner per tempo |
| Citation verification | After each response | Verify all citations against legal databases |
| EMA update | After scoring | `ema[uid] = 0.9 * ema[uid] + 0.1 * new_score` |
| Weight submission | Every 100 blocks | Normalized weights to blockchain |
| Legal database sync | Daily | Update statute and case law databases |
| Challenge set rotation | Weekly | New hypothetical scenarios to prevent memorization |

### 4.3 Validator Incentive Alignment

1. **Bond Growth:** Validators who independently verify citations and honestly evaluate miners build stronger EMA bonds.
2. **Commit-Reveal:** 1-tempo encrypted weights prevent copying.
3. **Database Quality:** Validators with comprehensive, up-to-date legal databases produce more accurate scores, aligning better with consensus.
4. **Consensus-Based Weights:** Bond accrual rewards honest, consistent validators.

---

## 5. Business Logic & Market Rationale

### 5.1 The Problem and Why It Matters

- **77% of civil legal problems** go unresolved due to cost barriers (World Justice Project).
- Legal advice costs **$150-$1,000/hour** — inaccessible for most individuals and small businesses.
- Existing legal AI (ChatGPT, generic LLMs) **hallucinates citations** — fabricating non-existent statutes and case law.
- No verification layer exists for AI-generated legal content.

**Market Size:**
- Global legal services: **$1 trillion+** annually.
- Legal tech market: **$28B by 2027** (Grand View Research).
- AI in legal: **$1.5B by 2026**, growing 30%+ CAGR.

### 5.2 Competing Solutions

**Within Bittensor:**

| Subnet | Focus | How We Differ |
|--------|-------|---------------|
| No direct competitor | No existing legal AI subnet | First-mover in verified legal AI on Bittensor |

**Outside Bittensor:**

| Solution | Limitation | Our Advantage |
|----------|-----------|---------------|
| LegalZoom / Rocket Lawyer | Template-based, not AI-driven, expensive subscriptions | AI-powered, pay-per-query, continuously improving |
| ChatGPT / Claude for legal | Hallucinates citations, no verification | Every citation verified against authoritative databases |
| Casetext (CoCounsel) | Proprietary, expensive ($200+/month), US-only | Open, multi-jurisdiction, $TAO-incentivized |
| Harvey AI | Enterprise-only, invite-only access | Permissionless, accessible to individuals and SMBs |

### 5.3 Why This Use Case Is Well-Suited to a Bittensor Subnet

1. **Verifiable output:** Legal citations are binary — they either exist in legal databases or they don't. This enables objective scoring.
2. **Competitive improvement:** Multiple miners competing on citation accuracy and legal reasoning quality drives continuous improvement.
3. **High-value application:** Legal advice commands premium pricing ($150-$1,000/hr equivalent), supporting sustainable economics.
4. **Multi-jurisdictional complexity:** The variety of legal systems creates rich, diverse challenges that prevent simple gaming.
5. **Natural quality assurance:** Validator citation verification creates a unique trust layer that centralized legal AI lacks.

### 5.4 Path to Long-Term Adoption

**Phase 1 (Month 1-3):** Launch with US legal query analysis (federal + top 10 states by population).
**Phase 2 (Month 4-6):** Add UK and EU jurisdictions; launch consumer API.
**Phase 3 (Month 7-12):** Enterprise tier for law firms; legal aid organization partnerships.
**Phase 4 (Year 2+):** Multi-language support; contract review mechanism; regulatory compliance checker.

**Revenue Model:**
```
API Query Fees ($TAO) → Subnet AMM → Higher Alpha Price → More Emissions → More Miners → Better Legal AI
```

---

## 6. Go-To-Market Strategy

### 6.1 Initial Target Users & Use Cases

| Segment | Use Case | Value Proposition |
|---------|----------|-------------------|
| **Individuals** | Tenant rights, employment disputes, small claims | Affordable legal guidance with verified citations |
| **Startups / SMBs** | Contract review, compliance questions, IP basics | 100x cheaper than traditional legal counsel |
| **Legal aid organizations** | Scale free legal advice to underserved communities | AI-assisted triage with citation verification |
| **Law students** | Research assistant, bar exam preparation | Verified legal references for study |

### 6.2 Distribution & Growth Channels

- Open-source SDK and API documentation on GitHub.
- Listing on Bittensor subnet directories (SubnetAlpha, TaoStats).
- Partnerships with legal aid nonprofits (Legal Aid Society, Pro Bono Net).
- Content marketing: "How AI is democratizing legal access" blog series.
- Law school partnerships for beta testing and feedback.

### 6.3 Incentives for Early Participation

**For Early Miners:**
- Low competition = higher per-miner emissions.
- Pre-trained legal model weights and fine-tuning guides provided.
- Curated legal training datasets shared with early miners.

**For Early Validators:**
- Early bond accumulation advantage.
- Access to subnet owner's legal database infrastructure.
- Direct input on scoring methodology.

**For Early Users/Stakers:**
- Alpha token at lowest price; free API tier during beta (5,000 queries/month).
- Governance input on supported jurisdictions and case types.

**Bootstrapping Timeline:**
1. **Week 1-2:** Reference miner + validator running; publish accuracy baselines.
2. **Week 3-4:** Miner onboarding with pre-trained models; community recruitment.
3. **Month 2:** Public API launch; legal aid organization pilot.
4. **Month 3:** First law firm partnership; publish citation accuracy benchmarks.

---

## Appendix

### A. Subnet Hyperparameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `MaxAllowedUids` | 256 | Sufficient for diverse legal specializations |
| `MaxAllowedValidators` | 64 | Standard default |
| `ImmunityPeriod` | 5000 blocks | ~7 hours protection |
| `WeightsRateLimit` | 100 blocks | ~20 min between updates |
| `CommitRevealPeriod` | 1 tempo | Anti-weight-copying |
| `Tempo` | 360 blocks | ~72 min evaluation cycle |

### B. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Citation hallucination | Binary verification against authoritative databases; 0 score for fabricated citations |
| Jurisdiction confusion | Jurisdiction-specific challenges; separate scoring per jurisdiction |
| Outdated legal references | Daily database sync; validators check for repealed statutes |
| Unauthorized practice of law concerns | All responses include disclaimer: "Not legal advice. Consult a licensed attorney." |
| Low miner participation | Subnet owner runs reference miners; provide pre-trained models |

---

*This proposal was prepared for the Bittensor Subnet Ideathon 2026.*
*GitHub: https://github.com/yt2025id-lab/bittensor-legal*
