from __future__ import annotations

from math import exp, factorial
from typing import Dict, List, Tuple


def poisson_pmf(rate: float, k: int) -> float:
    if rate < 0:
        raise ValueError("rate must be >= 0")
    if k < 0:
        raise ValueError("k must be >= 0")
    return (exp(-rate) * (rate ** k)) / factorial(k)


def compute_expected_goals(home: object, away: object) -> Tuple[float, float]:
    """Simple expected goals estimate based on teams' offensive and defensive averages."""
    home_rate = ((home.goals_for_avg + away.goals_against_avg) / 2.0) * 0.95
    away_rate = ((away.goals_for_avg + home.goals_against_avg) / 2.0) * 0.95
    return home_rate, away_rate


def score_probability(home_rate: float, away_rate: float, home_goals: int, away_goals: int) -> float:
    return poisson_pmf(home_rate, home_goals) * poisson_pmf(away_rate, away_goals)


def total_goals_probability(home_rate: float, away_rate: float, total_goals: int) -> float:
    total = 0.0
    for home_goals in range(total_goals + 1):
        away_goals = total_goals - home_goals
        if away_goals < 0:
            continue
        total += score_probability(home_rate, away_rate, home_goals, away_goals)
    return total


def compute_goal_distribution(home_rate: float, away_rate: float, max_goals: int = 8) -> Dict[int, float]:
    distribution: Dict[int, float] = {}
    for total_goals in range(max_goals + 1):
        distribution[total_goals] = total_goals_probability(home_rate, away_rate, total_goals)
    return distribution


def top_exact_scores(home_rate: float, away_rate: float, limit: int = 2) -> List[Tuple[str, float]]:
    score_map: Dict[Tuple[int, int], float] = {}
    for home_goals in range(0, 7):
        for away_goals in range(0, 7):
            score_map[(home_goals, away_goals)] = score_probability(home_rate, away_rate, home_goals, away_goals)

    ranked = sorted(score_map.items(), key=lambda item: item[1], reverse=True)
    return [
        (f"{home_goals}-{away_goals}", probability)
        for (home_goals, away_goals), probability in ranked[:limit]
    ]
