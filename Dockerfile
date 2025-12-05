FROM python:3.11-slim

# 1) Pastas básicas
WORKDIR /app

# 2) Instalar dependências do sistema (Java + ODBC + build)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-17-jdk-headless \
        unixodbc-dev \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3) Copiar arquivos do projeto
COPY . .

# 4) Instalar dependências Python
RUN pip install --no-cache-dir \
    pyspark \
    pyodbc \
    Faker \
    pandas

# 5) Variáveis padrão (podem ser sobrescritas no docker-compose)
ENV DB_HOST=sqlserver \
    DB_PORT=1433 \
    DB_NAME=sicredi \
    DB_USER=sicredi_user \
    DB_PASSWORD=SenhaForte123!

# 6) Comando padrão: rodar ETL completa
CMD ["python", "-m", "etl.etl_sicooperative"]
