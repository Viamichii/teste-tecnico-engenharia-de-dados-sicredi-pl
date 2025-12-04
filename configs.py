# configs.py
# Configurações globais do projeto ETL Sicredi

import os

# --- Banco de dados SQL Server ---

# Para ODBC (pyodbc) – já estava funcionando assim:
DB_SERVER_ODBC = r"AMICHI\SQLEXPRESS"

DB_NAME = "sicredi"

DB_USER = "sicredi_user"
DB_PASSWORD = "SenhaForte123!"


# --- Conexão JDBC (Spark) ---
# Usando localhost + porta 1433, que você já testou e FUNCIONA
JDBC_HOST = "localhost"
JDBC_PORT = 1433

JDBC_URL = (
    f"jdbc:sqlserver://{JDBC_HOST}:{JDBC_PORT};"
    f"databaseName={DB_NAME};"
    "encrypt=false;"
    "trustServerCertificate=true;"
)

JDBC_DRIVER = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
JDBC_JAR_PACKAGE = "com.microsoft.sqlserver:mssql-jdbc:12.6.1.jre11"

# (se quiser manter o caminho local do JAR só pra debug, pode:
# JDBC_JAR_PATH = r"C:\Drivers\mssql-jdbc-13.2.1.jre11.jar"
# mas eu não usaria isso no código principal)


# --- Conexão ODBC (pyodbc) ---
ODBC_DRIVER = "ODBC Driver 17 for SQL Server"

def build_odbc_conn_str() -> str:
    """
    Monta a connection string ODBC para o pyodbc (usada no data_generator).
    """
    return (
        f"DRIVER={{{ODBC_DRIVER}}};"
        f"SERVER={DB_SERVER_ODBC};"
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
