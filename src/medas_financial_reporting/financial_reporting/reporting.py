"""Reporting generation functions."""

import s3fs
from openpyxl import load_workbook
from loguru import logger

from medas_financial_reporting.config import (
    S3_BUCKET,
    S3_TEMPLATE_KEY,
    S3_OUTPUT_KEY,
    LOCAL_TEMPLATE,
    LOCAL_OUTPUT,
    LOCAL_TMP_DIR,
    SHEET_INDICATORS,
    INDICATORS,
)


def download_template(fs: s3fs.S3FileSystem) -> None:
    """
    Télécharge le template Excel depuis MinIO vers le dossier temporaire.

    Args:
        fs: Filesystem S3.
    """
    LOCAL_TMP_DIR.mkdir(exist_ok=True)
    logger.info(f"Téléchargement du template depuis {S3_TEMPLATE_KEY}")
    try:
        fs.get(f"{S3_BUCKET}/{S3_TEMPLATE_KEY}", str(LOCAL_TEMPLATE))
        logger.success("Template téléchargé")
    except Exception as e:
        logger.critical(f"Impossible de télécharger le template : {e}")
        raise RuntimeError(f"Impossible de télécharger le template : {e}") from e


def write_data_to_excel(df) -> None:
    """
    Insère le DataFrame dans la feuille DATA du template.

    Args:
        df: DataFrame nettoyé.
    """
    import pandas as pd

    logger.info("Insertion des données dans le template")
    try:
        with pd.ExcelWriter(
            LOCAL_TEMPLATE,
            mode="a",
            engine="openpyxl",
            if_sheet_exists="replace",
        ) as writer:
            df.to_excel(writer, sheet_name="DATA", index=False)
        logger.success("Données insérées")
    except Exception as e:
        logger.error(f"Impossible d'insérer les données : {e}")
        raise RuntimeError(f"Impossible d'insérer les données : {e}") from e


def fill_indicators(data_sheet: str = "DATA") -> None:
    """
    Remplit les indicateurs dans la feuille Indicateurs.

    Args:
        data_sheet: Nom de la feuille de données.
    """
    logger.info("Remplissage des indicateurs")

    def formula_countif(col: str, val: str) -> str:
        return f'=COUNTIF({data_sheet}!{col}:{col}, "{val}")'

    def formula_countifs(pairs: list[tuple[str, str]]) -> str:
        conditions = ", ".join(
            f'{data_sheet}!{col}:{col}, "{val}"' for col, val in pairs
        )
        return f"=COUNTIFS({conditions})"

    def formula_sum(range_str: str) -> str:
        return f"=SUM({range_str})"

    wb = load_workbook(LOCAL_TEMPLATE)
    ws = wb[SHEET_INDICATORS]

    for item in INDICATORS:
        cell = f"E{item['row']}"
        if item["formule"] == "COUNTIF":
            ws[cell] = formula_countif(*item["args"][0])
        elif item["formule"] == "COUNTIFS":
            ws[cell] = formula_countifs(item["args"])
        elif item["formule"] == "SUM":
            ws[cell] = formula_sum(item["args"])
        else:
            raise ValueError(f"Formule inconnue : {item['formule']}")

    wb.save(LOCAL_OUTPUT)
    wb.close()
    logger.success(f"Reporting généré : {LOCAL_OUTPUT}")


def upload_reporting(fs: s3fs.S3FileSystem) -> None:
    """
    Upload le reporting final vers MinIO.

    Args:
        fs: Filesystem S3.
    """
    logger.info(f"Upload du reporting vers {S3_OUTPUT_KEY}")
    try:
        fs.put(str(LOCAL_OUTPUT), f"{S3_BUCKET}/{S3_OUTPUT_KEY}")
        logger.success("Reporting uploadé")
    except Exception as e:
        logger.error(f"Impossible d'uploader le reporting : {e}")
        raise RuntimeError(f"Impossible d'uploader le reporting : {e}") from e
