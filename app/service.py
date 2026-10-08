from __future__ import annotations

from app.predictor import compute_expected_goals, compute_goal_distribution, top_exact_scores
from app.schemas import ExactScore, MatchPredictionResponse, TeamStats


def predict_match(home_team: TeamStats, away_team: TeamStats) -> MatchPredictionResponse:
    home_rate, away_rate = compute_expected_goals(home_team, away_team)

    distribution = compute_goal_distribution(home_rate, away_rate, max_goals=8)
    over_2_5_probability = sum(distribution[i] for i in range(3, 9))

    # BTTS = 1 - prob that both teams score 0
    btts_probability = 1.0 - (
        (2.718281828459045 ** (-home_rate)) * (2.718281828459045 ** (-away_rate))
    )

    most_likely_total = max(distribution, key=distribution.get)
    exact_scores = [
        ExactScore(score=score, probability=round(probability, 6))
        for score, probability in top_exact_scores(home_rate, away_rate, limit=2)
    ]

    return MatchPredictionResponse(
        home_team=home_team.name,
        away_team=away_team.name,
        home_expected_goals=round(home_rate, 3),
        away_expected_goals=round(away_rate, 3),
        over_under_2_5="Over 2.5" if over_2_5_probability >= 0.5 else "Under 2.5",
        btts="Oui" if btts_probability >= 0.5 else "Non",
        btts_probability=round(btts_probability, 6),
        most_likely_total_goals=most_likely_total,
        exact_scores=exact_scores,
        goal_distribution={int(goal): round(prob, 8) for goal, prob in distribution.items()},
    )
