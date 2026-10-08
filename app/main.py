from __future__ import annotations

from app.schemas import MatchPredictionRequest, MatchPredictionResponse
from app.predictor import predict_match


def analyze_match(request: MatchPredictionRequest) -> MatchPredictionResponse:
    return predict_match(request.home_team, request.away_team)
