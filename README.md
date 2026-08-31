# Modelagem Analítica para Ambiente Lakehouse

## Contexto

Este projeto faz parte do portfólio de estudos e projetos práticos em Engenharia e Analytics de Dados. Ele simula, de ponta a ponta, um pipeline de dados sobre um ambiente **Lakehouse**: extração de dados via **web scraping**, armazenamento em um **Volume** do Databricks, e processamento em camadas (**Bronze → Silver → Gold**) utilizando **PySpark**, **SQL** e o **Databricks Unity Catalog**.

Como estudo de caso, os dados são coletados do site público [books.toscrape.com](https://books.toscrape.com/) — criado especificamente para prática de web scraping — simulando um cenário real de ingestão de dados externos.

## Objetivo

- Demonstrar a extração de dados de uma fonte externa (scraping) e seu armazenamento em um Volume do Unity Catalog.
- Construir uma arquitetura de dados em camadas (Bronze, Silver e Gold) sobre um Lakehouse.
- Estruturar a governança dos dados no Databricks (Catalog, Schemas, Volume e Tabelas).
- Aplicar boas práticas de modelagem dimensional para consumo analítico (esquema estrela).
- Separar claramente **funções reutilizáveis** (`.py`) de **notebooks de execução/transformação** (`.ipynb`), como em um projeto real no Databricks.

## Stack utilizada

- **Apache Spark / PySpark** — processamento distribuído e transformação de dados.
- **Requests / BeautifulSoup** — extração (scraping) dos dados de origem.
- **SQL** — modelagem analítica, criação de tabelas e consultas.
- **Delta Lake** (formato de tabela, conceitual) — versionamento e confiabilidade das camadas.
- **Databricks Unity Catalog** — governança de Catalog, Schemas, Volumes e Tabelas.
- **Jupyter / Databricks Notebooks** — orquestração das transformações.

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
│   └── common/                  # apenas funções reutilizáveis (.py)
│       ├── spark_utils.py
│       ├── scraping_utils.py
│       ├── bronze_utils.py
│       ├── silver_utils.py
│       └── gold_utils.py
├── notebooks/                   # notebooks Databricks (.ipynb) — execução do pipeline
│   ├── 01_scrape_to_volume.ipynb
│   ├── 02_ingest_bronze.ipynb
│   ├── 03_transform_silver.ipynb
│   └── 04_aggregate_gold.ipynb
├── requirements.txt
└── .gitignore
```

## Arquitetura

A visão detalhada da arquitetura (scraping, camadas, Unity Catalog e modelagem dimensional) está documentada em [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), incluindo um diagrama visual do pipeline completo.

## Como executar (no Databricks)

Passo 1. Execute `sql/ddl/00_setup_unity_catalog.sql` para criar o Catalog (`lakehouse_catalog`), os Schemas (`bronze`, `silver`, `gold`) e o Volume de landing.

Passo 2. Execute os demais scripts DDL (`01`, `02` e `03`) para criar as tabelas de cada camada.

Passo 3. Execute os notebooks em `notebooks/`, na ordem: `01_scrape_to_volume` → `02_ingest_bronze` → `03_transform_silver` → `04_aggregate_gold`.

Os notebooks importam as funções definidas em `src/common/` — nenhuma lógica de transformação vive fora dos módulos `.py` ou dos notebooks.

## Status

✅ **Concluído** — pipeline completo, do scraping à camada Gold, com governança via Unity Catalog. Próximas evoluções podem incluir agendamento via Databricks Workflows e testes automatizados de qualidade de dados.

## Autor

Projeto desenvolvido por Adriano Costa como parte do portfólio de projetos em Engenharia de Dados e Analytics.
