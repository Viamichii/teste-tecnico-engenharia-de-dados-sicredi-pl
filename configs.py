# configs.py
# Configurações globais do projeto ETL Sicredi

# --- Banco de dados SQL Server ---
DB_SERVER = r"AMICHI\SQLEXPRESS"
DB_NAME = "sicredi"

# Usuário dedicado ao projeto (já criado no SQL Server)
DB_USER = "sicredi_user"
DB_PASSWORD = "SenhaForte123!"  # ajuste se mudou

# --- Conexão JDBC (Spark) ---
JDBC_URL = (
    f"jdbc:sqlserver://{DB_SERVER}:1433;"
    f"databaseName={DB_NAME};"
    "encrypt=false;"
    "trustServerCertificate=true"
)

JDBC_DRIVER = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
JDBC_JAR_PACKAGE = "com.microsoft.sqlserver:mssql-jdbc:12.6.1.jre11"

# --- Conexão ODBC (pyodbc) ---
ODBC_DRIVER = "ODBC Driver 17 for SQL Server"

def build_odbc_conn_str() -> str:
    """
    Monta a connection string ODBC para uso no pyodbc.
    Exemplo produzido:
    DRIVER={ODBC Driver 17 for SQL Server};SERVER=AMICHI\SQLEXPRESS;DATABASE=sicredi;UID=sicredi_user;PWD=...
    """
    return (
        f"DRIVER={{{ODBC_DRIVER}}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
    )

# --- Caminhos de dados ---
BRONZE_PATH = "./data/bronze"
SILVER_PATH = "./data/silver"
