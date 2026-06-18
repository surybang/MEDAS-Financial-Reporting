"""Storage functions for MinIO interactions."""

import pandas as pd
import s3fs
from loguru import logger

from medas_financial_reporting.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_SESSION_TOKEN,
    LOCAL_OUTPUT,
    LOCAL_TEMPLATE,
    LOCAL_TMP_DIR,
    S3_DATA_PROCESSED_KEY,
    S3_ENDPOINT,
    S3_OUTPUT_KEY,
    S3_TEMPLATE_KEY,
)


def get_fs() -> s3fs.S3FileSystem:
    """Retourne un filesystem S3 authentifié."""
    endpoint = S3_ENDPOINT
    if not endpoint.startswith("https://"):
        endpoint = f"https://{endpoint}"
    return s3fs.S3FileSystem(
        endpoint_url=endpoint,
        key=AWS_ACCESS_KEY_ID,
        secret=AWS_SECRET_ACCESS_KEY,
        token=AWS_SESSION_TOKEN,
    )


def download_template(fs: s3fs.S3FileSystem, bucket: str) -> None:
    """Télécharge le template Excel depuis MinIO."""
    LOCAL_TMP_DIR.mkdir(exist_ok=True)
    logger.info(f"Téléchargement du template depuis {S3_TEMPLATE_KEY}")
    try:
        fs.get(f"{bucket}/{S3_TEMPLATE_KEY}", str(LOCAL_TEMPLATE))
        logger.success("Template téléchargé")
    except Exception as e:
        logger.critical(f"Impossible de télécharger le template : {e}")
        raise RuntimeError(f"Impossible de télécharger le template : {e}") from e


def upload_reporting(fs: s3fs.S3FileSystem, bucket: str) -> None:
    """Upload le reporting final vers MinIO."""
    logger.info(f"Upload du reporting vers {S3_OUTPUT_KEY}")
    try:
        fs.put(str(LOCAL_OUTPUT), f"{bucket}/{S3_OUTPUT_KEY}")
        logger.success("Reporting uploadé")
    except Exception as e:
        logger.error(f"Impossible d'uploader le reporting : {e}")
        raise RuntimeError(f"Impossible d'uploader le reporting : {e}") from e


def init_minio_structure(fs: s3fs.S3FileSystem, bucket):
    """Génère la structure attendue pour le projet dans le stockage distant si elle n'existe pas."""  # noqa: E501
    folders = [
        f"{bucket}/MEDAS-FinancialReporting/data/processed/",
        f"{bucket}/MEDAS-FinancialReporting/data/raw/",
        f"{bucket}/MEDAS-FinancialReporting/template/",
        f"{bucket}/MEDAS-FinancialReporting/output/",
    ]

    for path in folders:
        if not fs.exists(path):
            with fs.open(path, "wb") as f:
                f.write(b"")
                logger.debug(f"Dossier créé : {path}")
    logger.info("Structure minio déjà existante")


def save_processed_data(fs: s3fs.S3FileSystem, df: pd.DataFrame, bucket: str) -> None:
    """Sauvegarde les données nettoyées sur MinIO."""
    path = f"{bucket}/{S3_DATA_PROCESSED_KEY}"
    logger.info(f"Sauvegarde des données nettoyées vers {path}")
    try:
        with fs.open(path, "wb") as f:
            df.to_parquet(f)
        logger.success("Données nettoyées sauvegardées")
    except Exception as e:
        logger.error(f"Impossible de sauvegarder les données : {e}")
        raise RuntimeError(f"Impossible de sauvegarder les données : {e}") from e


def read_processed_data(fs: s3fs.S3FileSystem, bucket: str) -> pd.DataFrame:
    """Charge les données nettoyées depuis MinIO."""
    path = f"{bucket}/{S3_DATA_PROCESSED_KEY}"
    logger.info(f"Chargement des données nettoyées depuis {path}")
    try:
        with fs.open(path, "rb") as f:
            return pd.read_parquet(f)
    except Exception as e:
        logger.error(f"Impossible de charger les données : {e}")
        raise RuntimeError(f"Impossible de charger les données : {e}") from e


def read_reporting(fs: s3fs.S3FileSystem, bucket: str) -> bytes:
    """Charge le reporting final depuis MinIO."""
    path = f"{bucket}/{S3_OUTPUT_KEY}"
    logger.info(f"Chargement du reporting depuis {path}")
    try:
        with fs.open(path, "rb") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Impossible de charger le reporting : {e}")
        raise RuntimeError(f"Impossible de charger le reporting : {e}") from e
