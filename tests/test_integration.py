# tests/test_integration.py
"""Tests d'intégration."""

import pytest
import pandas as pd

from medas_financial_reporting.financial_reporting.data import get_data


@pytest.mark.integration
def test_get_data_returns_dataframe():
    """Vérifie que get_data retourne bien un DataFrame non vide."""
    df = get_data()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


@pytest.mark.integration
def test_get_data_expected_columns():
    """Vérifie que les colonnes attendues sont présentes."""
    df = get_data()
    expected = {"type_client", "score", "score_prev", "id_agent", "drc_complet"}
    assert expected.issubset(set(df.columns))


@pytest.mark.integration
def test_get_data_schema_valid():
    """Vérifie que le schéma Pandera est respecté."""
    df = get_data()
    assert df["type_client"].isin(["PP", "PM"]).all()
    assert df["drc_complet"].dtype == bool
