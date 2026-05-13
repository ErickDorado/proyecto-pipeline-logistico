-- ============================================
-- ANÁLISIS SQL — Pipeline Logístico
-- Motor: DuckDB (lee CSV directamente)
-- ============================================

-- KPI 1: OTD y demora por carrier
SELECT
    carrier,
    COUNT(*)                                                        AS total_pedidos,
    ROUND(AVG(CASE WHEN entrega_a_tiempo THEN 1.0 ELSE 0 END)*100, 1) AS otd_pct,
    ROUND(AVG(demora_dias), 2)                                      AS demora_promedio,
    ROUND(AVG(costo_envio), 0)                                      AS costo_promedio
FROM 'data/processed/fact_orders.csv'
GROUP BY carrier
ORDER BY otd_pct DESC;

-- KPI 2: Costo logístico como % del valor por zona
SELECT
    zona_destino,
    COUNT(*)                            AS total_pedidos,
    ROUND(AVG(costo_pct_valor), 1)      AS costo_pct_valor,
    ROUND(AVG(demora_dias), 2)          AS demora_promedio,
    ROUND(AVG(costo_por_kg), 0)         AS costo_por_kg
FROM 'data/processed/fact_orders.csv'
GROUP BY zona_destino
ORDER BY costo_pct_valor DESC;

-- KPI 3: Tendencia mensual de OTD y devoluciones
SELECT
    trimestre,
    mes,
    COUNT(*)                                                           AS total_pedidos,
    ROUND(AVG(CASE WHEN entrega_a_tiempo THEN 1.0 ELSE 0 END)*100, 1) AS otd_pct,
    ROUND(AVG(CASE WHEN es_devolucion    THEN 1.0 ELSE 0 END)*100, 1) AS tasa_devolucion
FROM 'data/processed/fact_orders.csv'
GROUP BY trimestre, mes
ORDER BY mes;

-- KPI 4: Mejor y peor combinación carrier × zona
SELECT
    carrier,
    zona_destino,
    COUNT(*)                                                           AS pedidos,
    ROUND(AVG(CASE WHEN entrega_a_tiempo THEN 1.0 ELSE 0 END)*100, 1) AS otd_pct,
    ROUND(AVG(demora_dias), 2)                                         AS demora_promedio
FROM 'data/processed/fact_orders.csv'
GROUP BY carrier, zona_destino
HAVING COUNT(*) > 50
ORDER BY otd_pct DESC
LIMIT 10;