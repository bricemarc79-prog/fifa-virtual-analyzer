# FIFA Virtual Match Analyzer

Ce projet est un moteur Python pour analyser un match virtuel FIFA à partir des statistiques d'équipe fournies par l'utilisateur :
- équipe à domicile
- équipe à l'extérieur
- matchs joués
- victoires, nuls, défaites
- buts marqués et encaissés

Il calcule ensuite :
- Over / Under 2.5
- BTTS Oui / Non
- nombre probable de buts
- 2 scores exacts les plus probables

## Structure du projet

```text
fifa-virtual-analyzer/
├── app/
│   ├── __init__.py
│   ├── schemas.py
│   ├── predictor.py
│   ├── service.py
│   └── main.py
├── .gitignore
├── README.md
├── requirements.txt
├── run.py
└── .venv/
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Lancer l'API

```bash
uvicorn app.main:app --reload
```

Puis ouvrez :
- http://127.0.0.1:8000/docs

## Exemple de requête

```json
{
  "home_team": {
    "name": "Paris FC",
    "matches": 20,
    "wins": 9,
    "draws": 6,
    "losses": 5,
    "goals_for": 31,
    "goals_against": 24
  },
  "away_team": {
    "name": "Lyon",
    "matches": 20,
    "wins": 8,
    "draws": 5,
    "losses": 7,
    "goals_for": 27,
    "goals_against": 29
  }
}
```

## Exemple de réponse

```json
{
  "home_team": "Paris FC",
  "away_team": "Lyon",
  "home_expected_goals": 1.483,
  "away_expected_goals": 1.233,
  "over_under_2_5": "Over 2.5",
  "btts": "Oui",
  "btts_probability": 0.612123,
  "most_likely_total_goals": 2,
  "exact_scores": [
    {"score": "1-1", "probability": 0.168123},
    {"score": "2-1", "probability": 0.141211}
  ],
  "goal_distribution": {
    "0": 0.087,
    "1": 0.219,
    "2": 0.271,
    "3": 0.215,
    "4": 0.121,
    "5": 0.057,
    "6": 0.022,
    "7": 0.006,
    "8": 0.002
  }
}
```

## Détails du modèle

Le calcul repose sur une estimation de buts attendus par équipe, puis sur une approximation de distribution de Poisson.

Formule simplifiée :
- butes attendus domicile = moyenne de but marqués domicile + moyenne de but encaissés extérieur / 2
- butes attendus extérieur = moyenne de but marqués extérieur + moyenne de but encaissés domicile / 2

Ensuite, on calcule les probabilités de :
- score exact
- total de buts
- Over / Under 2.5
- BTTS

## Remarque importante

Il s'agit d'un modèle statistique de base. Il ne s'agit pas d'une API officielle de bookmakers. Le projet est pensé comme un moteur d'analyse interne, facilement extensible.

## Licence

MIT
