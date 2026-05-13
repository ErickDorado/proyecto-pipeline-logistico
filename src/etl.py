import pandas as pd
import numpy as np
import os

def extract():
    df = pd.read_csv('data/raw/logistics_raw.csv',
                     parse_dates=['fecha_pedido', 'fecha_entrega'])
    print(f"[EXTRACT] {len(df)} registros cargados")
    return df

def transform(df):
    # Features derivadas
    df['demora_dias']    = df['dias_reales'] - df['dias_prometidos']
    df['costo_por_kg']   = (df['costo_envio'] / df['peso_kg']).round(2)
    df['costo_pct_valor']= (df['costo_envio'] / df['valor_mercaderia'] * 100).round(2)
    df['es_devolucion']  = df['estado'] == 'Devuelto'
    df['semana_año']     = df['fecha_pedido'].dt.strftime('%Y-W%V')

    # Tabla de hechos
    fact_orders = df[[
        'order_id', 'fecha_pedido', 'fecha_entrega', 'mes', 'trimestre', 'semana_año',
        'producto_categoria', 'zona_destino', 'carrier', 'estado',
        'peso_kg', 'valor_mercaderia', 'costo_envio', 'costo_por_kg', 'costo_pct_valor',
        'dias_prometidos', 'dias_reales', 'demora_dias',
        'entrega_a_tiempo', 'es_devolucion'
    ]].copy()

    # KPIs por carrier
    kpi_carrier = df.groupby('carrier').agg(
        total_pedidos   = ('order_id', 'count'),
        otd_pct         = ('entrega_a_tiempo', 'mean'),
        demora_promedio = ('demora_dias', 'mean'),
        costo_promedio  = ('costo_envio', 'mean'),
        tasa_devolucion = ('es_devolucion', 'mean')
    ).reset_index().round(3)

    # KPIs por zona
    kpi_zona = df.groupby('zona_destino').agg(
        total_pedidos  = ('order_id', 'count'),
        otd_pct        = ('entrega_a_tiempo', 'mean'),
        costo_pct_valor= ('costo_pct_valor', 'mean'),
        valor_total    = ('valor_mercaderia', 'sum'),
        demora_promedio= ('demora_dias', 'mean')
    ).reset_index().round(3)

    # KPIs por mes (para tendencia en Power BI)
    kpi_mes = df.groupby(['trimestre', 'mes']).agg(
        total_pedidos   = ('order_id', 'count'),
        otd_pct         = ('entrega_a_tiempo', 'mean'),
        costo_promedio  = ('costo_envio', 'mean'),
        tasa_devolucion = ('es_devolucion', 'mean')
    ).reset_index().round(3)

    print(f"[TRANSFORM] fact_orders: {len(fact_orders)} filas, {fact_orders.shape[1]} columnas")
    print(f"[TRANSFORM] kpi_carrier: {len(kpi_carrier)} filas")
    print(f"[TRANSFORM] kpi_zona:    {len(kpi_zona)} filas")
    print(f"[TRANSFORM] kpi_mes:     {len(kpi_mes)} filas")
    return fact_orders, kpi_carrier, kpi_zona, kpi_mes

def load(fact_orders, kpi_carrier, kpi_zona, kpi_mes):
    os.makedirs('data/processed', exist_ok=True)

    # CSVs individuales
    fact_orders.to_csv('data/processed/fact_orders.csv', index=False)
    kpi_carrier.to_csv('data/processed/kpi_carrier.csv', index=False)
    kpi_zona.to_csv('data/processed/kpi_zona.csv', index=False)
    kpi_mes.to_csv('data/processed/kpi_mes.csv', index=False)

    # Excel consolidado para Power BI
    with pd.ExcelWriter('data/processed/logistics_analytics.xlsx', engine='openpyxl') as writer:
        fact_orders.to_excel(writer, sheet_name='fact_orders', index=False)
        kpi_carrier.to_excel(writer, sheet_name='kpi_carrier', index=False)
        kpi_zona.to_excel(writer, sheet_name='kpi_zona', index=False)
        kpi_mes.to_excel(writer, sheet_name='kpi_mes', index=False)

    print("[LOAD] Archivos en data/processed/:")
    for f in os.listdir('data/processed'):
        size = os.path.getsize(f'data/processed/{f}')
        print(f"       {f} ({size/1024:.1f} KB)")

if __name__ == '__main__':
    print("=" * 45)
    print("ETL — Pipeline Logístico")
    print("=" * 45)
    df = extract()
    fact_orders, kpi_carrier, kpi_zona, kpi_mes = transform(df)
    load(fact_orders, kpi_carrier, kpi_zona, kpi_mes)
    print("\n✅ ETL completado")