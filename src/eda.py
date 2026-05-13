import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

df = pd.read_csv('logistics_raw.csv', parse_dates=['fecha_pedido', 'fecha_entrega'])

print("=" * 45)
print("CALIDAD DE DATOS")
print("=" * 45)
print(f"Registros:   {len(df)}")
print(f"Columnas:    {df.shape[1]}")
print(f"Nulos:\n{df.isnull().sum()}")
print(f"Duplicados:  {df.duplicated('order_id').sum()}")

print("\n" + "=" * 45)
print("KPIs PRINCIPALES")
print("=" * 45)
otd = df['entrega_a_tiempo'].mean()
print(f"OTD global:          {otd:.1%}")
print(f"Demora promedio:     {(df['dias_reales'] - df['dias_prometidos']).mean():.2f} días")
print(f"Costo envío prom:    ${df['costo_envio'].mean():,.0f}")
print(f"Tasa devolución:     {(df['estado'] == 'Devuelto').mean():.1%}")

print("\nOTD por carrier:")
print(df.groupby('carrier')['entrega_a_tiempo'].mean().sort_values().apply(lambda x: f"{x:.1%}"))

print("\nOTD por zona:")
print(df.groupby('zona_destino')['entrega_a_tiempo'].mean().sort_values().apply(lambda x: f"{x:.1%}"))

# --- GRÁFICOS ---
fig = plt.figure(figsize=(14, 10))
fig.patch.set_facecolor('#0d0d14')
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.35)

color_accent = '#E8FF47'
color_bar    = '#47CFFF'
color_neg    = '#FF6B6B'

ax_style = dict(facecolor='#111118', tick_params=dict(colors='#888'))

def style_ax(ax, title):
    ax.set_facecolor('#111118')
    ax.tick_params(colors='#888', labelsize=9)
    ax.set_title(title, color='#ccc', fontsize=11, pad=10)
    for spine in ax.spines.values():
        spine.set_edgecolor('#222')

# 1. OTD por carrier
ax1 = fig.add_subplot(gs[0, 0])
otd_c = df.groupby('carrier')['entrega_a_tiempo'].mean().sort_values()
bars = ax1.barh(otd_c.index, otd_c.values * 100, color=color_bar, height=0.6)
ax1.axvline(otd * 100, color=color_accent, linestyle='--', linewidth=1.2, label=f'Promedio {otd:.0%}')
ax1.set_xlabel('OTD %', color='#888', fontsize=9)
ax1.legend(fontsize=8, facecolor='#1a1a2a', labelcolor='#aaa')
style_ax(ax1, 'OTD % por Carrier')

# 2. Distribución de demora
ax2 = fig.add_subplot(gs[0, 1])
delay = df['dias_reales'] - df['dias_prometidos']
ax2.hist(delay, bins=25, color=color_bar, edgecolor='#0d0d14', alpha=0.85)
ax2.axvline(0, color=color_accent, linestyle='--', linewidth=1.2, label='Sin demora')
ax2.axvline(delay.mean(), color=color_neg, linestyle='--', linewidth=1.2, label=f'Media {delay.mean():.1f}d')
ax2.set_xlabel('Días de demora', color='#888', fontsize=9)
ax2.legend(fontsize=8, facecolor='#1a1a2a', labelcolor='#aaa')
style_ax(ax2, 'Distribución de Demora')

# 3. Costo promedio por zona
ax3 = fig.add_subplot(gs[1, 0])
costo_z = df.groupby('zona_destino')['costo_envio'].mean().sort_values()
ax3.barh(costo_z.index, costo_z.values, color=color_accent, height=0.6)
ax3.set_xlabel('Costo promedio ($)', color='#888', fontsize=9)
style_ax(ax3, 'Costo Envío Promedio por Zona')

# 4. Volumen mensual
ax4 = fig.add_subplot(gs[1, 1])
vol = df.groupby('mes')['order_id'].count()
ax4.plot(vol.index, vol.values, color=color_accent, marker='o', linewidth=2, markersize=5)
ax4.fill_between(vol.index, vol.values, alpha=0.15, color=color_accent)
ax4.set_xlabel('Mes', color='#888', fontsize=9)
ax4.set_xticks(range(1, 13))
style_ax(ax4, 'Volumen de Pedidos por Mes')

fig.suptitle('EDA — Pipeline Logístico', color='#fff', fontsize=14, y=1.01)
plt.savefig('eda_overview.png', dpi=150, bbox_inches='tight', facecolor='#0d0d14')
print("\n✅ Gráfico guardado: eda_overview.png")