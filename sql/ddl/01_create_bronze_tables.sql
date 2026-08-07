-- =====================================================================
-- Camada BRONZE
-- Objetivo: armazenar os dados brutos extraídos via scraping,
-- exatamente como coletados da fonte, com colunas de auditoria.
-- Fonte: https://books.toscrape.com (site público para prática de scraping)
-- Pré-requisito: executar 00_setup_unity_catalog.sql
-- =====================================================================

USE CATALOG lakehouse_catalog;

-- Dados brutos de livros, coletados via scraping
-- (ver notebooks/01_scrape_to_volume.ipynb)
CREATE TABLE IF NOT EXISTS lakehouse_catalog.bronze.livros_raw (
    titulo                STRING,
    preco_raw             STRING,
    rating_raw            STRING,
    disponibilidade_raw   STRING,
    categoria             STRING,
    url_produto           STRING,
    dt_coleta             STRING,
    origem_arquivo        STRING,
    dt_ingestao           TIMESTAMP
) USING DELTA;
