# MEDAS Financial Reporting

## Documentation

La documentation du projet est disponible ici : [surybang.github.io/MEDAS-Financial-Reporting](https://surybang.github.io/MEDAS-Financial-Reporting/)

## Contexte

🖊️ En cours d'écriture

## Données

Les données sont disponibles ici :
```
https://minio.lab.sspcloud.fr/fabienhos/td-reporting-financial/financial_data.parquet
```
### D'où viennent-elles ?
Les données ont été générées à partir d'un script dans un autre projet, elles sont totalement fictives mais représentatives d'un cas d'usage réel pour un reporting financier auprès d'un opérateur de contrôle.

## Point d'entrée

Le projet est constitué de plusieurs sous package.

Pour générer le reporting en ligne de commande  :
```bash
uv run reporting --bucket <nom_user_SSPCloud>
```