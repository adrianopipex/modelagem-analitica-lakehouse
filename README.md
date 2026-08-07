# Modelagem Analítica para Ambiente Lakehouse

## Contexto

Este projeto faz parte do portfólio de estudos e projetos práticos em Engenharia e Analytics de Dados. O objetivo é simular a modelagem analítica de um ambiente **Lakehouse**, unindo a flexibilidade de um Data Lake com a governança e performance de um Data Warehouse, utilizando **Apache Spark** e **SQL** como principais ferramentas de processamento e consulta.

O projeto está em construção e será evoluído incrementalmente com novos modelos, otimizações e exemplos de consumo analítico.

## Objetivo

- Demonstrar a construção de uma arquitetura de dados em camadas (Bronze, Silver e Gold) sobre um Lakehouse.
- Aplicar boas práticas de modelagem dimensional para consumo analítico (ex.: esquemas estrela).
- Utilizar Spark para ingestão e transformação de dados, e SQL para modelagem e consultas analíticas.
- Servir como material de estudo e referência para pipelines de dados analíticos.

## Stack utilizada

- **Apache Spark / PySpark** — processamento distribuído e transformação de dados.
- **SQL** — modelagem analítica, criação de tabelas e consultas.
- **Delta Lake** (formato de tabela, conceitual) — versionamento e confiabilidade das camadas.

## Estrutura do projeto

```
modelagem-analitica-lakehouse/
├── README.md
├── docs/
│   └── ARCHITECTURE.md
├── sql/
│   └── ddl/
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

A visão detalhada da arquitetura (camadas, fluxo de dados e decisões de modelagem) está documentada em [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Como executar

Passo 1. Crie um ambiente virtual Python e instale as dependências listadas em `requirements.txt`.

Passo 2. Execute os scripts DDL em `sql/ddl/` no seu ambiente Spark/SQL para criar as tabelas das camadas Bronze, Silver e Gold.

Passo 3. Execute os scripts em `src/` na ordem: ingestão (Bronze) → transformação (Silver) → agregação analítica (Gold).

## Status

🚧 Projeto em construção — novos modelos e melhorias serão adicionados progressivamente.

## Autor

Projeto desenvolvido por Adriano como parte do portfólio de projetos em Engenharia de Dados e Analytics.
