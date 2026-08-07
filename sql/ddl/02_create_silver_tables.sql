-- =====================================================================
-- Camada SILVER
-- Objetivo: dados limpos, com tipos corretos, deduplicados e
-- padronizados, prontos para serem combinados/agregados na camada Gold.
-- Pré-requisito: executar 00_setup_unity_catalog.sql
-- =====================================================================

USE CATALOG lakehouse_catalog;

-- Clientes padronizados e deduplicados
CREATE TABLE IF NOT EXISTS lakehouse_catalog.silver.clientes (
    id_cliente          STRING      NOT NULL,
    nome                STRING,
    email               STRING,
    data_nascimento     DATE,
    cidade              STRING,
    estado              STRING,
    dt_atualizacao      TIMESTAMP
) USING DELTA;

-- Produtos padronizados
CREATE TABLE IF NOT EXISTS lakehouse_catalog.silver.produtos (
    id_produto          STRING      NOT NULL,
    nome_produto        STRING,
    categoria           STRING,
    preco_unitario      DECIMAL(10,2),
    dt_atualizacao      TIMESTAMP
) USING DELTA;

-- Vendas padronizadas, com tipos corrigidos e chaves validadas
CREATE TABLE IF NOT EXISTS lakehouse_catalog.silver.vendas (
    id_venda            STRING      NOT NULL,
    id_cliente          STRING      NOT NULL,
    id_produto          STRING      NOT NULL,
    quantidade          INT,
    valor_total         DECIMAL(12,2),
    data_venda          DATE,
    dt_atualizacao      TIMESTAMP
) USING DELTA;
