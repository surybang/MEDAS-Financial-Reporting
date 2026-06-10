"""Entry point for the financial reporting pipeline."""

from medas_financial_reporting import (
    download_template,
    get_fs,
    init_minio_structure,
    save_processed_data,
    upload_reporting,
)
from medas_financial_reporting.config import (
    LOCAL_TMP_DIR,
    S3_BUCKET,
)
from medas_financial_reporting.financial_reporting import (
    clean_data,
    fill_indicators,
    get_data,
    write_data_to_excel,
)


def main() -> None:

    bucket = S3_BUCKET

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
