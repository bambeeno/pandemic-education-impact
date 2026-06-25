# 01_preparacion.py
# Proyecto 3 — Pandemic Education Impact
# Objetivo: filtrar el dataset limpio del P2 al rango 2015-2025,
# validar cobertura pre/durante/post pandemia y dejar listo para análisis.

import pandas as pd
import os

# ── Rutas ──────────────────────────────────────────────────────────────────────
base_dir = os.path.dirname(os.path.abspath(__file__))
input_path  = os.path.join(base_dir, '..', 'data', '02_education_spending_clean.csv')
output_path = os.path.join(base_dir, '..', 'output', '01_pandemic_prep.csv')
os.makedirs(os.path.join(base_dir, '..', 'output'), exist_ok=True)

# ── Carga ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(input_path)
print(f"Dataset cargado: {df.shape[0]:,} filas, {df.shape[1]} columnas")
print(f"Columnas: {df.columns.tolist()}\n")

# ── Filtro temporal 2015-2025 ──────────────────────────────────────────────────
df = df[df['year'].between(2015, 2025)].copy()
print(f"Después de filtro 2015-2025: {df.shape[0]:,} filas")
print(f"Países únicos: {df['country_name'].nunique()}")
print(f"Años cubiertos: {sorted(df['year'].unique())}\n")

# ── Clasificación de períodos ──────────────────────────────────────────────────
def clasificar_periodo(year):
    if year <= 2019:
        return 'pre_pandemic'
    elif year <= 2021:
        return 'pandemic'
    else:
        return 'recovery'

df['period'] = df['year'].apply(clasificar_periodo)
print("Distribución por período:")
print(df['period'].value_counts().sort_index())
print()

# ── Cobertura por país: datos disponibles en cada período ─────────────────────
cobertura = df.groupby('country_name')['period'].apply(
    lambda x: set(x.tolist())
).reset_index()
cobertura.columns = ['country_name', 'periods_available']

cobertura['tiene_pre']      = cobertura['periods_available'].apply(lambda x: 'pre_pandemic' in x)
cobertura['tiene_pandemic'] = cobertura['periods_available'].apply(lambda x: 'pandemic' in x)
cobertura['tiene_recovery'] = cobertura['periods_available'].apply(lambda x: 'recovery' in x)

print("Cobertura por período:")
print(f"  Con datos pre-pandemia (2015-2019):  {cobertura['tiene_pre'].sum()} países")
print(f"  Con datos pandemia (2020-2021):       {cobertura['tiene_pandemic'].sum()} países")
print(f"  Con datos recuperación (2022+):       {cobertura['tiene_recovery'].sum()} países")
print()

# ── Países con cobertura completa (los tres períodos) ─────────────────────────
completos = cobertura[
    cobertura['tiene_pre'] & cobertura['tiene_pandemic'] & cobertura['tiene_recovery']
]
print(f"Países con los 3 períodos disponibles: {len(completos)}")

# ── Países con pandemia pero sin recuperación (lag de reporte) ────────────────
sin_recovery = cobertura[
    cobertura['tiene_pre'] & cobertura['tiene_pandemic'] & ~cobertura['tiene_recovery']
]
print(f"Países con pre + pandemia pero sin recuperación aún: {len(sin_recovery)}")
print()

# ── Flag de inclusión en análisis principal ────────────────────────────────────
# Criterio: debe tener dato en 2019 (baseline) y al menos uno en 2020 o 2021
tiene_2019 = df[df['year'] == 2019]['country_name'].unique()
tiene_pandemia = df[df['year'].isin([2020, 2021])]['country_name'].unique()

paises_validos = set(tiene_2019) & set(tiene_pandemia)
print(f"Países con dato en 2019 Y al menos un año pandémico: {len(paises_validos)}")

df['flag_analisis_principal'] = df['country_name'].isin(paises_validos)

# ── Resumen de flags heredados del P2 ─────────────────────────────────────────
flag_cols = [c for c in df.columns if c.startswith('flag_')]
print(f"\nFlags disponibles: {flag_cols}")
for flag in flag_cols:
    if flag in df.columns:
        n = df[flag].sum()
        print(f"  {flag}: {n} registros marcados")

# ── Export ────────────────────────────────────────────────────────────────────
df.to_csv(output_path, index=False)
print(f"\nOutput exportado: {output_path}")
print(f"Shape final: {df.shape}")