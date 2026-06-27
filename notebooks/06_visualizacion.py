# 06_visualizacion.py
# Proyecto 3 — Pandemic Education Impact
# Objetivo: 6 visualizaciones con storytelling — descriptivas y analíticas

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# ── Rutas ──────────────────────────────────────────────────────────────────────
base_dir = os.path.dirname(os.path.abspath(__file__))
out_dir  = os.path.join(base_dir, '..', 'output')

# ── Carga ──────────────────────────────────────────────────────────────────────
serie     = pd.read_csv(os.path.join(out_dir, '02_serie_temporal.csv'))
regional  = pd.read_csv(os.path.join(out_dir, '02_serie_regional.csv'))
evento    = pd.read_csv(os.path.join(out_dir, '03_evento.csv'))
ev_reg    = pd.read_csv(os.path.join(out_dir, '03_evento_regional.csv'))
recup     = pd.read_csv(os.path.join(out_dir, '04_recuperacion.csv'))
recup_reg = pd.read_csv(os.path.join(out_dir, '04_recuperacion_regional.csv'))

# ── Paleta y estilo global ─────────────────────────────────────────────────────
PALETTE_REGION = {
    'Central Asia':               '#E67E22',
    'East Asia & Pacific':        '#5DADE2',
    'Europe':                     '#48C9B0',
    'Latin America & Caribbean':  '#EC7063',
    'Middle East & North Africa': '#C39BD3',
    'North America':              '#58D68D',
    'South Asia':                 '#F7DC6F',
    'Sub-Saharan Africa':         '#AAB7B8',
}

BG_COLOR       = '#1C1C2E'   # fondo oscuro principal
BG_AXES        = '#252540'   # fondo de ejes
COLOR_BASELINE = '#A9CCE3'   # azul claro para líneas de referencia
COLOR_SHOCK    = '#EC7063'   # rojo suave
COLOR_RECOVERY = '#58D68D'   # verde suave
COLOR_BAND     = '#5DADE2'   # azul medio para banda std
COLOR_LINE     = '#85C1E9'   # azul claro para línea principal
TEXT_PRIMARY   = '#ECF0F1'   # blanco hueso — texto principal
TEXT_SECONDARY = '#BDC3C7'   # gris claro — texto secundario
GRID_COLOR     = '#3D3D5C'   # gris azulado para grilla

plt.rcParams.update({
    'font.family':           'DejaVu Sans',
    'figure.facecolor':      BG_COLOR,
    'axes.facecolor':        BG_AXES,
    'axes.edgecolor':        GRID_COLOR,
    'axes.labelcolor':       TEXT_PRIMARY,
    'axes.titlecolor':       TEXT_PRIMARY,
    'xtick.color':           TEXT_SECONDARY,
    'ytick.color':           TEXT_SECONDARY,
    'text.color':            TEXT_PRIMARY,
    'grid.color':            GRID_COLOR,
    'grid.alpha':            0.4,
    'grid.linestyle':        '--',
    'axes.spines.top':       False,
    'axes.spines.right':     False,
    'axes.spines.left':      True,
    'axes.spines.bottom':    True,
    'legend.facecolor':      '#2C2C4A',
    'legend.edgecolor':      GRID_COLOR,
    'legend.labelcolor':     TEXT_PRIMARY,
    'figure.dpi':            150,
})

