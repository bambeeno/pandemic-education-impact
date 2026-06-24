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
| `01_preparacion.py` | Filter 2015–2025, validate pre/during/post coverage | ⬜ Pending |
| `02_serie_temporal.py` | Global and regional year-by-year trend | ⬜ Pending |
| `03_evento.py` | Event study: baseline vs shock vs recovery | ⬜ Pending |
| `04_recuperacion.py` | Recovery index by country and region | ⬜ Pending |
| `05_exportar.py` | Excel export — 5 sheets + merge-ready for Project 4 | ⬜ Pending |
| `06_visualizacion.py` | Time series, heatmap, recovery chart | ⬜ Pending |

## Key Questions
- How did the pandemic affect education spending globally and by region?
- Which countries cut spending the most in 2020–2021?
- Which countries had recovered by 2022–2023, and which hadn't?
- Were there countries that *increased* spending during the pandemic?

## Known Limitations
- Public spending ≠ total education spending (private/household excluded)
- Coverage gaps in 2023–2025 data (reporting lag)
- Recovery index uses 2019 as baseline — single-year baseline, sensitive to outliers