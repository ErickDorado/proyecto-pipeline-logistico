# 🚚 Pipeline de Analytics Logístico

Proyecto end-to-end de análisis de operaciones logísticas: 
generación de datos, pipeline ETL, análisis SQL y dashboard ejecutivo en Power BI.

---

## 📊 Hallazgos principales

- **OTD global del 61.3%** — indica un problema sistémico de entregas a resolver
- **Córdoba tiene el peor OTD (41.1%)** versus CABA que lidera con 74.8%
- **Andreani es el carrier más confiable** (63.9% OTD, menor demora promedio)
- **Correo Argentino tiene el peor desempeño** (59.6% OTD, mayor costo promedio)
- **Rappi Envíos en CABA alcanza 77.6% OTD** — los carriers urbanos rinden mejor en ciudad
- **Febrero y Noviembre son los meses críticos** con OTD por debajo del 58%

---

## 🖼️ Dashboard

### Resumen Ejecutivo
![Resumen Ejecutivo](docs/resumen_ejecutivo.png)

### Análisis de Carriers
![Análisis de Carriers](docs/analisis_carriers.png)

### Geografía y Costos
![Geografía y Costos](docs/geografia_costos.png)

---
## 🛠️ Stack tecnológico

| Herramienta | Uso |
|-------------|-----|
| Python · pandas · numpy | Generación de datos y ETL |
| Faker | Datos sintéticos realistas |
| DuckDB · SQL | Análisis exploratorio y KPIs |
| Power BI · DAX | Dashboard ejecutivo |
| Excel | Fuente de datos consolidada |

---

## 🏗️ Arquitectura del pipeline
```text
Raw Data (CSV/XLSX)
↓
Python ETL
(limpieza + features)
↓
Tablas Analíticas          SQL Queries
(fact_orders, kpis)   →   (DuckDB)
↓
Power BI Dashboard
(3 páginas ejecutivas)

---

## 📁 Estructura del proyecto

proyecto-pipeline/
├── data/
│   ├── raw/                  # Dataset original generado
│   │   ├── logistics_raw.csv
│   │   ├── logistics_raw.xlsx
│   │   └── eda_overview.png
│   └── processed/            # Tablas post-ETL
│       ├── fact_orders.csv
│       ├── kpi_carrier.csv
│       ├── kpi_zona.csv
│       ├── kpi_mes.csv
│       └── logistics_analytics.xlsx
├── src/
│   ├── generate_data.py      # Generación del dataset
│   ├── eda.py                # Análisis exploratorio
│   └── etl.py                # Pipeline ETL
├── sql/
│   ├── analysis.sql          # Queries de negocio
│   └── run_queries.py        # Ejecución con DuckDB
├── dashboards/
│   ├── logistics_dashboard.pbix
│   └── logistics_dashboard.pdf
├── docs/
│   ├── resumen_ejecutivo.png
│   ├── analisis_carriers.png
│   └── geografia_costos.png
└── README.md
---

## 🚀 Cómo reproducir el proyecto

```bash
# 1. Clonar el repositorio
git clone https://github.com/ErickDorado/proyecto-pipeline-logistico
cd proyecto-pipeline-logistico

# 2. Instalar dependencias
pip install pandas numpy faker openpyxl matplotlib seaborn duckdb

# 3. Generar el dataset
python src/generate_data.py

# 4. Exploración de datos
python src/eda.py

# 5. Ejecutar el ETL
python src/etl.py

# 6. Correr queries SQL
python sql/run_queries.py

