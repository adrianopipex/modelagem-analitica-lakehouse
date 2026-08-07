"""
Camada Bronze — Ingestão de dados brutos.

Este script lê os dados de origem a partir do Volume do Unity Catalog
(landing_volume) e grava, sem transformação, nas tabelas da camada
Bronze do Lakehouse, adicionando apenas metadados de auditoria
(arquivo de origem e timestamp de ingestão).

Pré-requisito: executar sql/ddl/00_setup_unity_catalog.sql
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

CATALOG = "lakehouse_catalog"
VOLUME_BASE_PATH = f"/Volumes/{CATALOG}/bronze/landing_volume"

SOURCE_PATH_CLIENTES = f"{VOLUME_BASE_PATH}/clientes/"
SOURCE_PATH_PRODUTOS = f"{VOLUME_BASE_PATH}/produtos/"
SOURCE_PATH_VENDAS = f"{VOLUME_BASE_PATH}/vendas/"


def get_spark_session() -> SparkSession:
    """Cria (ou reutiliza) a sessão Spark."""
    return SparkSession.builder.appName("ingest_bronze").getOrCreate()


def ingest_raw(spark: SparkSession, source_path: str, source_format: str = "csv"):
    """Lê os dados brutos do Volume e adiciona colunas de auditoria."""
    df = (
        spark.read.format(source_format)
        .option("header", "true")
        .option("inferSchema", "true")
        .load(source_path)
    )
    df = df.withColumn("origem_arquivo", F.input_file_name())
    df = df.withColumn("dt_ingestao", F.current_timestamp())
    return df


def main():
    spark = get_spark_session()
    spark.sql(f"USE CATALOG {CATALOG}")

    clientes_df = ingest_raw(spark, SOURCE_PATH_CLIENTES)
    clientes_df.write.format("delta").mode("append").saveAsTable(
        f"{CATALOG}.bronze.clientes_raw"
    )

    produtos_df = ingest_raw(spark, SOURCE_PATH_PRODUTOS)
    produtos_df.write.format("delta").mode("append").saveAsTable(
        f"{CATALOG}.bronze.produtos_raw"
    )

    vendas_df = ingest_raw(spark, SOURCE_PATH_VENDAS)
    vendas_df.write.format("delta").mode("append").saveAsTable(
        f"{CATALOG}.bronze.vendas_raw"
    )

    print("Ingestão da camada Bronze concluída com sucesso.")


if __name__ == "__main__":
    main()
