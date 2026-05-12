"""Entry point for the financial reporting pipeline."""

import s3fs
from loguru import logger
import argparse

from medas_financial_reporting.config import (
    S3_ENDPOINT,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_SESSION_TOKEN,
    S3_BUCKET,
    S3_TEMPLATE_KEY,
    S3_DATA_PROCESSED_KEY,
    S3_OUTPUT_KEY,
    LOCAL_TMP_DIR,
    LOCAL_TEMPLATE,
    LOCAL_OUTPUT,
)
from medas_financial_reporting.financial_reporting import (
    write_data_to_excel,
    fill_indicators,
    get_data,
    clean_data,
)


def get_fs() -> s3fs.S3FileSystem:
    endpoint = S3_ENDPOINT
    if not endpoint.startswith("https://"):
        endpoint = f"https://{endpoint}"
    return s3fs.S3FileSystem(
        endpoint_url=endpoint,
        key=AWS_ACCESS_KEY_ID,
        secret=AWS_SECRET_ACCESS_KEY,
        token=AWS_SESSION_TOKEN,
    )


def init_minio_structure(fs: s3fs.S3FileSystem, bucket):
    folders = [
        f"{bucket}/MEDAS-FinancialReporting/data/proccesed/.keep",
        f"{bucket}/MEDAS-FinancialReporting/data/raw/.keep",
        f"{bucket}/MEDAS-FinancialReporting/template/.keep",
        f"{bucket}/MEDAS-FinancialReporting/output/.keep",
    ]

    for path in folders:
        if not fs.exists(path):
            with fs.open(path, "wb") as f:
                f.write(b"")
                logger.debug(f"Dossier créé : {path}")
        logger.info("Structure minio déjà existante")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bucket",
        type=str,
        default=S3_BUCKET,
        help="Nom de votre bucket"
    )
    return parser.parse_args()


def main() -> None:
    # Parser les paramètres pour la reproductibilité
    args = parse_args()
    bucket = args.bucket

    LOCAL_TMP_DIR.mkdir(exist_ok=True)
    # Intialiser le filesystem
    fs = get_fs()

    # Créer la structure sur MinIO si elles n'existent pas
    init_minio_structure(fs, bucket)

    # Récupérer et valider les données brutes
    df = get_data()

    # Nettoyer les données
    df = clean_data(df)

    # Sauvegarder les données nettoyées sur MinIO
    logger.info("Sauvegarde des données nettoyées")
    with fs.open(f"{bucket}/{S3_DATA_PROCESSED_KEY}", "wb") as f:
        df.to_parquet(f)
    logger.success("Données nettoyées sauvegardées")

    # Télécharger le template
    logger.info("Téléchargement du template")
    fs.get(f"{bucket}/{S3_TEMPLATE_KEY}", str(LOCAL_TEMPLATE))
    logger.success("Template téléchargé")

    # Insérer les données et remplir les indicateurs
    write_data_to_excel(df)
    fill_indicators()

    # Uploader le reporting final
    logger.info("Upload du reporting vers MinIO")
    fs.put(str(LOCAL_OUTPUT), f"{S3_BUCKET}/{S3_OUTPUT_KEY}")
    logger.success("Reporting disponible sur MinIO")


if __name__ == "__main__":
    main()
