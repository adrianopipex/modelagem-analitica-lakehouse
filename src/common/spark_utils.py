"""
Funções utilitárias para criação e configuração da SparkSession e
para montagem de caminhos dentro do Volume do Unity Catalog.

Este módulo contém apenas funções reutilizáveis — a execução do
pipeline acontece nos notebooks em `notebooks/`.
"""

from pyspark.sql import SparkSession

CATALOG = "lakehouse_catalog"
VOLUME_BASE_PATH = f"/Volumes/{CATALOG}/bronze/landing_volume"


def get_spark_session(app_name: str = "modelagem-analitica-lakehouse") -> SparkSession:
    """Cria (ou reutiliza) a SparkSession e define o catalog padrão."""
    spark = SparkSession.builder.appName(app_name).getOrCreate()
    spark.sql(f"USE CATALOG {CATALOG}")
    return spark


def volume_path(*parts: str) -> str:
    """Monta um caminho dentro do Volume de landing a partir de subpastas.

    Exemplo: volume_path("livros") -> "/Volumes/lakehouse_catalog/bronze/landing_volume/livros"
    """
    return "/".join([VOLUME_BASE_PATH, *parts])
