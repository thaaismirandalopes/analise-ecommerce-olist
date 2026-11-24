-- Segmentação RFM dos clientes da Olist.
--
-- R (recência):   há quantos dias o cliente fez a última compra
-- F (frequência): quantos pedidos o cliente fez
-- V (valor):      quanto o cliente gastou em produtos
--
-- O resultado é a tabela clientes_rfm, com uma linha por cliente.

DROP TABLE IF EXISTS clientes_rfm;

CREATE TABLE clientes_rfm AS

-- Passo 1: pedidos entregues, já com a identificação real do cliente.
-- O customer_id muda a cada pedido. Quem identifica a pessoa é o customer_unique_id.
WITH pedidos_entregues AS (
    SELECT
        c.customer_unique_id,
        o.order_id,
        o.order_purchase_timestamp
    FROM orders AS o
    INNER JOIN customers AS c
        ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
),

-- Passo 2: valor de cada pedido (soma dos itens, sem frete).
valor_por_pedido AS (
    SELECT
        order_id,
        SUM(price) AS valor
    FROM order_items
    GROUP BY order_id
),

-- Passo 3: o "hoje" da análise é o dia seguinte ao último pedido da base.
data_referencia AS (
    SELECT MAX(order_purchase_timestamp)::date + 1 AS dia
    FROM pedidos_entregues
),

-- Passo 4: os três números de cada cliente.
base_rfm AS (
    SELECT
        p.customer_unique_id,
        (SELECT dia FROM data_referencia) - MAX(p.order_purchase_timestamp)::date AS recencia_dias,
        COUNT(*)     AS frequencia,
        SUM(v.valor) AS valor_total
    FROM pedidos_entregues AS p
    INNER JOIN valor_por_pedido AS v
        ON v.order_id = p.order_id
    GROUP BY p.customer_unique_id
),

-- Passo 5: notas de 1 a 5.
-- R e V: NTILE(5) divide os clientes em 5 grupos do mesmo tamanho.
-- F: regra fixa, porque 97% dos clientes têm 1 pedido só.
--    Com NTILE, clientes iguais cairiam em notas diferentes por sorteio.
notas AS (
    SELECT
        customer_unique_id,
        recencia_dias,
        frequencia,
        valor_total,
        NTILE(5) OVER (ORDER BY recencia_dias DESC, customer_unique_id) AS nota_r,
        CASE
            WHEN frequencia = 1 THEN 1
            WHEN frequencia = 2 THEN 3
            ELSE 5
        END AS nota_f,
        NTILE(5) OVER (ORDER BY valor_total, customer_unique_id) AS nota_v
    FROM base_rfm
)

-- Passo 6: o nome do segmento. O CASE para na primeira regra que for verdadeira.
SELECT
    customer_unique_id,
    recencia_dias,
    frequencia,
    valor_total,
    nota_r,
    nota_f,
    nota_v,
    CASE
        WHEN nota_f >= 3 AND nota_r >= 4 THEN 'Campeões'
        WHEN nota_f >= 3                 THEN 'Recorrentes inativos'
        WHEN nota_r >= 4 AND nota_v >= 4 THEN 'Recentes de alto valor'
        WHEN nota_r >= 4                 THEN 'Recentes'
        WHEN nota_r >= 2 AND nota_v >= 4 THEN 'Em risco de alto valor'
        WHEN nota_r >= 2                 THEN 'Mornos'
        ELSE 'Perdidos'
    END AS segmento
FROM notas;
