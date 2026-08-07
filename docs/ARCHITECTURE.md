# Arquitetura — Modelagem Analítica para Ambiente Lakehouse

## Visão Geral

Este projeto adota a **arquitetura medalhão (Medallion Architecture)**, um padrão amplamente utilizado em ambientes Lakehouse para organizar dados em camadas progressivas de qualidade e granularidade: **Bronze**, **Silver** e **Gold**.

```
 Fontes de Dados         Bronze              Silver               Gold
 (arquivos, APIs,     (dados brutos)     (dados limpos e     (dados agregados
  bancos de dados)    ingestão 1:1       padronizados)        para consumo
                       da origem                               analítico/BI)

     [Fonte] ───────▶ [bronze.*] ─────▶ [silver.*] ─────▶ [gold.*]
```

## Diagrama da Arquitetura

![Arquitetura Lakehouse — Databricks Unity Catalog](architecture_diagram.png)

## Camada Bronze

- Recebe os dados brutos, sem transformação, exatamente como vieram da fonte (arquivos CSV/JSON/Parquet, APIs, bancos relacionais).
- Mantém histórico completo (append-only) para rastreabilidade e auditoria.
- Serve como camada de recuperação em caso de erro nas camadas seguintes.
- Implementada nos scripts em `src/bronze/` e nas definições em `sql/ddl/01_create_bronze_tables.sql`.

## Camada Silver

- Aplica limpeza, padronização de tipos e nomes de colunas, deduplicação e regras básicas de qualidade de dados.
- Realiza junções (joins) entre diferentes fontes quando necessário para formar entidades de negócio coerentes.
- Representa uma visão "confiável" dos dados, ainda em granularidade próxima à operacional.
- Implementada em `src/silver/` e `sql/ddl/02_create_silver_tables.sql`.

## Camada Gold

- Contém dados modelados para consumo analítico: tabelas fato e dimensão (modelagem dimensional / esquema estrela), métricas agregadas e KPIs.
- Otimizada para performance de leitura em ferramentas de BI e consultas analíticas.
- Implementada em `src/gold/` e `sql/ddl/03_create_gold_tables.sql`.

## Modelagem Dimensional (Camada Gold)

A camada Gold segue os princípios de modelagem dimensional:

- **Tabelas Fato**: armazenam métricas e eventos de negócio (ex.: vendas, transações), com granularidade bem definida.
- **Tabelas Dimensão**: descrevem o contexto das métricas (ex.: cliente, produto, tempo, região), permitindo análises multidimensionais (drill-down, slice-and-dice).

## Implementação no Databricks (Unity Catalog)

O projeto foi desenhado para ser implantado em um workspace Databricks, utilizando o **Unity Catalog** para governança dos dados. A hierarquia de objetos segue o padrão:

```
Catalog (lakehouse_catalog)
 ├── Volume (armazenamento de arquivos)
 │    └── bronze.landing_volume  →  /Volumes/lakehouse_catalog/bronze/landing_volume/
 │
 ├── Schema bronze
 │    ├── clientes_raw
 │    ├── produtos_raw
 │    └── vendas_raw
 │
 ├── Schema silver
 │    ├── clientes
 │    ├── produtos
 │    └── vendas
 │
 └── Schema gold
      ├── dim_cliente
      ├── dim_produto
      ├── dim_tempo
      └── fato_vendas
```

Etapas de configuração (ver `sql/ddl/00_setup_unity_catalog.sql`):

- **Catalog**: `lakehouse_catalog` é o catálogo raiz do projeto, isolando seus dados de outros projetos no mesmo workspace.
- **Schemas**: um schema por camada (`bronze`, `silver`, `gold`), permitindo aplicar permissões e organização independentes por camada.
- **Volume**: `lakehouse_catalog.bronze.landing_volume` é utilizado para armazenar os arquivos brutos (CSV/JSON/Parquet) recebidos das fontes de dados antes de serem lidos e gravados como tabelas Delta na camada Bronze.
- **Tabelas**: criadas dentro de cada schema, sempre referenciadas pelo nome completo `catalog.schema.tabela` (ex.: `lakehouse_catalog.gold.fato_vendas`), conforme as boas práticas de governança do Unity Catalog.

## Ferramentas

- **Apache Spark / PySpark**: motor de processamento distribuído utilizado para ingestão (Bronze) e transformação (Silver/Gold).
- **SQL**: utilizado para definição de esquemas (DDL) e para consultas analíticas sobre as camadas.
- **Delta Lake** (conceitual): formato de tabela que traz confiabilidade transacional (ACID), versionamento e time travel ao Lakehouse.
- **Databricks Unity Catalog**: governança centralizada de Catalogs, Schemas, Volumes e Tabelas.

## Fluxo de Execução

1. **Setup (Unity Catalog)**: `sql/ddl/00_setup_unity_catalog.sql` cria o Catalog, os Schemas e o Volume de landing.
2. **Ingestão (Bronze)**: `src/bronze/ingest_bronze.py` lê os arquivos do Volume e grava na camada Bronze sem transformação.
3. **Transformação (Silver)**: `src/silver/transform_silver.py` lê a camada Bronze, aplica limpeza e padronização, e grava na camada Silver.
4. **Agregação Analítica (Gold)**: `src/gold/aggregate_gold.py` lê a camada Silver, aplica modelagem dimensional e agregações, e grava na camada Gold, pronta para consumo.

## Próximos Passos

- Adicionar exemplos de dados de entrada (dataset de amostra).
- Incluir testes automatizados de qualidade de dados.
- Explorar otimizações de performance (particionamento, Z-Ordering, cache).
