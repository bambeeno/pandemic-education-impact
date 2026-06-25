# 02_serie_temporal.py
# Proyecto 3 — Pandemic Education Impact
# Objetivo: análisis de tendencia global y regional año a año (2015-2025)
# Herramientas nuevas: groupby + agg, rolling average, pivot por región

import pandas as pd
import os

# ── Rutas ──────────────────────────────────────────────────────────────────────
base_dir    = os.path.dirname(os.path.abspath(__file__))
input_path  = os.path.join(base_dir, '..', 'output', '01_pandemic_prep.csv')
output_path = os.path.join(base_dir, '..', 'output', '02_serie_temporal.csv')
output_regional = os.path.join(base_dir, '..', 'output', '02_serie_regional.csv')

# ── Carga ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(input_path)
print(f"Dataset cargado: {df.shape[0]:,} filas\n")

# ── Solo países válidos para análisis principal ────────────────────────────────
df_valid = df[df['flag_analisis_principal'] == True].copy()
print(f"Registros en análisis principal: {df_valid.shape[0]:,}")
print(f"Países: {df_valid['country_name'].nunique()}\n")

# ── A. Tendencia global año a año ─────────────────────────────────────────────
tendencia_global = df_valid.groupby('year').agg(
    n_paises       = ('value_pct_gdp', 'count'),
    media_global   = ('value_pct_gdp', 'mean'),
    mediana_global = ('value_pct_gdp', 'median'),
    std_global     = ('value_pct_gdp', 'std'),
    min_global     = ('value_pct_gdp', 'min'),
    max_global     = ('value_pct_gdp', 'max'),
).reset_index()

# Rolling average de 3 años (suaviza fluctuaciones)
tendencia_global['rolling_avg_3y'] = (
    tendencia_global['media_global']
    .rolling(window=3, center=True)
    .mean()
    .round(4)
)

tendencia_global = tendencia_global.round(4)
print("── Tendencia global año a año ──────────────────────────────────────────")
print(tendencia_global.to_string(index=False))
print()

# ── B. Variación interanual global ────────────────────────────────────────────
tendencia_global['var_interanual_pp'] = (
    tendencia_global['media_global'].diff().round(4)
)
tendencia_global['var_interanual_pct'] = (
    tendencia_global['media_global'].pct_change().mul(100).round(2)
)

print("── Variación interanual (puntos porcentuales y %) ──────────────────────")
print(tendencia_global[['year', 'media_global', 'var_interanual_pp', 'var_interanual_pct']].to_string(index=False))
print()

# ── C. Identificar el año de mayor caída y mayor recuperación ─────────────────
caida_max = tendencia_global.loc[tendencia_global['var_interanual_pp'].idxmin()]
recuperacion_max = tendencia_global.loc[tendencia_global['var_interanual_pp'].idxmax()]

print(f"Año de mayor caída:        {int(caida_max['year'])} "
        f"({caida_max['var_interanual_pp']:+.4f} pp)")
print(f"Año de mayor recuperación: {int(recuperacion_max['year'])} "
        f"({recuperacion_max['var_interanual_pp']:+.4f} pp)\n")

