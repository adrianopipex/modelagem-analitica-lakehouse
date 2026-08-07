-- =====================================================================
-- Camada SILVER
-- Objetivo: dados de livros limpos, com tipos corretos, deduplicados
-- e padronizados, prontos para a modelagem analítica da camada Gold.
-- Pré-requisito: executar 00_setup_unity_catalog.sql
-- =====================================================================

USE CATALOG lakehouse_catalog;

CREATE TABLE IF NOT EXISTS lakehouse_catalog.silver.livros (
    id_livro            STRING       NOT NULL,   -- hash(titulo + categoria)
    titulo              STRING,
    categoria           STRING,
    preco               DECIMAL(10,2),
    rating              INT,
    disponivel          BOOLEAN,
    dt_coleta           DATE,
    dt_atualizacao      TIMESTAMP
) USING DELTA;
