# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# Dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        default-jre-headless \
        curl \
        gnupg2 \
        unixodbc \
        unixodbc-dev \
        build-essential && \
    rm -rf /var/lib/apt/lists/*

# Adicionar repositório Microsoft e instalar msodbcsql18
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-prod.gpg && \
    curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*

# Copia apenas requirements para aproveitar cache do Docker
COPY requirements.txt /tmp/requirements.txt

# Instala dependências Python com cache de pip (BuildKit)
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir --prefer-binary -r /tmp/requirements.txt

# Copia o resto do projeto
COPY . .

ENV DB_HOST=sqlserver \
    DB_PORT=1433 \
    DB_NAME=sicredi \
    DB_USER=sicredi_user \
    DB_PASSWORD=SenhaForte123! \
    PYTHONUNBUFFERED=1

CMD ["python", "etl/etl_sicooperative.py"]