def guardar(fig, nombre):
    path = os.path.join(out_dir, nombre)
    fig.savefig(path, bbox_inches='tight', dpi=150, facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  Guardado: {nombre}")

# ══════════════════════════════════════════════════════════════════════════════
# BLOQUE 1 — DESCRIPTIVOS
# ══════════════════════════════════════════════════════════════════════════════

# ── Gráfico 1: Serie temporal global ──────────────────────────────────────────
print("\n── Gráfico 1: Serie temporal global")

s = serie[serie['year'] <= 2023].copy()

fig, ax = plt.subplots(figsize=(13, 6))

# Bandas de período
ax.axvspan(2015,   2019.5, alpha=0.08, color='#A9CCE3')
ax.axvspan(2019.5, 2021.5, alpha=0.12, color=COLOR_SHOCK)
ax.axvspan(2021.5, 2023,   alpha=0.08, color=COLOR_RECOVERY)

# Banda std
ax.fill_between(
    s['year'],
    s['media_global'] - s['std_global'],
    s['media_global'] + s['std_global'],
    alpha=0.18, color=COLOR_BAND, label='±1 std dev'
)

# Línea principal
ax.plot(s['year'], s['media_global'], color=COLOR_LINE,
        linewidth=2.5, marker='o', markersize=5, zorder=5, label='Global mean')

# Rolling average
ax.plot(s['year'], s['rolling_avg_3y'], color=COLOR_LINE,
        linewidth=1.2, linestyle='--', alpha=0.5, label='3-year rolling avg')

# Línea baseline 2019
baseline_val = s[s['year'] == 2019]['media_global'].values[0]
ax.axhline(baseline_val, color=COLOR_BASELINE, linewidth=0.9,
           linestyle=':', alpha=0.8, label=f'2019 baseline ({baseline_val:.2f}%)')

# Etiquetas de períodos
ymin = s['media_global'].min() - s['std_global'].max() - 0.3
ax.text(2017,   ymin, 'BASELINE\n2015–2019', ha='center',
        fontsize=8, color=TEXT_SECONDARY, alpha=0.85)
ax.text(2020.5, ymin, 'SHOCK\n2020–2021', ha='center',
        fontsize=8, color=COLOR_SHOCK, alpha=0.9)
ax.text(2022.5, ymin, 'RECOVERY\n2022–2023', ha='center',
        fontsize=8, color=COLOR_RECOVERY, alpha=0.9)

# Anotación pico 2020
peak = s[s['year'] == 2020]['media_global'].values[0]
ax.annotate(
    f'+0.31 pp vs 2019\n(denominator effect)',
    xy=(2020, peak), xytext=(2020.4, peak + 0.32),
    fontsize=8, color=COLOR_SHOCK,
    arrowprops=dict(arrowstyle='->', color=COLOR_SHOCK, lw=1.2)
)

# Anotación caída 2023
val_2023 = s[s['year'] == 2023]['media_global'].values[0]
ax.annotate(
    f'Worst year: {val_2023:.2f}%\n(−0.35 pp vs 2022)',
    xy=(2023, val_2023), xytext=(2021.8, val_2023 - 0.42),
    fontsize=8, color=COLOR_RECOVERY,
    arrowprops=dict(arrowstyle='->', color=COLOR_RECOVERY, lw=1.2)
)

ax.set_title(
    'Global Education Spending (% of GDP) — 2015 to 2023\n'
    'The real cut came after the pandemic, not during it',
    fontsize=13, fontweight='bold', pad=15, color=TEXT_PRIMARY
)
ax.set_xlabel('Year', fontsize=10, color=TEXT_SECONDARY)
ax.set_ylabel('Government expenditure on education\n(% of GDP)', fontsize=10, color=TEXT_SECONDARY)
ax.set_xticks(s['year'])
ax.legend(fontsize=8, loc='upper right')
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))

fig.tight_layout()
guardar(fig, 'viz_01_serie_temporal_global.png')

# ── Gráfico 2: Heatmap regional ───────────────────────────────────────────────
print("── Gráfico 2: Heatmap regional")

pivot = regional[regional['year'] <= 2023].pivot(
    index='region', columns='year', values='media'
).round(2)

pivot = pivot.loc[pivot.mean(axis=1).sort_values(ascending=False).index]

fig, ax = plt.subplots(figsize=(14, 6))
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_AXES)

sns.heatmap(
    pivot,
    ax=ax,
    cmap='YlOrRd',
    annot=True,
    fmt='.2f',
    linewidths=0.5,
    linecolor=BG_COLOR,
    cbar_kws={'label': '% of GDP', 'shrink': 0.8},
    annot_kws={'size': 8, 'color': '#1C1C2E', 'fontweight': 'bold'}
)

