# My Ideal City — Île-de-France Explorer

An interactive tool for exploring quality-of-life scores across all communes and train stations in Île-de-France.

## Live Site

👉 **[https://lattamatic.github.io/My-Ideal-City/](https://lattamatic.github.io/My-Ideal-City/)**

## What's Inside

### Dashboards

| Page | Description |
|---|---|
| **Find Cities** | Choropleth map of all IDF communes coloured by quality-of-life score. Includes a live train line overlay fetched from the IDFM open data API. |
| **Find Train** | Per-line breakdown of RER/Transilien station scores — all data embedded, no external calls. |

### Data

| File | Description |
|---|---|
| `data/ville_ideale_full.csv` | Merged dataset — 71 real scraped scores + 1 195 synthetic scores for all IDF communes |
| `data/ville_ideale_idf.csv` | Real scraped data only |
| `data/communes_idf.csv` | Master commune list sourced from the French geo API |
| `data/ville_ideal_geojson.geojson` | Commune boundary polygons for Île-de-France |

### Scripts

| File | Description |
|---|---|
| `scraping/ville_ideale_scraper.py` | Scrapes quality-of-life scores from ville-ideale.fr |
| `scraping/rebuild_checkpoint.py` | Rebuilds the scraper checkpoint from an existing CSV |
| `viz/dashboard.py` | Reads the CSV + GeoJSON and generates `dashboard.html` |

## How to Regenerate the Map

```bash
# 1. Scrape scores (resumes from checkpoint.txt if interrupted)
python scraping/ville_ideale_scraper.py

# 2. Rebuild the dashboard HTML
python viz/dashboard.py
```

The train station HTML is self-contained and does not need to be regenerated unless the underlying data changes.

## Data Sources

- Quality-of-life scores: [ville-ideale.fr](https://www.ville-ideale.fr)
- Commune boundaries: [geo.api.gouv.fr](https://geo.api.gouv.fr)
- Live train lines: [IDFM Open Data API](https://data.iledefrance-mobilites.fr)

## Legal & Attribution

Quality-of-life scores are sourced from [www.ville-ideale.fr](https://www.ville-ideale.fr) and reproduced in accordance with their terms of use (source attribution + hyperlink provided). This project is a **non-commercial educational prototype** — the data is not resold or passed off as original. Only 71 cities have real scraped data; the remaining ~1,195 communes use synthetic scores generated for prototyping purposes only.

All dashboards display the attribution: *"Source : www.ville-ideale.fr"* with a direct hyperlink as required.
