# Placeholder for DB logic
from .models import LegalQuery, LegalResponse

def get_db():
    return {"queries": [], "responses": []}

def add_legal_query(db, query: LegalQuery):
    db["queries"].append(query)

def add_legal_response(db, response: LegalResponse):
    db["responses"].append(response)
