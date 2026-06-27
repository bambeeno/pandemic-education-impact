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

---

## Análisis contextual del event study — Variaciones 2020-2023

Analizar las variaciones del gasto educativo como porcentaje del PBI durante el período 2020-2023 requiere separar lo que fue un espejismo estadístico de lo que fueron decisiones políticas y realidades económicas crudas.

---

### Casos extremos de caída

**Timor-Leste (-3.65 pp / -52%) — El colapso del fondo soberano y la ayuda externa**

La economía de Timor-Leste depende casi en su totalidad del Fondo del Petróleo (que financia hasta el 90% del presupuesto estatal) y de la ayuda internacional. En 2020, el precio del petróleo se desplomó y los mercados globales colapsaron, congelando los rendimientos de su fondo. El país arrastraba además fuerte inestabilidad política interna (impases presupuestarios entre el presidente y el parlamento). Cuando llegó el COVID-19, el gobierno priorizó subsidios de emergencia en efectivo para mitigar la pobreza extrema y la seguridad alimentaria, dejando la educación en un segundo plano. Al cerrarse las fronteras, la asistencia técnica y los fondos de agencias internacionales de desarrollo que cofinanciaban proyectos educativos se detuvieron en seco.

**Aruba (-27%) y Suriname (-23%) — El colapso del turismo y crisis de deuda**

Aruba es una de las economías más dependientes del turismo en el mundo. En 2020, su PBI cayó más del 25%. Sin ingresos fiscales, el gobierno tuvo que aplicar recortes nominales en el sector público —incluyendo maestros— como condición para recibir ayuda financiera de los Países Bajos. Suriname ya arrastraba una crisis económica severa antes de 2020, con deuda insostenible y devaluación masiva de su moneda. La pandemia terminó de asfixiar sus finanzas, obligando a un programa de austeridad extrema con el FMI que pulverizó el gasto social y educativo en términos reales.

---

### Casos extremos de aumento — Efecto denominador y flujos externos

**Macao SAR (+2.83 pp / +96.71%) — El espejismo del PBI casi cero**

Macao vive del turismo de casinos proveniente de China continental. Bajo la política de Zero-COVID de China, Macao cerró por completo y su PBI sufrió una contracción histórica de más del 50% en 2020. Sin embargo, el gobierno tiene gigantescas reservas fiscales acumuladas de años de bonanza y decidió mantener el gasto nominal en escuelas y salarios docentes usando esas reservas. Al dividirse un gasto educativo estable entre un PBI que se redujo a la mitad, el porcentaje se duplicó automáticamente. No fue una reforma educativa — fue matemática pura.

**Marshall Islands y Kiribati — Microestados dependientes de subsidios externos**

Estos países operan bajo el Tratado de Libre Asociación con EE. UU. (Marshall Islands) o reciben inyecciones masivas de ayuda de Australia, Taiwán y el Banco Asiático de Desarrollo. Durante la pandemia, los donantes enviaron fondos de emergencia empaquetados como apoyo presupuestario general. Dado que sus PBI locales son minúsculos y se contrajeron, la entrada masiva de dinero externo infló artificialmente el gasto público en todos los sectores, incluyendo educación.

**Sierra Leona y Cabo Verde — Apuestas genuinas de desarrollo**

En Sierra Leona el aumento es real y político. En 2018 el presidente Julius Maada Bio lanzó el programa Free Quality School Education (FQSE), comprometiéndose a destinar el 20% del presupuesto nacional a educación. Durante la pandemia el gobierno mantuvo ese compromiso a pesar de la crisis, lo que se tradujo en un incremento genuino de la inversión.

---

### Panorama regional — La brecha de la recuperación

**LATAM (-0.31 pp en recovery) — Austeridad forzada**

América Latina fue la región en desarrollo más golpeada económicamente por la pandemia y la que peor gestionó la post-pandemia en términos fiscales. Al llegar 2022, los países enfrentaban niveles de deuda altísimos acumulados por los bonos de emergencia de 2020, sumado a inflación global histórica. La respuesta generalizada de los ministerios de hacienda fue el ajuste fiscal para calmar a los mercados internacionales y frenar la inflación. Las escuelas en LATAM pasaron, en promedio, más tiempo cerradas que en cualquier otra región del mundo. Al reabrir, en lugar de una fuerte inversión para recuperar el rezago, la educación absorbió el costo de la consolidación fiscal.

**Europe (-0.20 pp en recovery) — El regreso de las reglas fiscales y la crisis energética**

En 2020-2021, la UE suspendió las reglas del Pacto de Estabilidad y Crecimiento y los gobiernos gastaron masivamente. En 2022-2023, con la inflación disparada y la crisis energética derivada de la guerra en Ucrania, Europa tuvo que reorientar presupuestos hacia subsidios energéticos y defensa, recortando sutilmente en áreas sociales como educación.

**Central Asia (+0.61 pp en recovery) — El boom de las materias primas y reformas del Estado**

