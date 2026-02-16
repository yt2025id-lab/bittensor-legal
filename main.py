from fastapi import FastAPI
from legal.routes import router as legal_router

app = FastAPI(title="AI Legal Assistant Subnet")
app.include_router(legal_router)

@app.get("/")
def root():
    return {"message": "Welcome to the AI Legal Assistant Subnet powered by Bittensor!"}