# 7. Abrir el dashboard
# Abrir dashboards/logistics_dashboard.pbix en Power BI Desktop
```

---

## 📈 KPIs del dashboard

| KPI | Valor | Descripción |
|-----|-------|-------------|
| OTD % | 61.3% | Pedidos entregados en fecha prometida |
| Demora promedio | 0.20 días | Desvío promedio respecto al SLA |
| Costo promedio | $1.335 | Costo de envío por pedido |
| Tasa devolución | 5.1% | Pedidos devueltos sobre el total |
| Costo por KG | $443 | Eficiencia del costo logístico |

---

## 🔍 Estructura del modelo de datos

**fact_orders** — tabla principal (5.000 filas · 20 columnas)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| order_id | string | Identificador único del pedido |
| fecha_pedido | date | Fecha de creación |
| carrier | string | Empresa de transporte |
| zona_destino | string | Zona geográfica de entrega |
| entrega_a_tiempo | bool | Si cumplió el SLA prometido |
| demora_dias | int | Días reales menos días prometidos |
| costo_pct_valor | float | Costo logístico como % del valor |

---
---

## 💡 Recomendaciones ejecutivas

### 🔴 Problema crítico — OTD al 61.3%
El estándar de la industria logística es **85% mínimo**. Estamos 24 puntos abajo, lo que significa que **4 de cada 10 pedidos no llegan cuando el cliente espera**. En términos de negocio: pérdida de recompra, reclamos, costo de atención al cliente y devoluciones.

**Objetivo:** alcanzar OTD del 80% para Q3 y 85% para fin de año.

---

### Decisión 1 — Renegociar o reemplazar Correo Argentino
Correo Argentino tiene el **peor OTD (59.6%) y el mayor costo promedio ($1.354)**. Es el peor en performance y el más caro.

**Acción:** redirigir su volumen a Andreani (mejor OTD 63.9%, costo similar).
**Impacto estimado:** +2 a +3 puntos de OTD global.

---

### Decisión 2 — Especializar carriers por zona
Los datos muestran que cada carrier tiene una zona donde rinde mejor:

| Carrier | Mejor zona | OTD |
|---------|-----------|-----|
| Rappi Envíos | CABA | 77.6% |
| OCA | GBA Norte | 72.0% |
| Andreani | GBA Sur / Oeste | 69-70% |

**Acción:** implementar regla de asignación de carrier por zona.
**Impacto estimado:** +5 a +8 puntos de OTD global.

---

### Decisión 3 — Intervenir Córdoba urgente
Córdoba tiene **41.1% OTD**, 20 puntos debajo del promedio. Casi 6 de cada 10 pedidos llegan tarde.

**Acción:** auditar el carrier que opera Córdoba y reemplazarlo. Como medida inmediata, aumentar el plazo prometido de 3 a 5 días para mejorar el OTD sin cambiar operaciones mientras se resuelve el problema de fondo.
**Impacto estimado:** +2 puntos de OTD global.

---

### Decisión 4 — Gestionar la estacionalidad
Febrero y Noviembre caen consistentemente por debajo del 58% OTD. Febrero por vacaciones y menor personal operativo. Noviembre por el pico de Hot Sale y Black Friday.

**Acción:** aumentar capacidad operativa en esos dos meses con personal adicional, stock adelantado y acuerdos de capacidad garantizada con carriers.
**Impacto estimado:** +1 a +2 puntos de OTD en meses críticos.

---

### Decisión 5 — Revisar la política de devoluciones
Tasa de devolución del **5.1% global**, con picos en Marzo (7.1%) y Mayo (6.1%). Cada devolución tiene costo doble: envío original más retorno.

**Acción:** cruzar devoluciones con categoría de producto para identificar si el problema es de packaging, descripción del producto o logística, antes de tomar decisiones operativas.

---

### Resumen ejecutivo

| Prioridad | Acción | Impacto OTD |
|-----------|--------|-------------|
| 🔴 Alta | Reasignar volumen de Correo Argentino a Andreani | +2 a +3 pts |
| 🔴 Alta | Regla de carrier por zona | +5 a +8 pts |
| 🔴 Alta | Intervención operativa en Córdoba | +2 pts |
| 🟡 Media | Refuerzo operativo Febrero y Noviembre | +1 a +2 pts |
| 🟡 Media | Análisis causa raíz de devoluciones | Reducción costos |

**Potencial total: pasar de 61.3% a ~75% OTD** con acciones operativas, sin inversión tecnológica nueva.

---

## 📋 Plan de acciones inmediatas

### Semana 1–2 — Acciones sin costo
```text
□ Mapear qué carrier opera cada zona actualmente
□ Implementar regla de asignación carrier por zona
  (Rappi → CABA, OCA → GBA Norte, Andreani → GBA Sur/Oeste)
□ Aumentar plazo prometido en Córdoba de 3 a 5 días
□ Identificar los 200 pedidos de Correo Argentino
  con mayor valor y reasignarlos a Andreani
```

### Semana 3–4 — Monitoreo
```text
□ Medir OTD diario por carrier con el nuevo esquema
□ Crear alerta si OTD cae debajo del 58% en alguna zona
□ Cruzar devoluciones con categoría de producto
□ Reunión de revisión con carriers de peor performance
```

### Mes 2 — Negociación
```text
□ Presentar datos de performance a cada carrier
□ Renegociar SLAs con penalidades por incumplimiento
□ Evaluar operador regional para Córdoba
□ Definir plan de capacidad para Febrero y Noviembre
```

### Mes 3 — Medición de impacto
```text
□ Comparar OTD pre vs post intervención
□ Calcular ahorro en devoluciones
□ Actualizar dashboard con nuevos datos
□ Presentar resultados a dirección
```

### KPIs de seguimiento semanal

| Métrica | Actual | Target Mes 1 | Target Mes 3 |
|---------|--------|--------------|--------------|
| OTD Global | 61.3% | 68% | 75% |
| OTD Córdoba | 41.1% | 55% | 65% |
| Tasa Devolución | 5.1% | 4.5% | 3.5% |
| OTD Correo Arg. | 59.6% | — | Reemplazado |

---

## 🔜 Próximos pasos

| | Análisis | Descripción |
|--|---------|-------------|
| 🔜 | **Simulación de impacto económico** | Traducir cada mejora de OTD a pesos: ahorro en devoluciones, reclamos y costo de atención al cliente |
| 🔜 | **Score de riesgo por pedido** | Modelo predictivo que asigne probabilidad de demora a cada pedido según zona, carrier y mes. Permite intervenir antes de que el problema ocurra |
| 🔜 | **Automatización del pipeline** | Scheduling diario del ETL para que el dashboard se actualice solo sin intervención manual |
| 🔜 | **Conexión a datos reales** | Reemplazar el dataset sintético por datos reales vía API o base de datos PostgreSQL |

## ⚠️ Limitaciones del dataset

- Dataset sintético generado con distribuciones estadísticas controladas
- Los valores de costo representan escenarios simulados, no tarifas reales de carriers
- La cobertura geográfica está simplificada a 6 zonas del mercado argentino