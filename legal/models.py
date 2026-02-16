from pydantic import BaseModel

class LegalQuery(BaseModel):
    user_id: str
    case_type: str
    description: str

class LegalResponse(BaseModel):
    summary: str
    references: list
    recommendation: str
