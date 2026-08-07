"""
Funções utilitárias para a camada Bronze — leitura dos arquivos JSON
brutos gravados no Volume (etapa de scraping) e escrita nas tabelas
Delta da camada Bronze, com metadados de auditoria.

Este módulo contém apenas funções — a execução acontece no notebook
`notebooks/02_ingest_bronze.ipynb`.
"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

CATALOG = "lakehouse_catalog"


def read_raw_json(spark: SparkSession, path: str) -> DataFrame:
    """Lê os arquivos JSON brutos gravados no Volume pela etapa de scraping."""
    return spark.read.option("multiline", "true").json(path)


def add_audit_columns(df: DataFrame, source_path: str) -> DataFrame:
    """Adiciona colunas de auditoria (origem do arquivo e timestamp de ingestão)."""
    return df.withColumn("origem_arquivo", F.lit(source_path)).withColumn(
        "dt_ingestao", F.current_timestamp()
    )


def write_bronze_table(df: DataFrame, table_name: str, mode: str = "append") -> None:
    """Grava o DataFrame na tabela Delta da camada Bronze."""
    df.write.format("delta").mode(mode).saveAsTable(f"{CATALOG}.bronze.{table_name}")
