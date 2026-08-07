-- =====================================================================
-- Setup Unity Catalog (Databricks)
-- Objetivo: criar a estrutura de governança de dados no Databricks —
-- Catalog -> Schemas (bronze, silver, gold) -> Volume (dados brutos).
-- Este script deve ser executado ANTES dos demais scripts DDL.
-- =====================================================================

-- 1. Catalog
CREATE CATALOG IF NOT EXISTS lakehouse_catalog
COMMENT 'Catalog do projeto de Modelagem Analítica para Ambiente Lakehouse';

USE CATALOG lakehouse_catalog;

-- 2. Schemas — um por camada da arquitetura medalhão
CREATE SCHEMA IF NOT EXISTS lakehouse_catalog.bronze
COMMENT 'Camada Bronze: dados brutos, sem transformação';

CREATE SCHEMA IF NOT EXISTS lakehouse_catalog.silver
COMMENT 'Camada Silver: dados limpos e padronizados';

CREATE SCHEMA IF NOT EXISTS lakehouse_catalog.gold
COMMENT 'Camada Gold: modelo dimensional para consumo analítico';

-- 3. Volume — armazenamento dos arquivos brutos de origem (antes da ingestão)
CREATE VOLUME IF NOT EXISTS lakehouse_catalog.bronze.landing_volume
COMMENT 'Volume para armazenar os arquivos brutos (CSV/JSON/Parquet) recebidos das fontes, antes da ingestão na camada Bronze';

-- Estrutura de pastas esperada dentro do Volume:
--   /Volumes/lakehouse_catalog/bronze/landing_volume/clientes/
--   /Volumes/lakehouse_catalog/bronze/landing_volume/produtos/
--   /Volumes/lakehouse_catalog/bronze/landing_volume/vendas/

-- 4. Tabelas
-- As tabelas de cada camada são criadas nos scripts seguintes:
--   01_create_bronze_tables.sql
--   02_create_silver_tables.sql
--   03_create_gold_tables.sql
-- Todas utilizam o nome completo no padrão Unity Catalog:
--   catalog.schema.tabela  (ex.: lakehouse_catalog.bronze.clientes_raw)
