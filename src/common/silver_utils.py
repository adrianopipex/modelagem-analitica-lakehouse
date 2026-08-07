"""
Funções utilitárias para a camada Silver — limpeza, tipagem e
deduplicação dos dados de livros provenientes da camada Bronze.

Este módulo contém apenas funções — a execução acontece no notebook
`notebooks/03_transform_silver.ipynb`.
"""

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F

CATALOG = "lakehouse_catalog"

RATING_MAPPING = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def clean_preco(df: DataFrame, column: str = "preco_raw") -> DataFrame:
    """Converte um preço no formato '£51.77' para DECIMAL(10,2)."""
    return df.withColumn(
        "preco", F.regexp_replace(F.col(column), "[^0-9.]", "").cast("decimal(10,2)")
    )


def clean_rating(df: DataFrame, column: str = "rating_raw") -> DataFrame:
    """Converte o rating textual ('Three') para inteiro (3)."""
    mapping_expr = F.create_map(
        [F.lit(x) for pair in RATING_MAPPING.items() for x in pair]
    )
    return df.withColumn("rating", mapping_expr[F.col(column)])


def clean_disponibilidade(df: DataFrame, column: str = "disponibilidade_raw") -> DataFrame:
    """Converte o texto de disponibilidade em booleano."""
    return df.withColumn("disponivel", F.col(column).contains("In stock"))


def build_id_livro(df: DataFrame) -> DataFrame:
    """Gera um identificador estável para o livro a partir de título e categoria."""
    return df.withColumn(
        "id_livro", F.sha2(F.concat_ws("|", F.col("titulo"), F.col("categoria")), 256)
    )


def deduplicate_latest(df: DataFrame, key_cols, order_col: str) -> DataFrame:
    """Remove duplicados, mantendo o registro mais recente por chave."""
    window = Window.partitionBy(*key_cols).orderBy(F.col(order_col).desc())
    return (
        df.withColumn("_rn", F.row_number().over(window))
        .filter(F.col("_rn") == 1)
        .drop("_rn")
    )
