-- =====================================================================
-- Camada BRONZE
-- Objetivo: armazenar os dados brutos, exatamente como recebidos da
-- fonte, com colunas de controle de ingestão (metadados de auditoria).
-- =====================================================================

CREATE SCHEMA IF NOT EXISTS bronze;

-- Dados brutos de clientes
CREATE TABLE IF NOT EXISTS bronze.clientes_raw (
    id_cliente          STRING,
    nome                STRING,
    email               STRING,
    data_nascimento     STRING,
    cidade              STRING,
    estado              STRING,
    origem_arquivo      STRING,
    dt_ingestao         TIMESTAMP
) USING DELTA;

-- Dados brutos de produtos
CREATE TABLE IF NOT EXISTS bronze.produtos_raw (
    id_produto          STRING,
    nome_produto        STRING,
    categoria           STRING,
    preco_unitario      STRING,
    origem_arquivo      STRING,
    dt_ingestao         TIMESTAMP
) USING DELTA;

-- Dados brutos de vendas/transações
CREATE TABLE IF NOT EXISTS bronze.vendas_raw (
    id_venda            STRING,
    id_cliente          STRING,
    id_produto          STRING,
    quantidade          STRING,
    valor_total         STRING,
    data_venda          STRING,
    origem_arquivo      STRING,
    dt_ingestao         TIMESTAMP
) USING DELTA;
