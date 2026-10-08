# FIFA Virtual Match Analyzer

Application Python pour analyser les matchs virtuels FIFA et prévoir les tendances de buts, le BTTS (Both Teams To Score), les scores exacts probables et les opportunités Over/Under.

Objectifs :
- saisir les statistiques d'une équipe à domicile et d'une équipe à l'extérieur
- calculer les taux attendus de buts
- estimer le nombre probable de buts
- afficher le BTTS Oui/Non
- proposer les 2 scores exacts les plus probables
- publier une API simple avec FastAPI

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
└── run.py
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Lancer l'API

```bash
uvicorn app.main:app --reload
```

Puis ouvrir :
- http://127.0.0.1:8000/docs

## Exemple de payload JSON

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
  "home_expected_goals": 1.56,
  "away_expected_goals": 1.31,
  "over_under_2_5": "Over 2.5",
  "btts": "Oui",
  "btts_probability": 0.58,
  "most_likely_total_goals": 2,
  "exact_scores": [
    {"score": "1-1", "probability": 0.21},
    {"score": "2-1", "probability": 0.17}
  ]
}
```

## Modèle de calcul

Le projet utilise une approximation par distribution de Poisson sur la base des statistiques fournies par l'utilisateur :
- moyennes de buts marqués
- moyennes de buts encaissés
- estimation du total attendu de buts
- calcul de probabilités pour les scores exacts et le BTTS

## Valeur ajoutée

Ce projet est conçu pour servir de base à un moteur de prédiction d'analyse de matchs FIFA virtuels, avec une architecture simple à étendre.

## À propos

Ce dépôt est une version initiale, open et modulable, destinée à évoluer avec :
- intégration de données externes
- historique de matchs
- pont avec des bookmakers partenaires
- interface web
- model de scoring plus avancé

## Licence

MIT