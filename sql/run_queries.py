import duckdb

con = duckdb.connect()

queries = {
    "OTD por Carrier": """
        SELECT carrier,
               COUNT(*) AS total_pedidos,
               ROUND(AVG(CASE WHEN entrega_a_tiempo THEN 1.0 ELSE 0 END)*100, 1) AS otd_pct,
               ROUND(AVG(demora_dias), 2) AS demora_promedio,
               ROUND(AVG(costo_envio), 0) AS costo_promedio
        FROM 'data/processed/fact_orders.csv'
        GROUP BY carrier ORDER BY otd_pct DESC
    """,
    "Costo % por Zona": """
        SELECT zona_destino,
               COUNT(*) AS total_pedidos,
               ROUND(AVG(costo_pct_valor), 1) AS costo_pct_valor,
               ROUND(AVG(demora_dias), 2) AS demora_promedio
        FROM 'data/processed/fact_orders.csv'
        GROUP BY zona_destino ORDER BY costo_pct_valor DESC
    """,
    "Tendencia Mensual": """
        SELECT trimestre, mes, COUNT(*) AS total_pedidos,
               ROUND(AVG(CASE WHEN entrega_a_tiempo THEN 1.0 ELSE 0 END)*100, 1) AS otd_pct,
               ROUND(AVG(CASE WHEN es_devolucion    THEN 1.0 ELSE 0 END)*100, 1) AS tasa_devolucion
        FROM 'data/processed/fact_orders.csv'
        GROUP BY trimestre, mes ORDER BY mes
    """,
    "Top Combinaciones Carrier x Zona": """
        SELECT carrier, zona_destino, COUNT(*) AS pedidos,
               ROUND(AVG(CASE WHEN entrega_a_tiempo THEN 1.0 ELSE 0 END)*100, 1) AS otd_pct
        FROM 'data/processed/fact_orders.csv'
        GROUP BY carrier, zona_destino HAVING COUNT(*) > 50
        ORDER BY otd_pct DESC LIMIT 10
    """
}

for nombre, query in queries.items():
    print(f"\n{'='*50}")
    print(f"  {nombre}")
    print('='*50)
    print(con.execute(query).df().to_string(index=False))

print("\n✅ Queries ejecutadas correctamente")