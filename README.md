# TD - Financial Reporting

## Contexte

Vous travaillez pour une institution financière qui gère un portefeuille de clients particuliers (PP) et professionnels (PM). Chaque client est associé à un score de risque (`score`) et un score précédent (`score_prev`) permettant de suivre l'évolution de son profil.

Le champ `drc_complet` indique si le dossier réglementaire du client est complet. L'`id_agent` identifie l'action d'un conseiller sur le profil du client.

L'objectif de ce TD est de produire *automatiquement* un rapport Excel de suivi à partir de ces données brutes.

## Démarrage

### 1. Créez votre dépôt depuis le template

Cliquez sur **Use this template** → **Create a new repository**

> Donnez-lui un nom explicite, ex: `td-reporting-<votre-prenom>`

### 2. Clonez votre dépôt

```bash
git clone https://github.com/<votre-username>/<nom-du-repo>.git
cd <nom-du-repo>
```

## Données

Les données sont disponibles ici :
```
https://minio.lab.sspcloud.fr/fabienhos/td-reporting-financial/financial_data.parquet
```

## Partie 1 — Exploration dans le notebook

Commencez par `notebook.ipynb`. Cette partie est intentionnellement libre : 
c'est un espace d'expérimentation pour forger vos intuitions.

## Partie 2 — Structuration du code

Une fois l'exploration terminée et votre logique validée dans le notebook, 
vous allez **restructurer votre code en projet Python modulable**.

### Pourquoi cette étape ?

Un notebook est pratique pour explorer, mais difficile à maintenir, tester et 
déployer. L'objectif est de transformer votre code en modules réutilisables.

### Structure cible potentielle

```
<projet>/
├── notebooks/
│   └── notebook.ipynb          # Vous pouvez garder le notebook en guise d'archive
├── output/
│   └── Reporting_Financier_2026-05-02.xlsx  # Fichier de sortie
├── template/
│   └── template_reporting.xlsx # Template pour générer le fichier de sortie
├── .gitignore
├── .python-version
├── config.py                   # Variables et constantes de configuration
├── main.py                     # Point d'entrée du projet
├── pyproject.toml
├── README.md
├── utils.py                    # Fonctions pour générer le reporting
└── uv.lock
```

### Point d'entrée

`main.py` doit pouvoir s'exécuter en une commande :

```bash
uv run main.py
```

Cette commande doit générer le reporting au format Excel.

### Conseils de migration notebook → scripts

- Chaque cellule qui *fait quelque chose* devient une **fonction**
- Chaque fonction va dans le module qui correspond à sa responsabilité
- Le notebook peut rester comme documentation / démonstration

## Objectifs pédagogiques

- Lire des données au format Parquet
- Explorer et nettoyer un DataFrame
- Générer un rapport Excel avec `openpyxl` et `pandas`
- Structurer son code et sa pensée.
- Passer d'un notebook exploratoire à un **projet Python structuré et exécutable**
