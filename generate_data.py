import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker('es_AR')
np.random.seed(42)
random.seed(42)

N = 5000

productos = ['Electrónica', 'Indumentaria', 'Alimentos', 'Ferretería', 'Farmacia']
zonas = ['CABA', 'GBA Norte', 'GBA Sur', 'GBA Oeste', 'Córdoba', 'Rosario']
carriers = ['OCA', 'Andreani', 'Correo Argentino', 'PickIt', 'Rappi Envíos']
estados = ['Entregado', 'En tránsito', 'Demorado', 'Devuelto', 'Cancelado']
pesos_estado = [0.72, 0.12, 0.08, 0.05, 0.03]

fechas_base = pd.date_range('2023-01-01', '2024-12-31', periods=N)

df = pd.DataFrame({
    'order_id':           [f'ORD-{i:05d}' for i in range(1, N+1)],
    'fecha_pedido':       fechas_base,
    'producto_categoria': np.random.choice(productos, N),
    'zona_destino':       np.random.choice(zonas, N),
    'carrier':            np.random.choice(carriers, N),
    'peso_kg':            np.round(np.random.exponential(scale=3, size=N).clip(0.1, 30), 2),
    'valor_mercaderia':   np.round(np.random.lognormal(mean=7, sigma=1, size=N), 2),
    'costo_envio':        np.round(np.random.uniform(150, 2500, N), 2),
    'dias_prometidos':    np.random.choice([1, 2, 3, 5, 7], N, p=[0.1, 0.25, 0.35, 0.2, 0.1]),
    'estado':             np.random.choice(estados, N, p=pesos_estado),
})

delay_factor = {
    'CABA': 0.0, 'GBA Norte': 0.3, 'GBA Sur': 0.4,
    'GBA Oeste': 0.5, 'Córdoba': 1.2, 'Rosario': 1.0
}

df['dias_reales'] = df.apply(
    lambda r: max(1, int(r['dias_prometidos'] + np.random.normal(delay_factor[r['zona_destino']], 1.5))),
    axis=1
)

df['entrega_a_tiempo'] = df['dias_reales'] <= df['dias_prometidos']
df['fecha_entrega']    = df['fecha_pedido'] + pd.to_timedelta(df['dias_reales'], unit='D')
df['mes']              = df['fecha_pedido'].dt.month
df['trimestre']        = df['fecha_pedido'].dt.quarter
df['semana']           = df['fecha_pedido'].dt.isocalendar().week.astype(int)

df.to_csv('logistics_raw.csv', index=False)
df.to_excel('logistics_raw.xlsx', index=False)

print(f"✅ Dataset generado: {len(df)} registros")
print(f"   Columnas: {list(df.columns)}")
print(f"\n📊 OTD global: {df['entrega_a_tiempo'].mean():.1%}")
print(f"   Estados:\n{df['estado'].value_counts()}")