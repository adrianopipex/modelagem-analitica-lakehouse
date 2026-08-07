"""
Camada Silver — Limpeza e padronização dos dados.

Este script lê as tabelas da camada Bronze (Unity Catalog), aplica
conversões de tipo, remove duplicados e padroniza os dados, gravando
o resultado nas tabelas da camada Silver.

Pré-requisito: executar sql/ddl/00_setup_unity_catalog.sql
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

CATALOG = "lakehouse_catalog"


def get_spark_session() -> SparkSession:
    return SparkSession.builder.appName("transform_silver").getOrCreate()


def transform_clientes(spark: SparkSession):
    df = spark.table(f"{CATALOG}.bronze.clientes_raw")
    df = (
        df.dropDuplicates(["id_cliente"])
        .withColumn("data_nascimento", F.to_date("data_nascimento"))
        .withColumn("dt_atualizacao", F.current_timestamp())
        .select(
            "id_cliente", "nome", "email", "data_nascimento",
            "cidade", "estado", "dt_atualizacao",
        )
    )
    df.write.format("delta").mode("overwrite").saveAsTable(f"{CATALOG}.silver.clientes")


def transform_produtos(spark: SparkSession):
    df = spark.table(f"{CATALOG}.bronze.produtos_raw")
    df = (
        df.dropDuplicates(["id_produto"])
        .withColumn("preco_unitario", F.col("preco_unitario").cast("decimal(10,2)"))
        .withColumn("dt_atualizacao", F.current_timestamp())
        .select(
            "id_produto", "nome_produto", "categoria",
            "preco_unitario", "dt_atualizacao",
        )
    )
    df.write.format("delta").mode("overwrite").saveAsTable(f"{CATALOG}.silver.produtos")


def transform_vendas(spark: SparkSession):
    df = spark.table(f"{CATALOG}.bronze.vendas_raw")
    df = (
        df.dropDuplicates(["id_venda"])
        .withColumn("quantidade", F.col("quantidade").cast("int"))
        .withColumn("valor_total", F.col("valor_total").cast("decimal(12,2)"))
        .withColumn("data_venda", F.to_date("data_venda"))
        .withColumn("dt_atualizacao", F.current_timestamp())
        .select(
            "id_venda", "id_cliente", "id_produto", "quantidade",
            "valor_total", "data_venda", "dt_atualizacao",
        )
    )
    df.write.format("delta").mode("overwrite").saveAsTable(f"{CATALOG}.silver.vendas")


def main():
    spark = get_spark_session()
    spark.sql(f"USE CATALOG {CATALOG}")
    transform_clientes(spark)
    transform_produtos(spark)
    transform_vendas(spark)
    print("Transformação da camada Silver concluída com sucesso.")


if __name__ == "__main__":
    main()