# ── D. Clasificación regional (por código de país — prefijo UN M.49) ──────────
# Asignación manual de región basada en country_code (ISO 3166-1 alpha-3)
regiones = {
    # América del Norte
    'USA': 'North America', 'CAN': 'North America', 'MEX': 'North America',
    # América Latina y Caribe
    'ARG': 'Latin America & Caribbean', 'BRA': 'Latin America & Caribbean',
    'BHS': 'Latin America & Caribbean', 'BLM': 'Latin America & Caribbean',
    'CHL': 'Latin America & Caribbean', 'COL': 'Latin America & Caribbean',
    'PER': 'Latin America & Caribbean', 'VEN': 'Latin America & Caribbean',
    'BOL': 'Latin America & Caribbean', 'ECU': 'Latin America & Caribbean',
    'PRY': 'Latin America & Caribbean', 'URY': 'Latin America & Caribbean',
    'CRI': 'Latin America & Caribbean', 'CUB': 'Latin America & Caribbean',
    'DOM': 'Latin America & Caribbean', 'GTM': 'Latin America & Caribbean',
    'HND': 'Latin America & Caribbean', 'JAM': 'Latin America & Caribbean',
    'NIC': 'Latin America & Caribbean', 'PAN': 'Latin America & Caribbean',
    'SLV': 'Latin America & Caribbean', 'TTO': 'Latin America & Caribbean',
    'HTI': 'Latin America & Caribbean', 'GUY': 'Latin America & Caribbean',
    'SUR': 'Latin America & Caribbean', 'BLZ': 'Latin America & Caribbean',
    'BRB': 'Latin America & Caribbean', 'ATG': 'Latin America & Caribbean',
    'DMA': 'Latin America & Caribbean', 'GRD': 'Latin America & Caribbean',
    'KNA': 'Latin America & Caribbean', 'LCA': 'Latin America & Caribbean',
    'VCT': 'Latin America & Caribbean',
    # Territorios del Caribe (dependientes pero reportados por UNESCO)
    'AIA': 'Latin America & Caribbean',  # Anguilla
    'ABW': 'Latin America & Caribbean',  # Aruba
    'BMU': 'Latin America & Caribbean',  # Bermuda
    'VGB': 'Latin America & Caribbean',  # British Virgin Islands
    'CYM': 'Latin America & Caribbean',  # Cayman Islands
    'CUW': 'Latin America & Caribbean',  # Curaçao
    'MSR': 'Latin America & Caribbean',  # Montserrat
    'PRI': 'Latin America & Caribbean',  # Puerto Rico
    'TCA': 'Latin America & Caribbean',  # Turks and Caicos Islands
    # Europa
    'DEU': 'Europe', 'FRA': 'Europe', 'GBR': 'Europe', 'ITA': 'Europe',
    'ESP': 'Europe', 'PRT': 'Europe', 'NLD': 'Europe', 'BEL': 'Europe',
    'SWE': 'Europe', 'NOR': 'Europe', 'DNK': 'Europe', 'FIN': 'Europe',
    'CHE': 'Europe', 'AUT': 'Europe', 'POL': 'Europe', 'CZE': 'Europe',
    'SVK': 'Europe', 'HUN': 'Europe', 'ROU': 'Europe', 'BGR': 'Europe',
    'GRC': 'Europe', 'HRV': 'Europe', 'SVN': 'Europe', 'EST': 'Europe',
    'LVA': 'Europe', 'LTU': 'Europe', 'IRL': 'Europe', 'LUX': 'Europe',
    'MLT': 'Europe', 'CYP': 'Europe', 'ISL': 'Europe', 'MKD': 'Europe',
    'ALB': 'Europe', 'SRB': 'Europe', 'BIH': 'Europe', 'MNE': 'Europe',
    'MDA': 'Europe', 'UKR': 'Europe', 'BLR': 'Europe', 'RUS': 'Europe',
    'GEO': 'Europe', 'ARM': 'Europe', 'AZE': 'Europe',
    'TUR': 'Europe',   # Türkiye
    'AND': 'Europe',   # Andorra
    'MCO': 'Europe',   # Monaco
    'SMR': 'Europe',   # San Marino
    # Asia Oriental y Pacífico
    'CHN': 'East Asia & Pacific', 'JPN': 'East Asia & Pacific',
    'KOR': 'East Asia & Pacific', 'AUS': 'East Asia & Pacific',
    'NZL': 'East Asia & Pacific', 'IDN': 'East Asia & Pacific',
    'MYS': 'East Asia & Pacific', 'PHL': 'East Asia & Pacific',
    'THA': 'East Asia & Pacific', 'VNM': 'East Asia & Pacific',
    'SGP': 'East Asia & Pacific', 'MMR': 'East Asia & Pacific',
    'KHM': 'East Asia & Pacific', 'LAO': 'East Asia & Pacific',
    'MNG': 'East Asia & Pacific', 'PNG': 'East Asia & Pacific',
    'FJI': 'East Asia & Pacific', 'TLS': 'East Asia & Pacific',
    'PRK': 'East Asia & Pacific', 'TWN': 'East Asia & Pacific',
    'BRN': 'East Asia & Pacific', 'WSM': 'East Asia & Pacific',
    'SLB': 'East Asia & Pacific', 'VUT': 'East Asia & Pacific',
    'TON': 'East Asia & Pacific', 'KIR': 'East Asia & Pacific',
    'FSM': 'East Asia & Pacific', 'PLW': 'East Asia & Pacific',
    'MHL': 'East Asia & Pacific', 'NRU': 'East Asia & Pacific',
    'TUV': 'East Asia & Pacific',
    'HKG': 'East Asia & Pacific',  # Hong Kong SAR
    'MAC': 'East Asia & Pacific',  # Macao SAR
    'COK': 'East Asia & Pacific',  # Cook Islands
    # Asia del Sur
    'IND': 'South Asia', 'PAK': 'South Asia', 'BGD': 'South Asia',
    'NPL': 'South Asia', 'LKA': 'South Asia', 'AFG': 'South Asia',
    'MDV': 'South Asia', 'BTN': 'South Asia',
    # Asia Central
    'KAZ': 'Central Asia', 'UZB': 'Central Asia', 'TKM': 'Central Asia',
    'KGZ': 'Central Asia', 'TJK': 'Central Asia',
    # Medio Oriente y África del Norte
    'SAU': 'Middle East & North Africa', 'IRN': 'Middle East & North Africa',
    'IRQ': 'Middle East & North Africa', 'SYR': 'Middle East & North Africa',
    'JOR': 'Middle East & North Africa', 'LBN': 'Middle East & North Africa',
    'ISR': 'Middle East & North Africa', 'PSE': 'Middle East & North Africa',
    'KWT': 'Middle East & North Africa', 'ARE': 'Middle East & North Africa',
    'QAT': 'Middle East & North Africa', 'BHR': 'Middle East & North Africa',
    'OMN': 'Middle East & North Africa', 'YEM': 'Middle East & North Africa',
    'EGY': 'Middle East & North Africa', 'LBY': 'Middle East & North Africa',
    'TUN': 'Middle East & North Africa', 'DZA': 'Middle East & North Africa',
    'MAR': 'Middle East & North Africa', 'MRT': 'Middle East & North Africa',
    'DJI': 'Middle East & North Africa',
    # África Subsahariana
    'NGA': 'Sub-Saharan Africa', 'ETH': 'Sub-Saharan Africa',
    'COD': 'Sub-Saharan Africa', 'TZA': 'Sub-Saharan Africa',
    'KEN': 'Sub-Saharan Africa', 'UGA': 'Sub-Saharan Africa',
    'GHA': 'Sub-Saharan Africa', 'MOZ': 'Sub-Saharan Africa',
    'MDG': 'Sub-Saharan Africa', 'CMR': 'Sub-Saharan Africa',
    'CIV': 'Sub-Saharan Africa', 'NER': 'Sub-Saharan Africa',
    'BFA': 'Sub-Saharan Africa', 'MLI': 'Sub-Saharan Africa',
    'MWI': 'Sub-Saharan Africa', 'ZMB': 'Sub-Saharan Africa',
    'SEN': 'Sub-Saharan Africa', 'SOM': 'Sub-Saharan Africa',
    'ZWE': 'Sub-Saharan Africa', 'GNB': 'Sub-Saharan Africa',
    'RWA': 'Sub-Saharan Africa', 'BDI': 'Sub-Saharan Africa',
    'BEN': 'Sub-Saharan Africa', 'TCD': 'Sub-Saharan Africa',
    'SDN': 'Sub-Saharan Africa', 'SSD': 'Sub-Saharan Africa',
    'ERI': 'Sub-Saharan Africa', 'CAF': 'Sub-Saharan Africa',
    'COG': 'Sub-Saharan Africa', 'GAB': 'Sub-Saharan Africa',
    'GNQ': 'Sub-Saharan Africa', 'STP': 'Sub-Saharan Africa',
    'AGO': 'Sub-Saharan Africa', 'NAM': 'Sub-Saharan Africa',
    'BWA': 'Sub-Saharan Africa', 'ZAF': 'Sub-Saharan Africa',
    'LSO': 'Sub-Saharan Africa', 'SWZ': 'Sub-Saharan Africa',
    'CPV': 'Sub-Saharan Africa', 'GMB': 'Sub-Saharan Africa',
    'GIN': 'Sub-Saharan Africa', 'SLE': 'Sub-Saharan Africa',
    'LBR': 'Sub-Saharan Africa', 'TGO': 'Sub-Saharan Africa',
    'COM': 'Sub-Saharan Africa', 'SYC': 'Sub-Saharan Africa',
    'MUS': 'Sub-Saharan Africa',
}
df_valid['region'] = df_valid['country_code'].map(regiones)