# Colorbar texto
ax.collections[0].colorbar.ax.yaxis.label.set_color(TEXT_PRIMARY)
ax.collections[0].colorbar.ax.tick_params(colors=TEXT_SECONDARY)

# Líneas de período
for x, label, color in [
    (5.5, '← SHOCK →',    COLOR_SHOCK),
    (7.5, '← RECOVERY →', COLOR_RECOVERY)
]:
    ax.axvline(x, color=TEXT_PRIMARY, linewidth=2, alpha=0.6)
    ax.text(x + 0.08, -0.5, label, fontsize=7.5,
            color=color, fontweight='bold')

ax.set_title(
    'Education Spending by Region and Year (% of GDP)\n'
    'Central Asia recovered strongly; Latin America fell the most',
    fontsize=13, fontweight='bold', pad=15, color=TEXT_PRIMARY
)
ax.set_xlabel('Year', fontsize=10, color=TEXT_SECONDARY)
ax.set_ylabel('', fontsize=10)
ax.tick_params(axis='y', labelsize=9, colors=TEXT_SECONDARY)
ax.tick_params(axis='x', labelsize=9, colors=TEXT_SECONDARY)

fig.tight_layout()
guardar(fig, 'viz_02_heatmap_regional.png')

# ── Gráfico 3: Recovery index por región (boxplot) ────────────────────────────
print("── Gráfico 3: Recovery index por región")

recup_clean = recup[recup['recovery_index'].notna()].copy()

orden = (
    recup_clean.groupby('region')['recovery_index']
    .median()
    .sort_values(ascending=True)
    .index.tolist()
)

fig, ax = plt.subplots(figsize=(13, 7))

bp = ax.boxplot(
    [recup_clean[recup_clean['region'] == r]['recovery_index'].values for r in orden],
    vert=False,
    patch_artist=True,
    notch=False,
    widths=0.55,
    medianprops=dict(color=BG_COLOR, linewidth=2.5),
    whiskerprops=dict(linewidth=1.2, color=TEXT_SECONDARY),
    capprops=dict(linewidth=1.2, color=TEXT_SECONDARY),
    flierprops=dict(marker='o', markersize=4, alpha=0.5,
                    markerfacecolor=TEXT_SECONDARY, markeredgecolor='none')
)

for patch, region in zip(bp['boxes'], orden):
    patch.set_facecolor(PALETTE_REGION.get(region, '#95A5A6'))
    patch.set_alpha(0.85)
    patch.set_edgecolor(TEXT_SECONDARY)

ax.axvline(100, color=TEXT_PRIMARY, linewidth=1.8,
           linestyle='--', alpha=0.7, label='2019 baseline (index = 100)')

ax.set_yticks(range(1, len(orden) + 1))
ax.set_yticklabels(orden, fontsize=9, color=TEXT_SECONDARY)
ax.set_xlabel('Recovery Index (100 = 2019 level)', fontsize=10, color=TEXT_SECONDARY)
ax.set_title(
    'Education Spending Recovery by Region\n'
    'South Asia leads; Latin America & Europe still below pre-pandemic levels',
    fontsize=13, fontweight='bold', pad=15, color=TEXT_PRIMARY
)
ax.legend(fontsize=9)
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f'))

fig.tight_layout()
guardar(fig, 'viz_03_recovery_index_region.png')

# ══════════════════════════════════════════════════════════════════════════════
# BLOQUE 2 — ANALÍTICOS
# ══════════════════════════════════════════════════════════════════════════════

# ── Gráfico 4: Distribución del impacto pandémico por región ──────────────────
print("── Gráfico 4: Distribución del impacto pandémico por región")

orden_impacto = ['caida_fuerte', 'caida_leve', 'estable', 'aumento_leve', 'aumento_fuerte']
colores_impacto = {
    'caida_fuerte':   '#C0392B',
    'caida_leve':     '#E67E22',
    'estable':        '#5D6D7E',
    'aumento_leve':   '#58D68D',
    'aumento_fuerte': '#1ABC9C',
}
labels_impacto = {
    'caida_fuerte':   'Strong drop (>−0.5pp)',
    'caida_leve':     'Mild drop (−0.5 to −0.1pp)',
    'estable':        'Stable (±0.1pp)',
    'aumento_leve':   'Mild increase (+0.1 to +0.5pp)',
    'aumento_fuerte': 'Strong increase (>+0.5pp)',
}

