-- Resumo de cada segmento: tamanho, peso na receita e perfil médio.

SELECT
    segmento,
    COUNT(*)                                                      AS clientes,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)            AS pct_clientes,
    ROUND(SUM(valor_total), 2)                                    AS receita,
    ROUND(100.0 * SUM(valor_total) / SUM(SUM(valor_total)) OVER (), 1) AS pct_receita,
    ROUND(AVG(valor_total), 2)                                    AS gasto_medio,
    ROUND(AVG(recencia_dias))                                     AS recencia_media_dias,
    ROUND(AVG(frequencia), 2)                                     AS frequencia_media
FROM clientes_rfm
GROUP BY segmento
ORDER BY receita DESC;
