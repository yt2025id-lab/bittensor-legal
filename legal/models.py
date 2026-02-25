from pydantic import BaseModel, Field
from typing import List, Optional


class LegalQuery(BaseModel):
    user_id: str = Field(..., example="user123")
    case_type: str = Field(..., example="tenant_rights")
    description: str = Field(
        ...,
        example="My landlord refuses to return my security deposit after move-out. I moved out 45 days ago and left the apartment in good condition.",
    )
    jurisdiction: str = Field(
        default="US-Federal",
        example="US-CA",
        description="Jurisdiction code (e.g. US-Federal, US-CA, US-NY, UK, EU)",
    )


# --- Miner models ---

class CitationDetail(BaseModel):
    statute: str = Field(..., description="Statute or case law citation")
    source_url: str = Field(..., description="Verification URL from legal database")
    verified: bool = Field(..., description="Whether validator confirmed this citation exists and is current")
    relevance_score: float = Field(..., description="How relevant this citation is to the query (0-1)")


class MinerResponse(BaseModel):
    miner_uid: int = Field(..., description="Unique miner ID on the subnet")
    miner_hotkey: str = Field(..., description="Miner's hotkey address")
    model_name: str = Field(..., description="Name of the legal AI model used")
    summary: str
    citations: List[CitationDetail]
    recommendation: str
    response_time_ms: int = Field(..., description="Miner response latency in milliseconds")


# --- Validator scoring ---

class ValidatorScore(BaseModel):
    citation_accuracy: float = Field(..., description="35% weight - Are citations real and current?")
    legal_relevance: float = Field(..., description="25% weight - Is the analysis relevant to the query?")
    completeness: float = Field(..., description="15% weight - Does it cover all applicable law?")
    jurisdiction_accuracy: float = Field(..., description="15% weight - Correct jurisdiction applied?")
    latency_score: float = Field(..., description="10% weight - Response speed")
    total_score: float = Field(..., description="Weighted total score")


class MinerResult(BaseModel):
    miner: MinerResponse
    validator_scores: ValidatorScore
    rank: int = Field(..., description="Miner rank for this query (1 = best)")
    tao_reward: float = Field(..., description="Estimated TAO reward for this response")


# --- Subnet response ---

class SubnetResponse(BaseModel):
    query_id: str = Field(..., description="Unique query identifier")
    subnet_uid: int = Field(default=87, description="Subnet UID on Bittensor network")
    block_number: int = Field(..., description="Bittensor block number")
    num_miners_responded: int
    num_citations_verified: int
    best_response: MinerResponse = Field(..., description="Highest-scoring miner response (returned to user)")
    best_score: ValidatorScore = Field(..., description="Validator scores for best response")
    all_miner_results: List[MinerResult] = Field(..., description="All miners ranked by score")
    consensus_method: str = Field(default="Yuma Consensus", description="Consensus mechanism used")


# --- Subnet status ---

class SubnetStatus(BaseModel):
    subnet_uid: int = 87
    subnet_name: str = "AI Legal Assistant"
    current_block: int
    total_miners: int
    total_validators: int
    active_miners: List[dict]
    active_validators: List[dict]
    emission_rate: str
    total_queries_processed: int
    avg_citation_accuracy: float
