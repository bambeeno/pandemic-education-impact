# 04_recuperacion.py
# Proyecto 3 — Pandemic Education Impact
# Objetivo: calcular índice de recuperación por país y región
# usando 2019 como año base (dato puntual, no promedio)

import pandas as pd
import os

# ── Rutas ──────────────────────────────────────────────────────────────────────
base_dir    = os.path.dirname(os.path.abspath(__file__))
input_path  = os.path.join(base_dir, '..', 'output', '02_prep_con_region.csv')
evento_path = os.path.join(base_dir, '..', 'output', '03_evento.csv')
output_path = os.path.join(base_dir, '..', 'output', '04_recuperacion.csv')
output_reg  = os.path.join(base_dir, '..', 'output', '04_recuperacion_regional.csv')

# ── Carga ──────────────────────────────────────────────────────────────────────
df     = pd.read_csv(input_path)
evento = pd.read_csv(evento_path)

df = df[df['flag_analisis_principal'] == True].copy()
print(f"Dataset cargado: {df.shape[0]:,} filas, {df['country_name'].nunique()} países\n")

# ── A. Valor puntual 2019 por país (baseline de referencia) ───────────────────
base_2019 = (
    df[df['year'] == 2019]
    [['country_name', 'value_pct_gdp', 'region']]
    .rename(columns={'value_pct_gdp': 'valor_2019'})
)
print(f"Países con dato en 2019: {len(base_2019)}\n")

# ── B. Último año disponible por país en recovery (2022-2023) ─────────────────
recovery = (
    df[df['year'].between(2022, 2023)]
    .sort_values('year', ascending=False)
    .groupby('country_name')
    .first()
    .reset_index()
    [['country_name', 'year', 'value_pct_gdp']]
    .rename(columns={'value_pct_gdp': 'valor_recovery', 'year': 'año_recovery'})
)
print(f"Países con dato en recovery (2022-2023): {len(recovery)}\n")

# ── C. Merge y cálculo del índice ─────────────────────────────────────────────
recup = base_2019.merge(recovery, on='country_name', how='left')

# Índice de recuperación: 100 = recuperó el nivel 2019
# > 100 = superó el pre-pandemia
# < 100 = aún por debajo
recup['recovery_index'] = (
    (recup['valor_recovery'] / recup['valor_2019']) * 100
).round(2)

recup['delta_vs_2019_pp'] = (
    recup['valor_recovery'] - recup['valor_2019']
).round(4)

# ── D. Clasificación del estado de recuperación ───────────────────────────────
def clasificar_recuperacion(idx):
    if pd.isna(idx):
        return 'sin_dato_recovery'
    elif idx >= 110:
        return 'superó_baseline'
    elif idx >= 95:
        return 'recuperado'
    elif idx >= 80:
        return 'recuperación_parcial'
    else:
        return 'rezagado'

recup['estado_recuperacion'] = recup['recovery_index'].apply(clasificar_recuperacion)

# ── E. Resumen global ─────────────────────────────────────────────────────────
con_dato = recup[recup['recovery_index'].notna()]

print("── Resumen global del índice de recuperación ───────────────────────────")
print(f"  Países con índice calculable:  {len(con_dato)}")
print(f"  Sin dato de recovery:          {recup['recovery_index'].isna().sum()}")
print(f"  Media del índice:              {con_dato['recovery_index'].mean():.2f}")
print(f"  Mediana del índice:            {con_dato['recovery_index'].median():.2f}")
print(f"  Países que superaron 2019:     {(con_dato['recovery_index'] >= 100).sum()}")
print(f"  Países por debajo de 2019:     {(con_dato['recovery_index'] < 100).sum()}")
print()

print("── Distribución por estado de recuperación ─────────────────────────────")
print(recup['estado_recuperacion'].value_counts().to_string())
print()

# ── F. Top y bottom del índice ────────────────────────────────────────────────
print("── Top 10 países mejor recuperados (índice más alto) ───────────────────")
print(
    con_dato.nlargest(10, 'recovery_index')
    [['country_name', 'region', 'valor_2019', 'valor_recovery', 'año_recovery', 'recovery_index', 'delta_vs_2019_pp']]
    .to_string(index=False)
)
print()

print("── Top 10 países menos recuperados (índice más bajo) ───────────────────")
print(
    con_dato.nsmallest(10, 'recovery_index')
    [['country_name', 'region', 'valor_2019', 'valor_recovery', 'año_recovery', 'recovery_index', 'delta_vs_2019_pp']]
    .to_string(index=False)
)
print()

# ── G. Resumen regional ───────────────────────────────────────────────────────
regional = (
    recup.groupby('region')
    .agg(
        n_paises              = ('country_name', 'count'),
        n_con_recovery        = ('recovery_index', 'count'),
        recovery_index_medio  = ('recovery_index', 'mean'),
        recovery_index_mediana= ('recovery_index', 'median'),
        pct_sobre_100         = ('recovery_index', lambda x: (x >= 100).sum()),
        delta_medio_pp        = ('delta_vs_2019_pp', 'mean'),
    )
    .reset_index()
    .round(2)
)

regional['pct_recuperados'] = (
    (regional['pct_sobre_100'] / regional['n_con_recovery']) * 100
).round(1)

print("── Resumen regional del índice de recuperación ─────────────────────────")
print(regional.to_string(index=False))
print()

# ── H. Países sin recuperación (sin dato 2022-2023) ──────────────────────────
sin_recovery = recup[recup['recovery_index'].isna()][['country_name', 'region', 'valor_2019']]
print(f"── Países sin dato de recovery ({len(sin_recovery)}) ────────────────────────────")
print(sin_recovery.to_string(index=False))
print()

# ── Export ────────────────────────────────────────────────────────────────────
recup.to_csv(output_path, index=False)
regional.to_csv(output_reg, index=False)

print(f"Outputs exportados:")
print(f"  {output_path}")
print(f"  {output_reg}")
print(f"Shape recuperación: {recup.shape}")