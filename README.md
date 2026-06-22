# MEDAS Financial Reporting

> Automatiser la génération d'un reporting financier Excel avec Python, du notebook au déploiement continu.

Ce dépôt accompagne un tutoriel pédagogique destiné aux étudiants du **Master MEDAS**. Il sert de fil rouge à un cours sur la reproductibilité, la mise en production et les bonnes pratiques à adopter lorsque l'on développe un projet de données : on part d'un simple notebook et on le transforme, étape par étape, en une véritable application déployée et livrée automatiquement.

## 🔗 Liens utiles

| Ressource | Lien |
| --- | --- |
| 📖 Le tutoriel complet | [surybang.github.io/MEDAS-Financial-Reporting](https://surybang.github.io/MEDAS-Financial-Reporting/) |
| 🚀 L'application en ligne | https://medas-financial-reporting.lab.sspcloud.fr/ |
| 📦 L'image Docker | [hub.docker.com/r/surybang/medas-financial-reporting](https://hub.docker.com/r/surybang/medas-financial-reporting) |
| 🔧 Le dépôt de déploiement (GitOps) | https://github.com/surybang/medas-financial-reporting-deployment |

## Données

Les données sont disponibles ici :
```
https://minio.lab.sspcloud.fr/fabienhos/td-reporting-financial/financial_data.parquet
```

### D'où viennent-elles ?
Les données ont été générées à partir d'un script dans un autre projet, elles sont totalement fictives mais représentatives d'un cas d'usage réel pour un reporting financier auprès d'un opérateur de contrôle.

## À qui s'adresse ce projet ?

Aux étudiants du **Master MEDAS** et plus largement à toute personne qui sait écrire un script Python qui "marche sur sa machine" et veut comprendre comment en faire un produit fiable, partageable et déployé. Aucune expertise en DevOps n'est requise au départ : le tutoriel construit chaque brique progressivement.

## Ce que fait le projet

À partir d'un jeu de données clients, le projet :

1. **charge et valide** les données brutes (contrôle de schéma)
2. **nettoie** les données et les persiste sur un stockage objet (MinIO / S3)
3. **génère** un reporting financier `Excel` à partir d'un template
4. **expose** le tout dans une application web interactive (`Streamlit`) où l'on consulte les indicateurs et télécharge le reporting

Le projet se compose de **deux data products** distincts : un **package** qui produit et persiste le reporting et une **application Streamlit** qui lit et expose le résultat. MinIO est le point de rencontre entre les deux.

## Stack technique

- **Python 3.13** avec [`uv`](https://docs.astral.sh/uv/) (gestion d'environnement, `src layout`, packaging)
- **pandas**, **openpyxl** pour la transformation et la génération Excel
- **pandera** pour la validation de schéma
- **Loguru** pour le logging
- **s3fs** pour le stockage objet
- **Streamlit** pour l'interface
- **ruff** (lint)
- **pytest** + **pytest-cov** (tests et couverture)
- **GitHub Actions** (CI/CD), **Docker**, **ArgoCD** (déploiement GitOps sur Kubernetes / SSP Cloud Onyxia)

## Lancer le projet en local

```bash
# Installer les dépendances
uv sync

# Générer le reporting
uv run reporting

# Lancer l'application
uv run app
```

> Le pipeline a besoin d'un accès à un stockage MinIO configuré via les variables d'environnement `AWS_S3_ENDPOINT`, `S3_BUCKET`, `AWS_ACCESS_KEY_ID` et `AWS_SECRET_ACCESS_KEY`.

## Le déploiement

L'application est déployée en **GitOps** : la `CI` build et publie l'image sur `Docker Hub` et **ArgoCD** surveille un dépôt de déploiement dédié (`medas-financial-reporting-deployment`) pour appliquer automatiquement tout changement sur le cluster. Le déploiement complet est documenté dans le tutoriel.

---