# configs.py
# Configurações globais do projeto ETL Sicredi

import os

# --- Banco de dados SQL Server ---

# Fora do Docker: DB_HOST = "localhost"
# Dentro do container: DB_HOST = "host.docker.internal" (ou nome do serviço do compose)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "1433"))

DB_NAME = os.getenv("DB_NAME", "sicredi")

DB_USER = os.getenv("DB_USER", "sicredi_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "SenhaForte123!")

# --- Conexão JDBC (Spark) ---
JDBC_URL = (
    f"jdbc:sqlserver://{DB_HOST}:{DB_PORT};"
    f"databaseName={DB_NAME};"
    "encrypt=false;"
    "trustServerCertificate=true;"
)

JDBC_DRIVER = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
JDBC_JAR_PACKAGE = "com.microsoft.sqlserver:mssql-jdbc:12.6.1.jre11"

# --- Conexão ODBC (pyodbc) ---
ODBC_DRIVER = "ODBC Driver 17 for SQL Server"

def build_odbc_conn_str() -> str:
    """
    Monta a connection string ODBC para o pyodbc (usada no data_generator).
    Ex.: SERVER=localhost,1433 ou SERVER=host.docker.internal,1433
    """
    return (
        f"DRIVER={{{ODBC_DRIVER}}};"
        f"SERVER={DB_HOST},{DB_PORT};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
    )

# --- Caminhos de dados ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BRONZE_PATH = os.path.join(PROJECT_ROOT, "data", "bronze")
SILVER_PATH = os.path.join(PROJECT_ROOT, "data", "silver")

os.makedirs(BRONZE_PATH, exist_ok=True)
os.makedirs(SILVER_PATH, exist_ok=True)