tabla = (
    evento.groupby(['region', 'impacto_shock'])
    .size()
    .unstack(fill_value=0)
    .reindex(columns=orden_impacto, fill_value=0)
)

tabla['total'] = tabla.sum(axis=1)
for col in orden_impacto:
    tabla[col + '_pct'] = tabla[col] / tabla['total'] * 100

orden_reg = (
    (tabla['caida_fuerte_pct'] + tabla['caida_leve_pct'])
    .sort_values(ascending=True).index.tolist()
)

fig, ax = plt.subplots(figsize=(13, 7))

bottom = pd.Series([0.0] * len(orden_reg), index=orden_reg)
for cat in orden_impacto:
    vals = tabla.loc[orden_reg, cat + '_pct']
    ax.barh(orden_reg, vals, left=bottom,
            color=colores_impacto[cat], label=labels_impacto[cat],
            edgecolor=BG_COLOR, linewidth=0.8)
    for i, (v, b) in enumerate(zip(vals, bottom)):
        if v > 8:
            ax.text(b + v / 2, i, f'{v:.0f}%',
                    ha='center', va='center', fontsize=7.5,
                    color='white', fontweight='bold')
    bottom += vals

ax.axvline(50, color=TEXT_SECONDARY, linewidth=0.8, linestyle=':', alpha=0.5)
ax.set_xlabel('Share of countries (%)', fontsize=10, color=TEXT_SECONDARY)
ax.set_title(
    'Pandemic Shock Impact by Region — Share of Countries per Category\n'
    'Most countries saw an apparent increase due to the denominator effect',
    fontsize=13, fontweight='bold', pad=15, color=TEXT_PRIMARY
)
ax.legend(loc='lower right', fontsize=8, framealpha=0.9)
ax.set_xlim(0, 100)
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
ax.tick_params(axis='y', labelsize=9, colors=TEXT_SECONDARY)
ax.tick_params(axis='x', colors=TEXT_SECONDARY)

fig.tight_layout()
guardar(fig, 'viz_04_impacto_por_region.png')

# ── Gráfico 5: Top/Bottom 15 países por recovery index ────────────────────────
print("── Gráfico 5: Top/Bottom países por recovery index")

excluir = ['Somalia', 'Vanuatu', 'Mauritania']
rc = recup_clean[~recup_clean['country_name'].isin(excluir)].copy()

top15    = rc.nlargest(15, 'recovery_index')
bottom15 = rc.nsmallest(15, 'recovery_index')
combined = pd.concat([top15, bottom15]).drop_duplicates()
combined = combined.sort_values('recovery_index', ascending=True)

fig, ax = plt.subplots(figsize=(13, 12))

colors = [PALETTE_REGION.get(r, '#95A5A6') for r in combined['region']]

bars = ax.barh(
    combined['country_name'],
    combined['recovery_index'],
    color=colors,
    edgecolor=BG_COLOR,
    linewidth=0.5,
    height=0.7
)

ax.axvline(100, color=TEXT_PRIMARY, linewidth=1.8,
           linestyle='--', alpha=0.8, label='2019 baseline', zorder=5)

for bar, val in zip(bars, combined['recovery_index']):
    ax.text(
        val + 1.5 if val < 100 else val - 1.5,
        bar.get_y() + bar.get_height() / 2,
        f'{val:.1f}',
        va='center',
        ha='left' if val < 100 else 'right',
        fontsize=7.5,
        color=TEXT_PRIMARY,
        fontweight='bold'
    )

handles = [
    mpatches.Patch(color=c, label=r)
    for r, c in PALETTE_REGION.items()
    if r in combined['region'].values
]
ax.legend(handles=handles, fontsize=8, loc='lower right',
          title='Region', title_fontsize=8)

