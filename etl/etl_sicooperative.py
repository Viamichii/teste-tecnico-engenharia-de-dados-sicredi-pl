# etl/etl_sicooperative.py
"""
Pipeline ETL do desafio Sicredi.

Etapas:
1) Geração de dados fictícios no SQL Server
2) Bronze (SQL Server → Parquet)
3) Silver (Parquet → CSV final)
"""

import os
import sys
from pyspark.sql import SparkSession, functions as F

# -----------------------------------------------------
# Configuração do caminho raiz do projeto
# -----------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import configs                  # noqa: E402
from sql import data_generator  # noqa: E402


# -----------------------------------------------------
# Variáveis principais
# -----------------------------------------------------
TABLES_BRONZE = {
    "associado": "dbo.associado",
    "conta": "dbo.conta",
    "cartao": "dbo.cartao",
    "movimento": "dbo.movimento",
}

BRONZE_PATH = configs.BRONZE_PATH
SILVER_PATH = configs.SILVER_PATH

JDBC_PROPS = {
    "user": configs.DB_USER,
    "password": configs.DB_PASSWORD,
    "driver": configs.JDBC_DRIVER,
}


# -----------------------------------------------------
# Funções auxiliares
# -----------------------------------------------------

def criar_spark() -> SparkSession:
    """Cria a SparkSession única para Bronze + Silver."""
    return (
        SparkSession.builder
        .appName("sicredi-etl")
        .config("spark.jars.packages", configs.JDBC_JAR_PACKAGE)
        .getOrCreate()
    )


def etapa_dados_ficticios() -> None:
    """Etapa 1: geração de massa de dados fictícia no SQL Server."""
    data_generator.main()


def etapa_bronze(spark: SparkSession) -> None:
    """Etapa 2: leitura das tabelas SQL e criação dos Parquets da Bronze."""
    os.makedirs(BRONZE_PATH, exist_ok=True)

    for nome_curto, nome_completo in TABLES_BRONZE.items():
        df = (
            spark.read.jdbc(
                url=configs.JDBC_URL,
                table=nome_completo,
                properties=JDBC_PROPS,
            )
            .withColumn("dt_ingestao", F.current_timestamp())
        )

        destino = os.path.join(BRONZE_PATH, nome_curto)
        (
            df.write
              .mode("overwrite")
              .parquet(destino)
        )


def etapa_silver(spark: SparkSession) -> None:
    """Etapa 3: join da Bronze e geração do CSV final na Silver."""
    bronze = BRONZE_PATH
    silver = SILVER_PATH

    df_associado = (
        spark.read.parquet(os.path.join(bronze, "associado"))
             .withColumnRenamed("id", "id_associado")
    )
    df_conta = (
        spark.read.parquet(os.path.join(bronze, "conta"))
             .withColumnRenamed("id", "id_conta")
    )
    df_cartao = (
        spark.read.parquet(os.path.join(bronze, "cartao"))
             .withColumnRenamed("id", "id_cartao")
    )
    df_movimento = (
        spark.read.parquet(os.path.join(bronze, "movimento"))
             .withColumnRenamed("id", "id_movimento")
    )

    # Join principal unificando associado + conta + cartao + movimento
    df_mov_flat = (
        df_movimento
            .join(df_cartao,    df_movimento.id_cartao == df_cartao.id_cartao,       "inner")
            .join(df_conta,     df_cartao.id_conta     == df_conta.id_conta,         "inner")
            .join(df_associado, df_cartao.id_associado == df_associado.id_associado, "inner")
            .select(
                F.col("nome").alias("nome_associado"),
                F.col("sobrenome").alias("sobrenome_associado"),
                F.col("idade").alias("idade_associado"),
                F.col("vlr_transacao").alias("vlr_transacao_movimento"),
                F.col("des_transacao").alias("des_transacao_movimento"),
                F.col("data_movimento"),
                F.col("num_cartao").alias("numero_cartao"),
                F.col("nom_impresso").alias("nome_impresso_cartao"),
                F.col("tipo").alias("tipo_conta"),
                F.col("data_criacao").alias("data_criacao_conta"),
            )
    )

    # Tipagens finais para exportação
    df_silver = df_mov_flat.select(
        F.col("nome_associado").cast("string"),
        F.col("sobrenome_associado").cast("string"),
        F.col("idade_associado").cast("string"),
        F.col("vlr_transacao_movimento").cast("string"),
        F.col("des_transacao_movimento").cast("string"),
        F.col("data_movimento").cast("string"),
        F.col("numero_cartao").cast("string"),
        F.col("nome_impresso_cartao").cast("string"),
        F.col("tipo_conta").cast("string"),
        F.col("data_criacao_conta").cast("string"),
    )

    os.makedirs(silver, exist_ok=True)

    (
        df_silver
            .coalesce(1)
            .write
            .mode("overwrite")
            .option("header", True)
            .csv(silver)
    )


# -----------------------------------------------------
# Execução principal da Pipeline ETL
# -----------------------------------------------------

def main() -> None:
    """Fluxo principal da pipeline."""
    etapa_dados_ficticios()

    spark = criar_spark()
    try:
        etapa_bronze(spark)
        etapa_silver(spark)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
