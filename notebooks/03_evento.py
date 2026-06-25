# 03_evento.py
# Proyecto 3 — Pandemic Education Impact
# Objetivo: event study — comparar baseline (2015-2019), shock (2020-2021)
# y recovery (2022+) por país y región.

import pandas as pd
import os

# ── Rutas ──────────────────────────────────────────────────────────────────────
base_dir    = os.path.dirname(os.path.abspath(__file__))
input_path  = os.path.join(base_dir, '..', 'output', '02_prep_con_region.csv')
output_path = os.path.join(base_dir, '..', 'output', '03_evento.csv')
output_reg  = os.path.join(base_dir, '..', 'output', '03_evento_regional.csv')

# ── Carga ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(input_path)
print(f"Dataset cargado: {df.shape[0]:,} filas\n")

# Solo análisis principal
df = df[df['flag_analisis_principal'] == True].copy()
print(f"Registros en análisis principal: {df.shape[0]:,}")
print(f"Países: {df['country_name'].nunique()}\n")

# ── A. Baseline por país: promedio 2015-2019 ───────────────────────────────────
baseline = (
    df[df['year'].between(2015, 2019)]
    .groupby('country_name')['value_pct_gdp']
    .agg(
        baseline_mean  = 'mean',
        baseline_std   = 'std',
        baseline_n     = 'count',
    )
    .reset_index()
    .round(4)
)

print(f"Países con baseline 2015-2019: {len(baseline)}")
print(f"Baseline global (media de medias): {baseline['baseline_mean'].mean():.4f}%\n")

# ── B. Shock por país: promedio 2020-2021 ─────────────────────────────────────
shock = (
    df[df['year'].between(2020, 2021)]
    .groupby('country_name')['value_pct_gdp']
    .agg(
        shock_mean = 'mean',
        shock_n    = 'count',
    )
    .reset_index()
    .round(4)
)

print(f"Países con dato en período shock (2020-2021): {len(shock)}\n")

# ── C. Recovery por país: promedio 2022-2023 ──────────────────────────────────
# Excluimos 2024-2025 por cobertura insuficiente
recovery = (
    df[df['year'].between(2022, 2023)]
    .groupby('country_name')['value_pct_gdp']
    .agg(
        recovery_mean = 'mean',
        recovery_n    = 'count',
    )
    .reset_index()
    .round(4)
)

print(f"Países con dato en período recovery (2022-2023): {len(recovery)}\n")

# ── D. Merge de los tres períodos ─────────────────────────────────────────────
evento = baseline.merge(shock, on='country_name', how='left')
evento = evento.merge(recovery, on='country_name', how='left')

# Agregar región
region_map = df[['country_name', 'region']].drop_duplicates()
evento = evento.merge(region_map, on='country_name', how='left')

# ── E. Cálculo de deltas ──────────────────────────────────────────────────────
evento['delta_shock_pp']    = (evento['shock_mean']    - evento['baseline_mean']).round(4)
evento['delta_recovery_pp'] = (evento['recovery_mean'] - evento['baseline_mean']).round(4)
evento['delta_shock_pct']   = ((evento['delta_shock_pp']    / evento['baseline_mean']) * 100).round(2)
evento['delta_recovery_pct']= ((evento['delta_recovery_pp'] / evento['baseline_mean']) * 100).round(2)

# ── F. Clasificación del impacto pandémico ────────────────────────────────────
def clasificar_impacto(delta):
    if pd.isna(delta):
        return 'sin_dato'
    elif delta >= 0.5:
        return 'aumento_fuerte'
    elif delta >= 0.1:
        return 'aumento_leve'
    elif delta >= -0.1:
        return 'estable'
    elif delta >= -0.5:
        return 'caida_leve'
    else:
        return 'caida_fuerte'

evento['impacto_shock'] = evento['delta_shock_pp'].apply(clasificar_impacto)

# ── G. Resumen global ─────────────────────────────────────────────────────────
print("── Resumen global por período ──────────────────────────────────────────")
print(f"  Baseline  2015-2019:  {evento['baseline_mean'].mean():.4f}% (n={len(evento[evento['baseline_n']>0])} países)")
print(f"  Shock     2020-2021:  {evento['shock_mean'].mean():.4f}% (n={evento['shock_n'].notna().sum()} países)")
print(f"  Recovery  2022-2023:  {evento['recovery_mean'].mean():.4f}% (n={evento['recovery_n'].notna().sum()} países)")
print()

print("── Delta shock (vs baseline) ───────────────────────────────────────────")
print(f"  Media global:   {evento['delta_shock_pp'].mean():+.4f} pp")
print(f"  Mediana global: {evento['delta_shock_pp'].median():+.4f} pp")
print()

print("── Delta recovery (vs baseline) ────────────────────────────────────────")
print(f"  Media global:   {evento['delta_recovery_pp'].mean():+.4f} pp")
print(f"  Mediana global: {evento['delta_recovery_pp'].median():+.4f} pp")
print()

# ── H. Distribución del impacto ───────────────────────────────────────────────
print("── Clasificación del impacto pandémico ─────────────────────────────────")
print(evento['impacto_shock'].value_counts().to_string())
print()

# ── I. Top 5 países con mayor caída y mayor aumento durante el shock ──────────
print("── Top 5 países con mayor CAÍDA durante shock ──────────────────────────")
print(
    evento[evento['delta_shock_pp'].notna()]
    .nsmallest(5, 'delta_shock_pp')
    [['country_name', 'region', 'baseline_mean', 'shock_mean', 'delta_shock_pp', 'delta_shock_pct']]
    .to_string(index=False)
)
print()

print("── Top 5 países con mayor AUMENTO durante shock ────────────────────────")
print(
    evento[evento['delta_shock_pp'].notna()]
    .nlargest(5, 'delta_shock_pp')
    [['country_name', 'region', 'baseline_mean', 'shock_mean', 'delta_shock_pp', 'delta_shock_pct']]
    .to_string(index=False)
)
print()

# ── J. Resumen regional ───────────────────────────────────────────────────────
regional = (
    evento.groupby('region')
    .agg(
        n_paises          = ('country_name', 'count'),
        baseline_mean     = ('baseline_mean', 'mean'),
        shock_mean        = ('shock_mean', 'mean'),
        recovery_mean     = ('recovery_mean', 'mean'),
        delta_shock_pp    = ('delta_shock_pp', 'mean'),
        delta_recovery_pp = ('delta_recovery_pp', 'mean'),
    )
    .reset_index()
    .round(4)
)

print("── Resumen regional ────────────────────────────────────────────────────")
print(regional.to_string(index=False))
print()

# ── Export ────────────────────────────────────────────────────────────────────
evento.to_csv(output_path, index=False)
regional.to_csv(output_reg, index=False)

print(f"Outputs exportados:")
print(f"  {output_path}")
print(f"  {output_reg}")
print(f"Shape evento: {evento.shape}")