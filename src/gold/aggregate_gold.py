"""
Camada Gold — Modelagem dimensional e agregação analítica.

Este script lê as tabelas da camada Silver (Unity Catalog), constrói
as dimensões e a tabela fato (modelo estrela) e grava o resultado nas
tabelas da camada Gold, prontas para consumo analítico/BI.

Pré-requisito: executar sql/ddl/00_setup_unity_catalog.sql
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

CATALOG = "lakehouse_catalog"


def get_spark_session() -> SparkSession:
    return SparkSession.builder.appName("aggregate_gold").getOrCreate()


def build_dim_cliente(spark: SparkSession):
    df = spark.table(f"{CATALOG}.silver.clientes")
    df = df.withColumn(
        "faixa_etaria",
        F.when(F.floor(F.datediff(F.current_date(), F.col("data_nascimento")) / 365) < 25, "até 24")
        .when(F.floor(F.datediff(F.current_date(), F.col("data_nascimento")) / 365) < 40, "25-39")
        .otherwise("40+"),
    ).select("id_cliente", "nome", "cidade", "estado", "faixa_etaria")
    df.write.format("delta").mode("overwrite").saveAsTable(f"{CATALOG}.gold.dim_cliente")


def build_dim_produto(spark: SparkSession):
    df = spark.table(f"{CATALOG}.silver.produtos").select(
        "id_produto", "nome_produto", "categoria", "preco_unitario"
    )
    df.write.format("delta").mode("overwrite").saveAsTable(f"{CATALOG}.gold.dim_produto")


def build_dim_tempo(spark: SparkSession):
    df = (
        spark.table(f"{CATALOG}.silver.vendas")
        .select("data_venda")
        .distinct()
        .withColumnRenamed("data_venda", "data")
        .withColumn("ano", F.year("data"))
        .withColumn("mes", F.month("data"))
        .withColumn("trimestre", F.quarter("data"))
        .withColumn("nome_mes", F.date_format("data", "MMMM"))
    )
    df.write.format("delta").mode("overwrite").saveAsTable(f"{CATALOG}.gold.dim_tempo")


def build_fato_vendas(spark: SparkSession):
    vendas = spark.table(f"{CATALOG}.silver.vendas")
    dim_cliente = spark.table(f"{CATALOG}.gold.dim_cliente").select("id_cliente")
    dim_produto = spark.table(f"{CATALOG}.gold.dim_produto").select("id_produto")
    dim_tempo = spark.table(f"{CATALOG}.gold.dim_tempo").select(F.col("data").alias("data_venda"))

    fato = (
        vendas.join(dim_cliente, "id_cliente")
        .join(dim_produto, "id_produto")
        .join(dim_tempo, "data_venda")
        .select("id_cliente", "id_produto", "data_venda", "quantidade", "valor_total")
    )
    fato.write.format("delta").mode("overwrite").saveAsTable(f"{CATALOG}.gold.fato_vendas")


def main():
    spark = get_spark_session()
    spark.sql(f"USE CATALOG {CATALOG}")
    build_dim_cliente(spark)
    build_dim_produto(spark)
    build_dim_tempo(spark)
    build_fato_vendas(spark)
    print("Agregação da camada Gold concluída com sucesso.")


if __name__ == "__main__":
    main()
