"""
Funções utilitárias para a camada Gold — construção das dimensões e
da tabela fato do modelo estrela para análise de preços de livros.

Este módulo contém apenas funções — a execução acontece no notebook
`notebooks/04_aggregate_gold.ipynb`.
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

CATALOG = "lakehouse_catalog"


def build_dim_tempo(df: DataFrame, date_column: str = "dt_coleta") -> DataFrame:
    """Constrói a dimensão tempo a partir das datas de coleta distintas."""
    return (
        df.select(date_column)
        .distinct()
        .withColumnRenamed(date_column, "data")
        .withColumn("ano", F.year("data"))
        .withColumn("mes", F.month("data"))
        .withColumn("trimestre", F.quarter("data"))
        .withColumn("nome_mes", F.date_format("data", "MMMM"))
    )


def build_dim_livro(df: DataFrame) -> DataFrame:
    """Constrói a dimensão livro (um registro por id_livro)."""
    return df.select("id_livro", "titulo", "categoria").dropDuplicates(["id_livro"])


def build_dim_categoria(df: DataFrame) -> DataFrame:
    """Constrói a dimensão categoria."""
    return df.select("categoria").distinct()


def build_fato_preco_livro(
    silver_df: DataFrame,
    dim_livro: DataFrame,
    dim_categoria: DataFrame,
    dim_tempo: DataFrame,
) -> DataFrame:
    """Junta a Silver com as dimensões para montar a tabela fato."""
    categoria_dim = dim_categoria.withColumnRenamed("categoria", "categoria_dim")

    return (
        silver_df.join(dim_livro.select("id_livro"), "id_livro")
        .join(categoria_dim, silver_df["categoria"] == categoria_dim["categoria_dim"])
        .join(dim_tempo, silver_df["dt_coleta"] == dim_tempo["data"])
        .select("id_livro", "categoria", "data", "preco", "rating", "disponivel")
    )
