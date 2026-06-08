"""Streamlit app for financial reporting."""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from loguru import logger

from medas_financial_reporting.config import (
    S3_BUCKET,
    S3_DATA_PROCESSED_KEY,
    S3_OUTPUT_KEY,
)
from medas_financial_reporting.storage import get_fs


def run():
    """Entry point pour lancer l'app Streamlit."""
    import sys

    from streamlit.web import cli as stcli

    sys.argv = ["streamlit", "run", __file__]
    stcli.main()


# Palette partagée
PALETTE = {
    "PP": "#2C5F8A",
    "PM": "#7BAFD4",
    "V": "#4A7FA5",
    "O": "#6B9EBF",
    "R": "#8DBDD8",
    "S": "#B0CDE0",
    "N": "#D0E4EF",
    "AUTO": "#2C5F8A",
    "MANUEL": "#7BAFD4",
}


@st.cache_data
def load_data() -> pd.DataFrame:
    """Charge les données nettoyées depuis MinIO."""
    fs = get_fs()
    with fs.open(f"{S3_BUCKET}/{S3_DATA_PROCESSED_KEY}", "rb") as f:
        return pd.read_parquet(f)


@st.cache_data
def load_reporting() -> bytes:
    """Charge le reporting final depuis MinIO."""
    fs = get_fs()
    with fs.open(f"{S3_BUCKET}/{S3_OUTPUT_KEY}", "rb") as f:
        return f.read()


def plot_bar(series: pd.Series, title: str) -> plt.Figure:
    """Génère un graphique en barres avec la palette partagée."""
    fig, ax = plt.subplots(figsize=(6, 3))
    colors = [PALETTE.get(str(k), "#7BAFD4") for k in series.index]
    series.plot(kind="bar", ax=ax, color=colors, edgecolor="white", linewidth=0.5)
    ax.set_title(title, fontsize=12, pad=10)
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=0)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


def main():
    st.set_page_config(
        page_title="Reporting Financier",
        page_icon="📊",
        layout="wide",
    )

    # Sidebar
    st.sidebar.title("📊 Reporting Financier")
    st.sidebar.markdown("---")

    try:
        reporting_bytes = load_reporting()
        if st.sidebar.download_button(
            label="📥 Télécharger le reporting",
            data=reporting_bytes,
            file_name="Reporting_Financier.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ):
            logger.info("Reporting téléchargé")
    except Exception:
        st.sidebar.warning("Reporting non disponible")

    st.sidebar.markdown("---")

    # Chargement des données
    with st.spinner("Chargement des données..."):
        df = load_data()

    st.title("Vue d'ensemble")
    st.caption(f"{len(df):,} clients")

    # Métriques
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Clients PP", df[df["type_client"] == "PP"].shape[0])
    col2.metric("Clients PM", df[df["type_client"] == "PM"].shape[0])
    col3.metric("DRC complets", int(df["drc_complet"].sum()))
    col4.metric("Scorés AUTO", int((df["id_agent"] == "AUTO").sum()))

    st.markdown("---")

    # Graphiques
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_bar(df["type_client"].value_counts(), "Répartition PP / PM"))
    with col2:
        st.pyplot(plot_bar(df["score"].value_counts(), "Distribution des scores"))

    col3, col4 = st.columns(2)
    with col3:
        st.pyplot(plot_bar(df["id_agent"].value_counts(), "Répartition AUTO / MANUEL"))
    with col4:
        drc_rate = df.groupby("type_client")["drc_complet"].mean() * 100
        st.pyplot(plot_bar(drc_rate, "Taux DRC complété (%)"))

    # Matrice des scores
    st.markdown("---")
    st.subheader("Matrice de transition des scores")
    transition = pd.crosstab(df["score_prev"], df["score"], margins=True)
    st.dataframe(transition, width="stretch")

    # Exploration
    st.markdown("---")
    st.subheader("Exploration personnalisée")
    col1, col2 = st.columns(2)
    with col1:
        type_sel = st.multiselect("Type de client", df["type_client"].unique())
    with col2:
        score_sel = st.multiselect("Score", df["score"].unique())

    df_filtered = df.copy()
    if type_sel:
        df_filtered = df_filtered[df_filtered["type_client"].isin(type_sel)]
    if score_sel:
        df_filtered = df_filtered[df_filtered["score"].isin(score_sel)]

    st.dataframe(df_filtered, width="stretch")
    st.caption(f"{len(df_filtered):,} lignes affichées")


if __name__ == "__main__":
    main()
