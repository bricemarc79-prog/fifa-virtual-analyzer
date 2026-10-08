from __future__ import annotations

from fastapi import FastAPI

from app.schemas import MatchPredictionRequest, MatchPredictionResponse
from app.service import analyze_match

app = FastAPI(
    title="FIFA Virtual Match Analyzer",
    description="Analyse des matchs virtuels FIFA et prédiction de résultats",
    version="0.1.0",
)


@app.get("/")
def home() -> dict:
    return {
        "message": "Bienvenue dans l'API FIFA Virtual Match Analyzer",
        "docs": "/docs",
    }


@app.post("/predict", response_model=MatchPredictionResponse)
def predict(request: MatchPredictionRequest) -> MatchPredictionResponse:
    return analyze_match(request)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
