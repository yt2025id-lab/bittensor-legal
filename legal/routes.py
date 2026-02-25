from fastapi import APIRouter
from .models import LegalQuery, SubnetResponse, SubnetStatus
from .ai import run_subnet_query, get_subnet_status

router = APIRouter(tags=["Legal Subnet"])


@router.post("/advice", response_model=SubnetResponse, summary="Submit legal query to subnet")
def advice(query: LegalQuery):
    """
    Broadcasts a legal query to all miners on the subnet.

    **Subnet flow:**
    1. Query is sent to all active miners
    2. Each miner responds with legal analysis + statute citations
    3. Validators verify every citation against legal databases (Cornell LII, CourtListener)
    4. Yuma Consensus ranks miners by weighted score
    5. Best response returned to user, TAO rewards distributed

    **Scoring weights:**
    - Citation Accuracy: 35% (are citations real and current?)
    - Legal Relevance: 25% (is the analysis relevant?)
    - Completeness: 15% (does it cover all applicable law?)
    - Jurisdiction Accuracy: 15% (correct jurisdiction applied?)
    - Latency: 10% (response speed)
    """
    result = run_subnet_query(query)
    return SubnetResponse(**result)


@router.get("/subnet/status", response_model=SubnetStatus, summary="Get subnet dashboard")
def subnet_status():
    """
    Returns the current status of the AI Legal Assistant subnet,
    including active miners, validators, emission rates, and performance metrics.
    """
    return SubnetStatus(**get_subnet_status())
