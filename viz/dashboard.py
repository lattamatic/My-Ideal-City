#!/usr/bin/env python3
"""
Interactive Choropleth Map — Île-de-France quality of life scores.

SETUP:
    pip install pandas plotly

FILES NEEDED (same folder):
    ville_ideale_idf.csv
    ville_ideal_geojson.geojson

RUN:
    python dashboard.py
"""

import json
import re
import unicodedata
import pandas as pd
import plotly.graph_objects as go

CRITERIA = [
    "Environnement", "Transports", "Sécurité", "Santé",
    "Sports et loisirs", "Culture", "Enseignement", "Commerces", "Qualité de vie",
]

STATIC_OVERVIEW = (
    "Les habitants apprécient la proximité des transports et des commerces. "
    "Quelques points d'amélioration concernant les espaces verts. "
    "Vue d'ensemble positive avec un bon potentiel de développement."
)

# ── Slug → URL ─────────────────────────────────────────────────────────────────
def city_url(slug: str) -> str:
    return f"https://www.ville-ideale.fr/{slug}"

# ── Load & clean CSV ───────────────────────────────────────────────────────────
df = pd.read_csv("ville_ideale_idf.csv", encoding="utf-8-sig")
df = df[df["Nom"].notna()].copy()

for col in CRITERIA:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df[df[CRITERIA].notna().any(axis=1)].copy()
df["Note globale"] = df[CRITERIA].mean(axis=1).round(2)
df["Code INSEE"]   = df["Slug"].str.extract(r"_(\d{5})$").iloc[:, 0].str.zfill(5)
df = df[df["Code INSEE"].notna()].drop_duplicates(subset="Code INSEE").copy()
df["URL"] = df["Slug"].apply(city_url)

print(f"Cities with scores: {len(df)}")

# ── Load GeoJSON ───────────────────────────────────────────────────────────────
with open("ville_ideal_geojson.geojson", encoding="utf-8") as f:
    geojson = json.load(f)

for feat in geojson["features"]:
    feat["properties"]["com"] = str(feat["properties"]["com"]).zfill(5)

# ── Hover builder (plain text only) ───────────────────────────────────────────
def make_hover(row, active_col):
    lines = [
        f"{row['Nom']}",
        f"{row['Département']}",
        f"🔗 {row['URL']}",
        f"",
        f"Note globale : {row['Note globale']:.2f} / 10",
        f"──────────────────────",
    ]
    for c in CRITERIA:
        v = row[c]
        if pd.notna(v):
            marker = "▶" if c == active_col else " "
            lines.append(f"{marker} {c} : {v:.1f}")
    lines += [
        f"──────────────────────",
        f"Vue d'ensemble :",
        f"{STATIC_OVERVIEW}",
    ]
    return "<br>".join(lines)

# ── Build one trace per criterion ──────────────────────────────────────────────
all_columns = ["Note globale"] + CRITERIA
traces = []

for i, col in enumerate(all_columns):
    hover_texts = [make_hover(row, col) for _, row in df.iterrows()]

    traces.append(go.Choroplethmapbox(
        geojson=geojson,
        locations=df["Code INSEE"].tolist(),
        featureidkey="properties.com",
        z=df[col].tolist(),
        zmin=0,
        zmax=10,
        colorscale="RdYlGn",
        marker_opacity=0.8,
        marker_line_width=0.5,
        marker_line_color="white",
        colorbar=dict(
            title=dict(text="Note /10"),
            tickvals=[0, 2, 4, 6, 8, 10],
            ticktext=["0", "2", "4", "6", "8", "10"],
            thickness=16,
            len=0.6,
        ),
        text=hover_texts,
        hovertemplate="%{text}<extra></extra>",
        visible=(i == 0),
        name=col,
    ))

# ── Dropdown buttons ───────────────────────────────────────────────────────────
buttons = []
for i, col in enumerate(all_columns):
    visibility = [j == i for j in range(len(all_columns))]
    buttons.append(dict(
        label=col,
        method="update",
        args=[
            {"visible": visibility},
            {"title": f"Île-de-France — {col} par commune (ville-ideale.fr)"},
        ],
    ))

# ── Layout ─────────────────────────────────────────────────────────────────────
fig = go.Figure(data=traces)

fig.update_layout(
    mapbox=dict(
        style="carto-positron",
        center={"lat": 48.8566, "lon": 2.3522},
        zoom=9,
    ),
    updatemenus=[dict(
        buttons=buttons,
        direction="down",
        x=0.01,
        xanchor="left",
        y=0.99,
        yanchor="top",
        bgcolor="white",
        bordercolor="#ccc",
        borderwidth=1,
        font=dict(size=13),
        showactive=True,
    )],
    annotations=[dict(
        text="Critère :",
        x=0.01,
        xanchor="left",
        xref="paper",
        y=1.06,
        yanchor="top",
        yref="paper",
        showarrow=False,
        font=dict(size=13),
    )],
    title=dict(
        text="Île-de-France — Note globale par commune (ville-ideale.fr)",
        x=0.5,
        font=dict(size=16),
    ),
    margin={"r": 0, "t": 80, "l": 0, "b": 0},
    height=800,
)

fig.show()
