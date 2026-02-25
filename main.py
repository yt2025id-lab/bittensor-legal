from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from legal.routes import router as legal_router

app = FastAPI(
    title="AI Legal Assistant Subnet",
    description=(
        "Decentralized legal advisory subnet on Bittensor. "
        "Miners compete to provide the most accurate legal analysis with verified citations. "
        "Validators verify every citation against authoritative legal databases. "
        "TAO rewards distributed via Yuma Consensus."
    ),
    version="1.0.0",
)
app.include_router(legal_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", tags=["Root"])
def root():
    return FileResponse("static/index.html")
