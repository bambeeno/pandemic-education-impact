# 🦠 Pandemic Education Impact

Analysis of the COVID-19 pandemic's impact on global education spending (% of GDP),
with pre/during/post comparison and a country-level recovery index.

Part of a portfolio series on Human Development data:
- Project 1 — HDI global analysis (exploration & cleaning)
- Project 2 — Global education spending (full pipeline)
- **Project 3 — Pandemic impact on education spending** ← you are here
- Project 4 — HDI × education spending correlation (upcoming)

## Stack
Python · Pandas · Matplotlib · Seaborn · OpenPyXL

## Dataset
UNESCO UIS — Government expenditure on education (% of GDP)
Indicator: `XGDP.FSGOV` · Coverage: 206 countries · 1970–2025
Source: SDG 4 Education – Global and Thematic Indicators (last update: Feb 2026)
Reused from Project 2 pipeline — `02_education_spending_clean.csv`

## Pipeline
| Script | Description | Status |
|--------|-------------|--------|
| `01_preparacion.py` | Filter 2015–2025, period classification, coverage flags | ✅ Done |
| `02_serie_temporal.py` | Global and regional year-by-year trend, rolling avg, region × year pivot | ✅ Done |
| `03_evento.py` | Event study: baseline (2015-2019) vs shock (2020-2021) vs recovery (2022-2023) | ✅ Done |
| `04_recuperacion.py` | Recovery index by country and region (baseline: 2019) | ✅ Done |
| `05_exportar.py` | Excel export — 8 sheets + merge-ready for Project 4 | ✅ Done |
| `06_visualizacion.py` | Time series, heatmap, recovery chart | ⬜ Pending |

## Key Questions
- How did the pandemic affect education spending globally and by region?
- Which countries cut spending the most in 2020–2021?
- Which countries had recovered by 2022–2023, and which hadn't?
- Were there countries that *increased* spending during the pandemic?

## Key Findings
- The apparent spending increase in 2020 (+0.31 pp globally) was largely a denominator
  effect — GDP collapsed faster than education budgets, inflating the % of GDP metric.
- The real cuts came later: 2021–2023 saw sustained decline, with 2023 being the worst
  year of the period (-0.35 pp, -8.20% vs 2022).
- Of 155 countries with a calculable recovery index, 83 (54%) had not recovered their
  2019 spending level by 2022–2023.
- Latin America & Caribbean is the most lagged region (only 31.4% of countries recovered),
  followed by Europe (37.5%).
- South Asia leads recovery (83.3% of countries above 2019 baseline), driven by India,
  Bangladesh and Sri Lanka.
- Central Asia is the only region where the recovery mean exceeded the pre-pandemic
  baseline by a significant margin (+0.61 pp), boosted by commodity export revenues.

## Known Limitations
- Public spending ≠ total education spending (private/household excluded)
- Coverage gaps in 2024 (38 countries) and 2025 (2 countries) due to reporting lag
- Recovery index uses 2019 as single-year baseline — sensitive to outliers
- The denominator effect distorts % of GDP comparisons for small economies and
  commodity-dependent countries during periods of sharp GDP contraction
- USA, UK, Japan, Colombia and Ukraine have no recovery data due to reporting lag,
  not actual deterioration