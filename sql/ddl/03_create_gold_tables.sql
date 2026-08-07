-- =====================================================================
-- Camada GOLD
-- Objetivo: modelo dimensional (esquema estrela) para análise de
-- preços, avaliações e disponibilidade de livros por categoria e
-- ao longo do tempo.
-- Pré-requisito: executar 00_setup_unity_catalog.sql
-- =====================================================================

USE CATALOG lakehouse_catalog;

-- Dimensão Livro
CREATE TABLE IF NOT EXISTS lakehouse_catalog.gold.dim_livro (
    sk_livro            BIGINT      GENERATED ALWAYS AS IDENTITY,
    id_livro            STRING      NOT NULL,
    titulo              STRING,
    categoria           STRING
) USING DELTA;

-- Dimensão Categoria
CREATE TABLE IF NOT EXISTS lakehouse_catalog.gold.dim_categoria (
    sk_categoria        BIGINT      GENERATED ALWAYS AS IDENTITY,
    categoria           STRING      NOT NULL
) USING DELTA;

-- Dimensão Tempo (data da coleta)
CREATE TABLE IF NOT EXISTS lakehouse_catalog.gold.dim_tempo (
    sk_tempo            BIGINT      GENERATED ALWAYS AS IDENTITY,
    data                DATE        NOT NULL,
    ano                 INT,
    mes                 INT,
    trimestre           INT,
    nome_mes            STRING
) USING DELTA;

-- Fato Preço do Livro (snapshot de preço/rating/disponibilidade por coleta)
CREATE TABLE IF NOT EXISTS lakehouse_catalog.gold.fato_preco_livro (
    sk_fato             BIGINT      GENERATED ALWAYS AS IDENTITY,
    sk_livro            BIGINT      NOT NULL,
    sk_categoria        BIGINT      NOT NULL,
    sk_tempo            BIGINT      NOT NULL,
    preco               DECIMAL(10,2),
    rating              INT,
    disponivel          BOOLEAN
) USING DELTA;

-- Exemplo de consulta analítica: preço médio por categoria e mês
-- SELECT t.ano, t.mes, c.categoria, AVG(f.preco) AS preco_medio
-- FROM lakehouse_catalog.gold.fato_preco_livro f
-- JOIN lakehouse_catalog.gold.dim_categoria c ON f.sk_categoria = c.sk_categoria
-- JOIN lakehouse_catalog.gold.dim_tempo t ON f.sk_tempo = t.sk_tempo
-- GROUP BY t.ano, t.mes, c.categoria
-- ORDER BY t.ano, t.mes;
