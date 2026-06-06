"""Entry point for the financial reporting pipeline."""

import argparse

from medas_financial_reporting.config import (
    S3_BUCKET,
    LOCAL_TMP_DIR,
)
from medas_financial_reporting.financial_reporting import (
    write_data_to_excel,
    fill_indicators,
    get_data,
    clean_data,
)
from medas_financial_reporting import (
    init_minio_structure,
    get_fs,
    download_template,
    upload_reporting,
    save_processed_data,
)


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
    save_processed_data(fs, df, bucket)

    # Télécharger le template
    download_template(fs, bucket)

    # Insérer les données et remplir les indicateurs
    write_data_to_excel(df)
    fill_indicators()

    # Uploader le reporting sur MinIO
    upload_reporting(fs, bucket)


if __name__ == "__main__":
    main()
