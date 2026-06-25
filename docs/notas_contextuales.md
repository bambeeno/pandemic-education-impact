# Notas contextuales — Pandemic Education Impact

Documento de referencia para decisiones de análisis y hallazgos de contexto que no son evidentes solo con los números. Se actualiza a medida que avanza el pipeline.

---

## ¿Por qué solo 38 países en 2024 y 2 en 2025?

Lag de reporte. Los países reportan sus datos educativos a la UNESCO con 1 a 3 años de retraso: primero cierran el ejercicio fiscal, luego lo auditan, luego lo reportan al organismo internacional. En 2024 solo los países más ágiles administrativamente ya tienen datos cargados. En 2025 prácticamente nadie. No es un problema del dataset — es la naturaleza del dato.

**Decisión de análisis:** 2024 y 2025 se tratan como años parciales, no representativos. No se sacan conclusiones de su variación interanual. Se mantienen en el dataset pero se marcan como cobertura insuficiente en cualquier visualización o tabla que los incluya.

---

## ¿Por qué el lag específico de USA y Canadá?

North America no tiene datos desde 2023 en el dataset. Varias razones combinadas:

- **Sistema federal:** tanto USA como Canadá tienen educación descentralizada — cada estado/provincia reporta por separado y luego se consolida a nivel nacional. Ese proceso es más lento que en países con sistema educativo centralizado.
- **Ciclo fiscal distinto:** el año fiscal de USA termina en septiembre, no en diciembre. Eso corre todo el calendario de cierre y reporte.
- **Capas de validación:** los países desarrollados con sistemas estadísticos robustos paradójicamente tardan más porque tienen más instancias de validación antes de publicar.
- **UNESCO vs OCDE:** USA y Canadá suelen reportar primero a la OCDE (Education at a Glance) y ese dato migra a UNESCO con demora adicional.

**Decisión de análisis:** North America se mantiene en el análisis regional para los años con datos disponibles (2015–2022), pero se excluye de comparaciones que involucren 2023 en adelante.

---

## El aumento del gasto en 2020 no significa mayor inversión

El gasto educativo como % del PBI *subió* en 2020 en todas las regiones (global: +0.31 pp, +7.15%). Esto es contraintuitivo pero se explica por el **efecto denominador**: los PBI colapsaron durante la pandemia más rápido que los presupuestos educativos. Aunque el gasto absoluto se mantuviera o cayera levemente, como porcentaje del PBI aumentó.

La caída real llegó después — 2021 (-0.17 pp), 2022 (-0.22 pp) y especialmente **2023 (-0.35 pp, -8.20%)**, cuando los gobiernos empezaron a ajustar el gasto fiscal con rezago, ya con los PBI en recuperación.

**Implicancia para el análisis:** el "shock pandémico" en este dataset no es 2020 — es el período 2021–2023. Cualquier narrativa de impacto debe contemplar este rezago.

---

## Fix de mapeo regional — 18 países sin región en primera corrida

En la primera ejecución de `02_serie_temporal.py`, 18 países quedaron sin región asignada por gaps en el diccionario manual de códigos ISO. Corregidos en el mismo script antes del primer commit válido. Los casos fueron:

| País | Código | Región asignada | Motivo del gap |
|------|--------|-----------------|----------------|
| Anguilla | AIA | Latin America & Caribbean | Territorio dependiente de UK |
| Aruba | ABW | Latin America & Caribbean | Territorio dependiente de Países Bajos |
| Bahamas | BHS | Latin America & Caribbean | Omisión simple |
| Bermuda | BMU | Latin America & Caribbean | Territorio dependiente de UK |
| British Virgin Islands | VGB | Latin America & Caribbean | Territorio dependiente de UK |
| Cayman Islands | CYM | Latin America & Caribbean | Territorio dependiente de UK |
| China, Hong Kong SAR | HKG | East Asia & Pacific | Reportado por separado de China |
| China, Macao SAR | MAC | East Asia & Pacific | Reportado por separado de China |
| Cook Islands | COK | East Asia & Pacific | Territorio asociado a Nueva Zelanda |
| Curaçao | CUW | Latin America & Caribbean | Territorio dependiente de Países Bajos |
| Monaco | MCO | Europe | Micro-estado omitido |
| Montserrat | MSR | Latin America & Caribbean | Territorio dependiente de UK |
| Puerto Rico | PRI | Latin America & Caribbean | Territorio de USA reportado por separado |
| San Marino | SMR | Europe | Micro-estado omitido |
| Andorra | AND | Europe | Micro-estado omitido |
| Turks and Caicos Islands | TCA | Latin America & Caribbean | Territorio dependiente de UK |
| Türkiye | TUR | Europe | Cambio de nombre (antes Turkey) no reflejado |
| Montserrat | MSR | Latin America & Caribbean | Territorio dependiente de UK |

**Decisión:** todos incluidos en sus regiones correspondientes. Ninguno se excluye del análisis.