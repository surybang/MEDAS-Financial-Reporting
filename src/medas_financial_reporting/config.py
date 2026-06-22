"""Configuration file for the project."""

import os
import sys
from datetime import datetime
from pathlib import Path

from loguru import logger
from pandera.pandas import Check, Column, DataFrameSchema, Timestamp

# Logger
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

logger.remove()
logger.add(
    sys.stderr,
    level=LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",  # noqa: E501
)

# Données source
DATA_URL = "https://minio.lab.sspcloud.fr/fabienhos/MEDAS-FinancialReporting/data/raw/financial_data.parquet"  # noqa: E501

# Template URL
TEMPLATE_URL = "https://minio.lab.sspcloud.fr/fabienhos/MEDAS-FinancialReporting/template/template_reporting.xlsx"  # noqa: E501

# MinIO
S3_ENDPOINT = os.environ.get("AWS_S3_ENDPOINT", "")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN", "")
S3_BUCKET = os.environ.get("S3_BUCKET", "fabienhos")

# Chemins MinIO
S3_DATA_PROCESSED_KEY = "MEDAS-FinancialReporting/data/processed/financial_data.parquet"
S3_OUTPUT_KEY = "MEDAS-FinancialReporting/output/reporting.xlsx"

# Chemins locaux temporaires
today = datetime.today().strftime("%Y-%m-%d")
LOCAL_TMP_DIR = Path("tmp")
LOCAL_TEMPLATE = LOCAL_TMP_DIR / "template_reporting.xlsx"
LOCAL_OUTPUT = LOCAL_TMP_DIR / f"Reporting_Financier_{today}.xlsx"

# Excel
SHEET_DATA = "DATA"
SHEET_INDICATORS = "Indicateurs"

INDICATORS = [
    # Répartition PP/PM
    {"row": 8, "formule": "COUNTIF", "args": [("B", "PP")]},
    {"row": 9, "formule": "COUNTIF", "args": [("B", "PM")]},
    {"row": 10, "formule": "SUM", "args": "E8:E9"},
    # Scores V/O/R/S
    {"row": 14, "formule": "COUNTIFS", "args": [("B", "PP"), ("D", "V")]},
    {"row": 15, "formule": "COUNTIFS", "args": [("B", "PP"), ("D", "O")]},
    {"row": 16, "formule": "COUNTIFS", "args": [("B", "PP"), ("D", "R")]},
    {"row": 17, "formule": "COUNTIFS", "args": [("B", "PP"), ("D", "S")]},
    {"row": 18, "formule": "SUM", "args": "E14:E17"},
    # DRC Complet
    {"row": 22, "formule": "COUNTIFS", "args": [("B", "PP"), ("G", "VRAI")]},
    {"row": 23, "formule": "COUNTIFS", "args": [("B", "PM"), ("G", "VRAI")]},
    {"row": 24, "formule": "SUM", "args": "E22:E23"},
    # Focus V/O
    {"row": 28, "formule": "COUNTIFS", "args": [("B", "PP"), ("D", "V")]},
    {"row": 29, "formule": "COUNTIFS", "args": [("B", "PM"), ("D", "V")]},
    {"row": 30, "formule": "SUM", "args": "E28:E29"},
    {"row": 31, "formule": "COUNTIFS", "args": [("B", "PP"), ("D", "O")]},
    {"row": 32, "formule": "COUNTIFS", "args": [("B", "PM"), ("D", "O")]},
    {"row": 33, "formule": "SUM", "args": "E31:E32"},
    # Focus V/O avec DRC complet
    {
        "row": 34,
        "formule": "COUNTIFS",
        "args": [("B", "PP"), ("D", "V"), ("G", "VRAI")],
    },
    {
        "row": 35,
        "formule": "COUNTIFS",
        "args": [("B", "PM"), ("D", "V"), ("G", "VRAI")],
    },
    {"row": 36, "formule": "SUM", "args": "E34:E35"},
    {
        "row": 37,
        "formule": "COUNTIFS",
        "args": [("B", "PP"), ("D", "O"), ("G", "VRAI")],
    },
    {
        "row": 38,
        "formule": "COUNTIFS",
        "args": [("B", "PM"), ("D", "O"), ("G", "VRAI")],
    },
    {"row": 39, "formule": "SUM", "args": "E37:E38"},
    # Focus R
    {"row": 43, "formule": "COUNTIFS", "args": [("B", "PP"), ("D", "R")]},
    {"row": 44, "formule": "COUNTIFS", "args": [("B", "PM"), ("D", "R")]},
    {"row": 45, "formule": "SUM", "args": "E43:E44"},
    {"row": 46, "formule": "COUNTIFS", "args": [("D", "R"), ("F", "AUTO")]},
    {"row": 47, "formule": "COUNTIFS", "args": [("D", "R"), ("F", "MANUEL")]},
    {"row": 48, "formule": "SUM", "args": "E46:E47"},
    # R avec DRC complet
    {
        "row": 49,
        "formule": "COUNTIFS",
        "args": [("B", "PP"), ("D", "R"), ("G", "VRAI")],
    },
    {
        "row": 50,
        "formule": "COUNTIFS",
        "args": [("B", "PM"), ("D", "R"), ("G", "VRAI")],
    },
    {"row": 51, "formule": "SUM", "args": "E49:E50"},
    # Nouveaux clients (score_prev = N)
    {
        "row": 52,
        "formule": "COUNTIFS",
        "args": [("B", "PP"), ("E", "N"), ("G", "VRAI")],
    },
    {
        "row": 53,
        "formule": "COUNTIFS",
        "args": [("B", "PM"), ("E", "N"), ("G", "VRAI")],
    },
    {"row": 54, "formule": "SUM", "args": "E52:E53"},
]

DATA_SCHEMA = DataFrameSchema(
    {
        "client_id": Column(int, nullable=False),
        "type_client": Column(
            str, Check(lambda s: s.isin(["PP", "PM"])), nullable=False
        ),
        "date_adhesion": Column(Timestamp, nullable=False),
        "score": Column(str, Check(lambda s: s.isin(["V", "O", "R"])), nullable=True),
        "score_prev": Column(
            str, Check(lambda s: s.isin(["V", "O", "R"])), nullable=True
        ),
        "id_agent": Column(str, nullable=False),
        "drc_complet": Column(bool, nullable=False),
    },
    strict=True,
)
