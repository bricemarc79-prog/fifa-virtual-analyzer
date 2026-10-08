from __future__ import annotations

from typing import Dict, List

from app.schemas import ExactScore, MatchPredictionResponse, TeamInput
from app.predictor import compute_expected_goals, compute_goal_distribution, top_exact_scores


def predict_match(home_team: TeamInput, away_team: TeamInput) -> MatchPredictionResponse:
    home_rate, away_rate = compute_expected_goals(home_team, away_team)

    distribution = compute_goal_distribution(home_rate, away_rate, max_goals=8)
    total_goals_prob = sum(distribution.values())
    if total_goals_prob == 0:
        total_goals_prob = 1.0

    over_2_5 = sum(distribution[i] for i in range(3, 9))
    under_2_5 = 1.0 - over_2_5

    btts_prob = 1.0 - (
        (2.718281828459045 ** (-home_rate)) * (2.718281828459045 ** (-away_rate))
    )

    most_likely_total = max(distribution, key=distribution.get)
    top_scores = top_exact_scores(home_rate, away_rate, limit=2)

    exact_scores: List[ExactScore] = [
        ExactScore(score=score, probability=round(probability, 6))
        for score, probability in top_scores
    ]

    return MatchPredictionResponse(
        home_team=home_team.name,
        away_team=away_team.name,
        home_expected_goals=round(home_rate, 3),
        away_expected_goals=round(away_rate, 3),
        over_under_2_5="Over 2.5" if over_2_5 >= 0.5 else "Under 2.5",
        btts="Oui" if btts_prob >= 0.5 else "Non",
        btts_probability=round(btts_prob, 6),
        most_likely_total_goals=most_likely_total,
        exact_scores=exact_scores,
        goal_distribution={int(goal): round(prob, 8) for goal, prob in distribution.items()},
    )
