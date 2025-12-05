import pyodbc
import time
import os

def init_database():
    # Conectar como SA primeiro (admin)
    sa_password = os.getenv("SA_PASSWORD", "YourStrong@Passw0rd")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "1433")
    
    # Aguardar SQL Server ficar pronto
    for attempt in range(30):
        try:
            conn_str = (
                f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                f"SERVER={db_host},{db_port};"
                f"UID=sa;"
                f"PWD={sa_password};"
                f"Encrypt=yes;"
                f"TrustServerCertificate=yes;"
            )
            conn = pyodbc.connect(conn_str)
            print("Conectado ao SQL Server!")
            break
        except Exception as e:
            print(f"Tentativa {attempt + 1}/30 - Aguardando SQL Server... {str(e)[:50]}")
            time.sleep(2)
    else:
        print("Falha ao conectar ao SQL Server após 30 tentativas")
        return False
    
    cursor = conn.cursor()
    
    # Criar banco de dados
    try:
        cursor.execute("CREATE DATABASE sicredi")
        print("Database 'sicredi' criado")
    except:
        print("Database 'sicredi' já existe")
    
    cursor.close()
    conn.close()
    
    # Conectar ao banco sicredi
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={db_host},{db_port};"
        f"DATABASE=sicredi;"
        f"UID=sa;"
        f"PWD={sa_password};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=yes;"
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # Criar login
    try:
        cursor.execute("CREATE LOGIN sicredi_user WITH PASSWORD = 'SenhaForte123!'")
        print("Login 'sicredi_user' criado")
    except:
        print("Login 'sicredi_user' já existe")
    
    # Criar usuário no banco
    try:
        cursor.execute("CREATE USER sicredi_user FOR LOGIN sicredi_user")
        print("Usuário 'sicredi_user' criado")
    except:
        print("Usuário 'sicredi_user' já existe")
    
    # Dar permissões
    try:
        cursor.execute("ALTER ROLE db_owner ADD MEMBER sicredi_user")
        print("Permissões concedidas")
    except:
        print("Permissões já existem")
    
    # Criar tabelas
    cursor.execute("""
    IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'associado')
    CREATE TABLE associado (
        id          INT IDENTITY(1,1) PRIMARY KEY,
        nome        VARCHAR(100),
        sobrenome   VARCHAR(100),
        idade       INT,
        email       VARCHAR(255)
    )
    """)
    
    cursor.execute("""
    IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'conta')
    CREATE TABLE conta (
        id            INT IDENTITY(1,1) PRIMARY KEY,
        tipo          VARCHAR(20),
        data_criacao  DATETIME2,
        id_associado  INT,
        FOREIGN KEY (id_associado) REFERENCES associado(id)
    )
    """)
    
    cursor.execute("""
    IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'cartao')
    CREATE TABLE cartao (
        id            INT IDENTITY(1,1) PRIMARY KEY,
        num_cartao    BIGINT,
        nom_impresso  VARCHAR(100),
        id_conta      INT,
        id_associado  INT,
        FOREIGN KEY (id_conta) REFERENCES conta(id),
        FOREIGN KEY (id_associado) REFERENCES associado(id)
    )
    """)
    
    cursor.execute("""
    IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'movimento')
    CREATE TABLE movimento (
        id              INT IDENTITY(1,1) PRIMARY KEY,
        vlr_transacao   DECIMAL(10,2),
        des_transacao   VARCHAR(255),
        data_movimento  DATETIME2,
        id_cartao       INT,
        FOREIGN KEY (id_cartao) REFERENCES cartao(id)
    )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Database inicializado com sucesso!")
    return True

if __name__ == "__main__":
    init_database()