Kazajistán, Uzbekistán y Turkmenistán se beneficiaron fuertemente del aumento de precios globales del petróleo, gas y minerales en 2022-2023. Sus economías no solo se recuperaron sino que crecieron con fuerza. Gobiernos como el de Uzbekistán y Kazajistán —con poblaciones muy jóvenes— utilizaron los excedentes para financiar planes de modernización educativa y digitalización que ya estaban planificados antes de la pandemia.

**South Asia y East Asia & Pacific — Inversión estratégica de largo plazo**

Estas regiones, lideradas por India, Indonesia y Vietnam, priorizan la educación como motor principal de su crecimiento industrial y atracción de inversión extranjera directa. El gasto se mantuvo alto en la fase de recuperación porque entienden la educación como infraestructura económica indispensable para mantener competitividad global.

---

## Análisis contextual del índice de recuperación — Casos extremos y divergentes

La brecha global en el gasto educativo se profundizó tras la pandemia: mientras los países desarrollados recuperaron o superaron sus niveles de inversión de 2019, las naciones de ingresos bajos y en desarrollo enfrentaron severas contracciones presupuestarias debido a crisis de deuda, inflación y shocks climáticos. El gasto gubernamental promedio global se estancó en torno al 4% del PBI, y la asistencia internacional para educación cayó notablemente al redireccionarse fondos hacia crisis geopolíticas y de seguridad.

---

### Casos de reconfiguración radical

**Vanuatu (índice 427) — Reconstrucción post-ciclones y ayuda externa**

Democracia con alta vulnerabilidad climática, azotada constantemente por ciclones que destruyen infraestructura escolar. Fuerte dependencia de asistencia oficial al desarrollo (AOD) y préstamos externos, principalmente de China. Su riesgo de sobreendeudamiento está clasificado como alto por el FMI. El salto de 1.77% en 2019 a 10.64% en 2023 representa un esfuerzo estatal masivo enfocado en alfabetización temprana y reconstrucción escolar post-ciclones — no un crecimiento orgánico del sistema educativo.

**Mauritania (índice 258) — Volatilidad extrema y posterior despegue**

Transición política pacífica en un entorno regional inestable (Sahel). Economía primaria impulsada por minería (hierro, oro) e incipiente explotación de gas. Registró caídas críticas durante la pandemia, tocando un piso de apenas 1.39% del PBI en 2022, para luego rebotar agresivamente hasta 4.71% en 2023 mediante una reforma nacional para expandir cobertura de educación primaria y secundaria.

---

### Casos divergentes — Respuestas y crisis

| País | Dinámica del gasto 2019-2023 |
|------|------------------------------|
| **Somalia** | Sistema en riesgo de colapso. Gasto doméstico casi inexistente; educación dependiente de flujos externos volátiles. El índice (142) es matemáticamente válido pero analíticamente irrelevante — el valor absoluto es cercano a cero en ambos períodos. |
| **Bangladesh** | Gasto estructuralmente bajo (~2% del PBI), estancado a pesar del crecimiento industrial sostenido. Abre una brecha notable entre expansión económica y desarrollo humano. |
| **Kazakhstan** | Gasto protegido institucionalmente por encima del 3-4% del PBI. Los excedentes del petróleo financiaron modernización digital y docente planificada antes de la pandemia. |
| **Suriname** | Crisis fiscal obligó a recortar partidas reales, deprimiendo salarios docentes y deteriorando infraestructura escolar. Estabilización gradual bajo programas del FMI, pero el índice (42) refleja el daño acumulado. |
| **Sierra Leone** | Implementó el programa Free Quality School Education (FQSE), subiendo la inversión a ~20% del presupuesto nacional durante el shock. Sin embargo, el índice de recovery (56) muestra que no sostuvo ese nivel — posiblemente por presión fiscal posterior o cambios en la metodología de reporte. |
| **Noruega** | Gasto robusto y constante por encima del 6% del PBI. El índice bajo (69) responde a que el valor 2019 era excepcionalmente alto y el dato de recovery disponible es 2022, posiblemente parcial. No refleja deterioro real del sistema educativo. |
| **Líbano** | Colapso macroeconómico histórico: devaluación de la moneda mayor al 95% e hiperinflación. Salarios docentes licuados, más de 1.1 millones de niños con educación interrumpida. El índice (59) refleja destrucción presupuestaria real. |

---

### Consideraciones clave para el análisis

- **Efecto denominador:** En economías pequeñas (microestados del Pacífico, Macao SAR), los saltos abruptos en el porcentaje del PBI pueden reflejar tanto caídas severas del PBI total como inyecciones puntuales de ayuda externa concentrada. El índice de recuperación hereda este sesgo — un índice extremadamente alto no siempre significa mejor sistema educativo.
- **Sostenibilidad fiscal:** La presión por el pago de deudas soberanas sigue siendo el principal obstáculo para que los países de bajos ingresos logren trayectorias estables de financiamiento educativo.
- **Dato parcial vs. deterioro real:** Casos como Noruega, UK o Japón aparecen sin dato de recovery por lag de reporte, no por recorte. Cualquier comparación regional que los incluya debe contemplar esta ausencia.