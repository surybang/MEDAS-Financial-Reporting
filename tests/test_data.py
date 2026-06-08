"""Tests for data.py"""

import pandas as pd
import pytest

from medas_financial_reporting.financial_reporting.data import clean_data


@pytest.fixture
def raw_df():
    """DataFrame minimal simulant les données brutes."""
    return pd.DataFrame(
        {
            "type_client": ["PP", "PM", "PP"],
            "score": ["V", None, "R"],
            "score_prev": [None, "O", None],
            "id_agent": ["AUTO", "AGT001", "AUTO"],
            "drc_complet": [True, False, True],
        }
    )


def test_clean_data_fills_score(raw_df):
    """Les NaN de score sont remplacés par S."""
    result = clean_data(raw_df)
    assert result["score"].iloc[1] == "S"


def test_clean_data_fills_score_prev(raw_df):
    """Les NaN de score_prev sont remplacés par N."""
    result = clean_data(raw_df)
    assert result["score_prev"].iloc[0] == "N"
    assert result["score_prev"].iloc[2] == "N"


def test_clean_data_id_agent(raw_df):
    """Les agents non AUTO sont remplacés par MANUEL."""
    result = clean_data(raw_df)
    assert result["id_agent"].iloc[0] == "AUTO"
    assert result["id_agent"].iloc[1] == "MANUEL"


def test_clean_data_no_nulls(raw_df):
    """Après nettoyage, score et score_prev ne contiennent plus de NaN."""
    result = clean_data(raw_df)
    assert result["score"].isna().sum() == 0
    assert result["score_prev"].isna().sum() == 0


def test_clean_data_preserves_rows(raw_df):
    """clean_data ne supprime pas de lignes."""
    result = clean_data(raw_df)
    assert len(result) == len(raw_df)
