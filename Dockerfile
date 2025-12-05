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

# Repositório Microsoft + driver ODBC 18
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-prod.gpg && \
    curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copia projeto
COPY . .

# Variáveis de ambiente padrão
ENV DB_HOST=sqlserver \
    DB_PORT=1433 \
    DB_NAME=sicredi \
    DB_USER=sicredi_user \
    DB_PASSWORD=SenhaForte123! \
    ODBC_DRIVER="ODBC Driver 18 for SQL Server" \
    PYTHONUNBUFFERED=1

CMD ["python", "etl/etl_sicooperative.py"]
