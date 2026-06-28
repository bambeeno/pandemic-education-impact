# 🦠 Impacto de la Pandemia en el Gasto Educativo Global

Análisis del impacto de la pandemia de COVID-19 en el gasto público en educación
(% del PBI) a nivel global, con comparación pre/durante/post pandemia e índice de
recuperación por país.

Parte de una serie de portfolio sobre datos de Desarrollo Humano:
- Proyecto 1 — Análisis global del IDH (exploración y limpieza)
- Proyecto 2 — Gasto educativo global (pipeline completo)
- **Proyecto 3 — Impacto de la pandemia en el gasto educativo** ← estás aquí
- Proyecto 4 — Correlación IDH × gasto educativo (próximamente)

## Stack
Python · Pandas · Matplotlib · Seaborn · OpenPyXL

## Dataset
UNESCO UIS — Gasto gubernamental en educación (% del PBI)
Indicador: `XGDP.FSGOV` · Cobertura: 206 países · 1970–2025
Fuente: SDG 4 Education – Global and Thematic Indicators (última actualización: feb 2026)
Reutilizado del pipeline del Proyecto 2 — `02_education_spending_clean.csv`

## Pipeline
| Script | Descripción | Estado |
|--------|-------------|--------|
| `01_preparacion.py` | Filtro 2015–2025, clasificación de períodos, flags de cobertura | ✅ Hecho |
| `02_serie_temporal.py` | Tendencia global y regional año a año, rolling avg, pivot región × año | ✅ Hecho |
| `03_evento.py` | Event study: baseline (2015-2019) vs shock (2020-2021) vs recovery (2022-2023) | ✅ Hecho |
| `04_recuperacion.py` | Índice de recuperación por país y región (baseline: 2019) | ✅ Hecho |
| `05_exportar.py` | Exportación a Excel — 8 hojas + merge-ready para Proyecto 4 | ✅ Hecho |
| `06_visualizacion.py` | Serie temporal, heatmap, gráfico de recuperación | ✅ Hecho |
## Preguntas clave
- ¿Cómo afectó la pandemia al gasto educativo global y por región?
- ¿Qué países recortaron más el gasto en 2020–2021?
- ¿Qué países se habían recuperado para 2022–2023 y cuáles no?
- ¿Hubo países que *aumentaron* el gasto durante la pandemia?

## Hallazgos principales
- El aumento aparente del gasto en 2020 (+0.31 pp a nivel global) fue en gran parte un
  efecto denominador: el PBI colapsó más rápido que los presupuestos educativos,
  inflando la métrica de % del PBI.
- Los recortes reales llegaron después: 2021–2023 registró una caída sostenida, siendo
  2023 el peor año del período (-0.35 pp, -8.20% respecto a 2022).
- De 155 países con índice de recuperación calculable, 83 (54%) no habían recuperado
  su nivel de gasto de 2019 al cierre de 2022–2023.
- América Latina y el Caribe es la región más rezagada (solo el 31.4% de los países
  se recuperó), seguida de Europa (37.5%).
- Asia del Sur lidera la recuperación (83.3% de países por encima del baseline 2019),
  impulsada por India, Bangladesh y Sri Lanka.
- Asia Central es la única región donde la media de recuperación superó
  significativamente el baseline pre-pandemia (+0.61 pp), impulsada por los ingresos
  de exportación de materias primas.

## Limitaciones conocidas
- Gasto público ≠ gasto total en educación (sector privado y hogares excluidos)
- Cobertura parcial en 2024 (38 países) y 2025 (2 países) por lag de reporte
- El índice de recuperación usa 2019 como año base único — sensible a outliers
- El efecto denominador distorsiona las comparaciones de % del PBI para economías
  pequeñas y países dependientes de materias primas durante períodos de fuerte
  contracción del PBI
- USA, UK, Japón, Colombia y Ucrania no tienen dato de recovery por lag de reporte,
  no por deterioro real del sistema educativo