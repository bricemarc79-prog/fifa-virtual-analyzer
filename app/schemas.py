from __future__ import annotations

from pydantic import BaseModel, Field, model_validator


class TeamStats(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    matches: int = Field(..., gt=0)
    wins: int = Field(..., ge=0)
    draws: int = Field(..., ge=0)
    losses: int = Field(..., ge=0)
    goals_for: int = Field(..., ge=0)
    goals_against: int = Field(..., ge=0)

    @model_validator(mode="after")
    def validate_match_totals(self):
        if self.wins + self.draws + self.losses != self.matches:
            raise ValueError("wins + draws + losses must equal matches")
        return self

    @property
    def goals_for_avg(self) -> float:
        return self.goals_for / self.matches if self.matches else 0.0

    @property
    def goals_against_avg(self) -> float:
        return self.goals_against / self.matches if self.matches else 0.0


class MatchPredictionRequest(BaseModel):
    home_team: TeamStats
    away_team: TeamStats


class ExactScore(BaseModel):
    score: str
    probability: float


class MatchPredictionResponse(BaseModel):
    home_team: str
    away_team: str
    home_expected_goals: float
    away_expected_goals: float
    over_under_2_5: str
    btts: str
    btts_probability: float
    most_likely_total_goals: int
    exact_scores: list[ExactScore]
    goal_distribution: dict[int, float]
