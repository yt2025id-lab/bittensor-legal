# AI Legal Assistant Demo Video Script

**Duration:** 5-7 minutes

---

## Scene 1: Opening (0:00-0:30)
- [Visual] Project logo with professional legal theme (navy/gold). Scales of justice with AI circuit pattern.
- [Voice Over] "Welcome to AI Legal Assistant Subnet - the decentralized platform making legal guidance accessible, affordable, and verified, powered by Bittensor. Because everyone deserves access to justice."

## Scene 2: The Problem (0:30-1:00)
- [Visual] Statistics: "$150-$1000/hour legal fees". "77% of civil legal problems go unresolved". Animated image of people turned away from courthouses.
- [Voice Over] "Legal advice costs $150 to over $1000 per hour. 77% of civil legal problems worldwide go unresolved because people simply can't afford help. Legal information is complex, jurisdiction-specific, and when AI tries to help, there's no way to verify if the answers are actually correct."

## Scene 3: The Solution (1:00-1:45)
- [Visual] Animated network of legal AI nodes. Bittensor integration. $TAO tokens flowing. People from around the world accessing legal help on devices.
- [Voice Over] "Our solution: a Bittensor subnet where legal AI models provide advice, and specialized validators verify every legal reference. Miners compete to give the most accurate, well-referenced answers. Validators check cited statutes and case law against real legal databases. Quality is rewarded with $TAO tokens, and everything is transparent on-chain."

## Scene 4: Mechanism Design Deep Dive (1:45-3:00)
- [Visual] Animated diagram:
  1. User submits legal query with jurisdiction
  2. Miners generate advice with references
  3. Validators verify references exist and are current
  4. Scores computed
  5. Rewards distributed
- [Voice Over] "Here's the mechanism. A user submits a legal query - for example, 'What are my rights as a tenant in California?' Multiple miners generate advice with specific statute and case law references. Validators then verify: do these references actually exist? Are they current? Are they relevant? Each miner receives a quality score, and $TAO rewards go to the most accurate contributors."
- [Visual] Show scoring formula: `Score = 0.5 * RefAccuracy + 0.3 * Relevance + 0.2 * Completeness`

## Scene 5: Live Demo (3:00-5:00)
- [Visual] Screen recording:
  1. Terminal: `uvicorn main:app --reload`
  2. Open browser/Postman: POST to `/advice`
  3. Show JSON request: `{"case_type": "tenant_rights", "description": "Landlord refuses to return security deposit after move-out"}`
  4. Show JSON response with summary, references, recommendation
  5. (Optional) Show validation flow or reputation dashboard
- [Voice Over] "Let's see it in action. We start our API, submit a tenant rights query to the /advice endpoint, and receive a detailed legal summary with specific statute references and actionable recommendations. In production, multiple miners would compete to provide the best answer, and validators ensure every reference is verified."

## Scene 6: Go-to-Market & Impact (5:00-6:00)
- [Visual] GTM roadmap. Partner logos (legal aid orgs, startup incubators). Market stats.
- [Voice Over] "We start by partnering with legal aid organizations and law schools - they need affordable tools, and their feedback improves our models. Then we expand to startup incubators for compliance-as-a-service, and eventually enterprise API integration. The legal tech market is $28 billion and growing at 30% annually."

## Scene 7: Closing & Call to Action (6:00-7:00)
- [Visual] Team info, social links, project logo. "Join Us" call to action.
- [Voice Over] "AI Legal Assistant Subnet - democratizing access to legal knowledge through decentralized AI. Join us in building a world where legal guidance is accessible to everyone, not just those who can afford it."

---
**Production Tips:**
- Use professional navy/gold color scheme throughout.
- Screen recordings should be clean and well-organized.
- Background music: calm, professional, corporate ambient.
- Voice should be professional, empathetic, and clear.
