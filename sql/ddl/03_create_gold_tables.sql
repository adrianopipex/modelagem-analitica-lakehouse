-- =====================================================================
-- Camada GOLD
-- Objetivo: modelo dimensional (esquema estrela) otimizado para
-- consumo analítico e ferramentas de BI.
-- =====================================================================

CREATE SCHEMA IF NOT EXISTS gold;

-- Dimensão Cliente
CREATE TABLE IF NOT EXISTS gold.dim_cliente (
    sk_cliente          BIGINT      GENERATED ALWAYS AS IDENTITY,
    id_cliente          STRING      NOT NULL,
    nome                STRING,
    cidade              STRING,
    estado              STRING,
    faixa_etaria        STRING
) USING DELTA;

-- Dimensão Produto
CREATE TABLE IF NOT EXISTS gold.dim_produto (
    sk_produto          BIGINT      GENERATED ALWAYS AS IDENTITY,
    id_produto          STRING      NOT NULL,
    nome_produto        STRING,
    categoria           STRING,
    preco_unitario      DECIMAL(10,2)
) USING DELTA;

-- Dimensão Tempo
CREATE TABLE IF NOT EXISTS gold.dim_tempo (
    sk_tempo            BIGINT      GENERATED ALWAYS AS IDENTITY,
    data                DATE        NOT NULL,
    ano                 INT,
    mes                 INT,
    trimestre           INT,
    nome_mes            STRING
) USING DELTA;

-- Fato Vendas
CREATE TABLE IF NOT EXISTS gold.fato_vendas (
    sk_venda            BIGINT      GENERATED ALWAYS AS IDENTITY,
    sk_cliente          BIGINT      NOT NULL,
    sk_produto          BIGINT      NOT NULL,
    sk_tempo            BIGINT      NOT NULL,
    quantidade          INT,
    valor_total         DECIMAL(12,2)
) USING DELTA;

-- Exemplo de consulta analítica: faturamento por categoria e mês
-- SELECT t.ano, t.mes, p.categoria, SUM(f.valor_total) AS faturamento
-- FROM gold.fato_vendas f
-- JOIN gold.dim_produto p ON f.sk_produto = p.sk_produto
-- JOIN gold.dim_tempo t ON f.sk_tempo = t.sk_tempo
-- GROUP BY t.ano, t.mes, p.categoria
-- ORDER BY t.ano, t.mes;
