# Modelagem Analítica para Ambiente Lakehouse

## Contexto

Este projeto faz parte do portfólio de estudos e projetos práticos em Engenharia e Analytics de Dados. O objetivo é simular a modelagem analítica de um ambiente **Lakehouse**, unindo a flexibilidade de um Data Lake com a governança e performance de um Data Warehouse, utilizando **Apache Spark**, **SQL** e o **Databricks Unity Catalog** como principais ferramentas de processamento, governança e consulta.

O projeto está em construção e será evoluído incrementalmente com novos modelos, otimizações e exemplos de consumo analítico.

## Objetivo

- Demonstrar a construção de uma arquitetura de dados em camadas (Bronze, Silver e Gold) sobre um Lakehouse.
- Estruturar a governança dos dados no Databricks utilizando Unity Catalog (Catalog, Schemas, Volume e Tabelas).
- Aplicar boas práticas de modelagem dimensional para consumo analítico (ex.: esquemas estrela).
- Utilizar Spark para ingestão e transformação de dados, e SQL para modelagem e consultas analíticas.
- Servir como material de estudo e referência para pipelines de dados analíticos.

## Stack utilizada

- **Apache Spark / PySpark** — processamento distribuído e transformação de dados.
- **SQL** — modelagem analítica, criação de tabelas e consultas.
- **Delta Lake** (formato de tabela, conceitual) — versionamento e confiabilidade das camadas.
- **Databricks Unity Catalog** — governança de Catalog, Schemas, Volumes e Tabelas.

## Estrutura do projeto

```
modelagem-analitica-lakehouse/
├── README.md
├── docs/
│   ├── ARCHITECTURE.md
│   └── architecture_diagram.png
├── sql/
│   └── ddl/
│       ├── 00_setup_unity_catalog.sql
│       ├── 01_create_bronze_tables.sql
│       ├── 02_create_silver_tables.sql
│       └── 03_create_gold_tables.sql
├── src/
│   ├── bronze/
│   │   └── ingest_bronze.py
│   ├── silver/
│   │   └── transform_silver.py
│   └── gold/
│       └── aggregate_gold.py
├── requirements.txt
└── .gitignore
```

## Arquitetura

A visão detalhada da arquitetura (camadas, fluxo de dados, estrutura no Unity Catalog e decisões de modelagem) está documentada em [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), incluindo um diagrama visual da solução.

## Como executar (no Databricks)

Passo 1. Execute `sql/ddl/00_setup_unity_catalog.sql` para criar o Catalog (`lakehouse_catalog`), os Schemas (`bronze`, `silver`, `gold`) e o Volume de landing (`bronze.landing_volume`).

Passo 2. Carregue os arquivos de origem (CSV) no Volume, em `/Volumes/lakehouse_catalog/bronze/landing_volume/`.

Passo 3. Execute os demais scripts DDL (`01`, `02` e `03`) para criar as tabelas das camadas Bronze, Silver e Gold.

Passo 4. Execute os scripts em `src/` na ordem: ingestão (Bronze) → transformação (Silver) → agregação analítica (Gold).

## Status

🚧 Projeto em construção — novos modelos e melhorias serão adicionados progressivamente.

## Autor

Projeto desenvolvido por Adriano como parte do portfólio de projetos em Engenharia de Dados e Analytics.
