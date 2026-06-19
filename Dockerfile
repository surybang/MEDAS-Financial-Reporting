# Image de base : Python 3.13 en version slim
FROM python:3.13-slim

# Copie du binaire uv depuis l'image officielle (pas besoin de l'installer à la main)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copie des fichiers de dépendances d'abord (pour profiter du cache des layers)
COPY pyproject.toml uv.lock ./

# Installation des dépendances (sans les dépendances de dev)
RUN uv sync --frozen --no-dev --no-install-project

# Copie du reste du code source
COPY . .

# Installation du projet lui-même
RUN uv sync --frozen --no-dev

# Création d'un utilisateur non-root et attribution des droits sur /app
RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app

# On bascule sur cet utilisateur : tout ce qui suit tourne sans privilèges admin
USER appuser

# Port exposé par Streamlit
EXPOSE 8501

# Commande de démarrage : on réutilise notre entrypoint uv
CMD ["uv", "run", "app"]