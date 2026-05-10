"""Data retrieval, cleaning and validation functions."""

import pandas as pd
import pandera.pandas as pa
from loguru import logger

from medas_financial_reporting.config import (
    DATA_URL,
    DATA_SCHEMA,
)


def get_data() -> pd.DataFrame:
    """
    Récupère et valide les données brutes depuis MinIO.

    Returns:
        pd.DataFrame: Les données brutes validées.

    Raises:
        pa.errors.SchemaError: Si les données ne respectent pas le schéma attendu.
        RuntimeError: Si le chargement des données échoue.
    """
    logger.info(f"Chargement des données depuis {DATA_URL}")
    try:
        df = pd.read_parquet(DATA_URL)
        DATA_SCHEMA.validate(df)
        logger.success(f"{len(df)} lignes chargées et validées")
        return df
    except pa.errors.SchemaError as e:
        logger.critical(f"Violation du schéma métier : {e}")
        raise
    except Exception as e:
        logger.critical(f"Impossible de charger les données : {e}")
        raise RuntimeError(f"Impossible de charger les données : {e}") from e


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applique les transformations métier sur les données brutes.

    Args:
        df: DataFrame contenant les données brutes et validées.

    Returns:
        pd.DataFrame: DataFrame contenant les données nettoyées.
    """
    logger.info("Nettoyage des données")
    df = df.assign(
        score=df["score"].fillna("S"),
        score_prev=df["score_prev"].fillna("N"),
        id_agent=df["id_agent"].where(df["id_agent"] == "AUTO", "MANUEL"),
    )
    logger.success(f"{len(df)} lignes nettoyées")
    return df
