# Coastal tourism in Australia – Vega-Lite starter kit

Thirteen working Vega-Lite (v5) specs, one per idiom, plus a page that shows them all.

**Every number in `data/` is made up.** It exists only so the charts render while you gather real data. Replace each CSV with real figures, keeping the same column names, and the charts will update. The one real file is `data/aus_states.topojson`: state boundaries simplified from ABS data via the `rowanhogan/australian-states` GitHub repo.

## Run it

The page loads specs and CSVs with `fetch`, which browsers block when you double-click a local HTML file. Use a local web server instead:

- **VS Code:** install the *Live Server* extension, right-click `index.html`, then choose *Open with Live Server*.
- **Terminal:** run `python -m http.server` in this folder, then open http://localhost:8000.
- **GitHub Pages:** push the folder to a repo and turn on Pages. The relative `data/...` paths keep working.

## What's in each spec

| Spec | Idiom | Data file | Vega-Lite techniques worth studying |
|---|---|---|---|
| `01_choropleth` | Choropleth map | regions.csv + aus_states.topojson | aggregate, `lookup` a geometry into your data, `shape` channel, equal-area projection |
| `02_proportional_symbols` | Proportional symbol map | regions.csv + aus_states.topojson | layered basemap, `longitude`/`latitude` channels, size scale, legend-bound selection |
| `03_parallel_coordinates` | Parallel coordinates | regions.csv | `fold`, `joinaggregate` min/max normalisation, `window` row ids, `detail` channel |
| `04_dumbbell` | Dumbbell chart | regions.csv | `fold` wide to long, layered line + circle, sorting by an aggregate |
| `05_heatmap` | Heatmap | monthly_regions.csv | rect marks, indexing each row to its own mean, diverging scale with `domainMid` |
| `06_cycle_plot` | Cycle plot | arrivals_monthly.csv | `facet` by month, layered line + mean rule |
| `07_radial` | Radial (polar area) chart | reef_monthly.csv | arc marks, `theta`/`theta2` in radians with `scale: null`, sqrt radius scale |
| `08_streamgraph` | Streamgraph | arrivals_monthly.csv | area mark with `stack: "center"`, `datetime()` from year/month columns, `order` channel |
| `09_waffle` | Waffle chart | marine_sectors.csv | `sequence()` + `flatten` to make one row per square, modulo maths for the grid |
| `10_marimekko` | Marimekko (mosaic) chart | regions.csv | two `stack` transforms with `normalize`, `x`/`x2`/`y`/`y2` rects |
| `11_jitter_strip` | Jittered strip plot | regions.csv | `yOffset` channel, deterministic pseudo-random jitter, labelling top values with `rank` |
| `12_slope` | Slope chart | regions.csv | `fold` two years into one column, direction calculated for colour, end labels |
| `13_flow_map` | Flow map | flows.csv + aus_states.topojson | rule marks with `longitude2`/`latitude2`, `window` rank to thin the lines, halo text layer |

Each spec's `description` field says which marks and channels it uses and why. Adapt those notes for your write-up.

### Three idioms were swapped
Vega-Lite has no layout for treemaps, Sankey diagrams or true beeswarms, which need full Vega. The kit uses these substitutes:

- **Waffle chart instead of treemap.** It still shows part-to-whole for the marine economy.
- **Marimekko chart instead of Sankey.** It still shows how spend splits by state and then by coastal vs inland.
- **Jittered strip plot instead of beeswarm.** Dots are offset so they don't overlap, but not packed by a force layout.

If your unit allows full Vega, its official examples include a treemap and a beeswarm (search "vega treemap example" or "vega beeswarm example").

## Data columns the specs expect

**regions.csv** has one row per tourism region.

| Column | Meaning |
|---|---|
| `region` | Tourism region name. Must match the boundary file if you map regions. |
| `state` | NSW, VIC, QLD, SA, WA, TAS, NT or ACT |
| `coastal` | `Coastal` or `Inland`. Classify this yourself, e.g. regions that touch the coastline in the TRA shapefile. |
| `capital` | `Yes` or `No`. Charts 3, 4 and 12 drop capitals so big cities don't swamp regional areas. |
| `lat`, `lon` | Approximate centre of the region, for chart 2 |
| `visitors_k`, `nights_k` | Overnight visitors and nights, in thousands (TRA DoTS + IVS via state tourism bodies) |
| `spend_m`, `dom_spend_m`, `intl_spend_m` | Total, domestic and international spend, in $ million |
| `jobs_share_2019`, `jobs_share_2024` | Tourism share of regional filled jobs, as % (Regional Tourism Satellite Account) |

**monthly_regions.csv:** `region`, `lat` (used to sort rows north to south), `month` (1–12), `trips_k`. Source: TRA regional mobility data.

**arrivals_monthly.csv:** `year`, `month` (1–12), `state`, `arrivals`. Source: ABS Overseas Arrivals and Departures, short-term visitor arrivals by state of intended stay.

**reef_monthly.csv:** `month` (1–12), `visitor_days`. Source: GBRMPA tourism visitation data.

**flows.csv:** `origin`, `origin_state`, `origin_lat`, `origin_lon`, `dest_region`, `dest_lat`, `dest_lon`, `trips_k`. One row per origin-destination pair. Source: TRA domestic regional mobility data, or the interstate/intrastate splits in state tourism snapshots.

**marine_sectors.csv:** `sector`, `order`, `group`, `share_pct`. `share_pct` must be whole numbers that add to 100. Source: AIMS Index of Marine Industry. If you rename sectors, update the colour `domain` in `09_waffle`.

Also update the chart titles once you have real data. They were written for the sample data and may not match what your real data shows.

## Mapping tourism regions instead of states

1. Download the tourism region shapefile ZIP from TRA (*Profiles → Tourism regions maps*).
2. Convert and simplify it with mapshaper (web version at mapshaper.org, or `npx mapshaper`):
   ```
   mapshaper TR_shapefile.shp -proj wgs84 -filter-islands min-area=100km2 -simplify 5% keep-shapes -rename-layers regions -o data/tourism_regions.topojson format=topojson
   ```
   Run `mapshaper TR_shapefile.shp -info` first to find the column holding region names.
3. In `01_choropleth`, delete the `aggregate` and `coastal_share` steps. Calculate a per-region measure such as spend per night, then change the lookup:
   ```json
   {
     "lookup": "region",
     "from": {
       "data": {"url": "data/tourism_regions.topojson", "format": {"type": "topojson", "feature": "regions"}},
       "key": "properties.YOUR_NAME_FIELD"
     },
     "as": "geo"
   }
   ```
   Region names in your CSV must match the shapefile exactly. Regions that don't match won't be drawn.

## Using the online Vega Editor

You can paste any spec into https://vega.github.io/editor, but the relative `data/...` URLs won't resolve there. For testing, temporarily swap them for full URLs to your files on GitHub, e.g. `https://raw.githubusercontent.com/<you>/<repo>/main/data/regions.csv`.

## Rebuilding the sample data
`python tools/make_sample_data.py` regenerates every placeholder CSV except the boundary file.