ax.set_xlabel('Recovery Index (100 = 2019 level)', fontsize=10, color=TEXT_SECONDARY)
ax.set_title(
    'Top & Bottom Countries by Education Spending Recovery Index\n'
    '(Outliers excluded: Vanuatu, Mauritania, Somalia)\n'
    'Suriname, Lebanon and Nicaragua remain critically lagged',
    fontsize=12, fontweight='bold', pad=15, color=TEXT_PRIMARY
)
ax.tick_params(axis='y', labelsize=8.5, colors=TEXT_SECONDARY)
ax.tick_params(axis='x', colors=TEXT_SECONDARY)

fig.tight_layout()
guardar(fig, 'viz_05_top_bottom_recovery.png')

# ── Gráfico 6: Scatter baseline vs delta shock ────────────────────────────────
print("── Gráfico 6: Scatter baseline vs delta shock")

ev = evento[evento['delta_shock_pp'].notna()].copy()
excluir_sc = ['Marshall Islands', 'Kiribati',
              'China, Macao Special Administrative Region']
ev = ev[~ev['country_name'].isin(excluir_sc)]

fig, ax = plt.subplots(figsize=(13, 8))

for region, group in ev.groupby('region'):
    ax.scatter(
        group['baseline_mean'],
        group['delta_shock_pp'],
        color=PALETTE_REGION.get(region, '#95A5A6'),
        alpha=0.80,
        s=60,
        label=region,
        edgecolors=BG_COLOR,
        linewidth=0.5
    )

ax.axhline(0, color=TEXT_PRIMARY, linewidth=1.2,
           linestyle='--', alpha=0.6, label='No change')
ax.axvline(ev['baseline_mean'].mean(), color=TEXT_SECONDARY,
           linewidth=0.8, linestyle=':', alpha=0.5,
           label=f'Global baseline mean ({ev["baseline_mean"].mean():.2f}%)')

# Etiquetas de cuadrantes
for x, y, txt in [
    (6.5,  1.8, 'High spenders\nthat increased'),
    (1.8,  1.8, 'Low spenders\nthat increased'),
    (6.5, -1.2, 'High spenders\nthat cut'),
    (1.8, -1.2, 'Low spenders\nthat cut'),
]:
    ax.text(x, y, txt, fontsize=7.5, color=TEXT_SECONDARY,
            alpha=0.7, ha='center')

# Anotaciones de casos notables
anotaciones = {
    'Timor-Leste':  (-0.3, -0.25),
    'Suriname':     (-0.3, -0.25),
    'Ethiopia':     (+0.1, -0.18),
    'Sierra Leone': (+0.2, +0.18),
    'Cabo Verde':   (+0.2, +0.15),
    'Norway':       (+0.2, +0.10),
}
for _, row in ev[ev['country_name'].isin(anotaciones.keys())].iterrows():
    dx, dy = anotaciones[row['country_name']]
    ax.annotate(
        row['country_name'],
        xy=(row['baseline_mean'], row['delta_shock_pp']),
        xytext=(row['baseline_mean'] + dx, row['delta_shock_pp'] + dy),
        fontsize=7.5, color=TEXT_PRIMARY,
        arrowprops=dict(arrowstyle='->', color=TEXT_SECONDARY, lw=0.9)
    )

ax.set_xlabel('Baseline spending 2015–2019 (% of GDP)', fontsize=10, color=TEXT_SECONDARY)
ax.set_ylabel('Change during pandemic shock (pp)', fontsize=10, color=TEXT_SECONDARY)
ax.set_title(
    'Pre-Pandemic Spending Level vs. Pandemic Shock Response\n'
    'Higher spenders were not necessarily more resilient',
    fontsize=13, fontweight='bold', pad=15, color=TEXT_PRIMARY
)
ax.legend(fontsize=8, loc='upper right', framealpha=0.9)
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%+.1f'))
ax.tick_params(colors=TEXT_SECONDARY)

fig.tight_layout()
guardar(fig, 'viz_06_scatter_baseline_vs_shock.png')

print("\nTodas las visualizaciones generadas.")