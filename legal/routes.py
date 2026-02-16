from fastapi import APIRouter
from .models import LegalQuery, LegalResponse
from .ai import get_legal_advice

router = APIRouter()

@router.post("/advice")
def advice(query: LegalQuery):
    result = get_legal_advice(query)
    return LegalResponse(**result)