# Países sin región asignada
sin_region = df_valid[df_valid['region'].isna()]['country_name'].unique()
if len(sin_region) > 0:
    print(f"Países sin región asignada ({len(sin_region)}): {list(sin_region)}\n")

# ── E. Tendencia regional año a año ───────────────────────────────────────────
df_con_region = df_valid[df_valid['region'].notna()].copy()

tendencia_regional = df_con_region.groupby(['region', 'year']).agg(
    n_paises     = ('value_pct_gdp', 'count'),
    media        = ('value_pct_gdp', 'mean'),
    mediana      = ('value_pct_gdp', 'median'),
).reset_index().round(4)

print("── Tendencia regional (primeras filas) ─────────────────────────────────")
print(tendencia_regional.head(20).to_string(index=False))
print()

# ── F. Pivot: media por región × año (tabla de calor) ─────────────────────────
pivot_regional = tendencia_regional.pivot(
    index='region', columns='year', values='media'
).round(4)

print("── Pivot región × año (media gasto % PBI) ──────────────────────────────")
print(pivot_regional.to_string())
print()

# ── G. Variación 2019 → 2020 por región ───────────────────────────────────────
if 2019 in pivot_regional.columns and 2020 in pivot_regional.columns:
    pivot_regional['delta_2019_2020'] = (
        pivot_regional[2020] - pivot_regional[2019]
    ).round(4)
    print("── Caída pandémica por región (2019 → 2020) ────────────────────────────")
    print(pivot_regional[['delta_2019_2020']].sort_values('delta_2019_2020').to_string())
    print()

# ── Export ────────────────────────────────────────────────────────────────────
tendencia_global.to_csv(output_path, index=False)
tendencia_regional.to_csv(output_regional, index=False)

# También guardamos el df_valid con región para los scripts siguientes
df_valid.to_csv(
    os.path.join(base_dir, '..', 'output', '02_prep_con_region.csv'),
    index=False
)

print(f"Outputs exportados:")
print(f"  {output_path}")
print(f"  {output_regional}")
print(f"  output/02_prep_con_region.csv")
