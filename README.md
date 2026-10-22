# Coastal tourism in Australia — Vega-Lite project

Thirteen Vega-Lite v5 charts covering Australia's 76 tourism regions, plus the data
behind them. All thirteen specs have been rendered and verified.

## Run it

The page fetches specs and CSVs, which browsers block for `file://` URLs. Serve the folder:

- **VS Code:** install *Live Server*, right-click `index.html`, *Open with Live Server*
- **Terminal:** `python -m http.server` in this folder, then open http://localhost:8000
- **GitHub Pages:** push the folder and enable Pages; the relative paths keep working

## The thirteen charts

| # | Idiom | Data | Vega-Lite techniques |
|---|---|---|---|
| 1 | Choropleth map | regions + topojson | `aggregate`, `lookup` geometry, `geoshape`, equal-area projection |
| 2 | Proportional symbol map | regions + topojson | layered basemap, `longitude`/`latitude`, area-proportional `size`, legend selection |
| 3 | Flow map | flows + topojson | `rule` with `longitude2`/`latitude2`, `window` rank to thin lines, layered basemap |
| 4 | Parallel coordinates | regions | `fold`, `joinaggregate` min-max normalisation, `window` row ids, `detail` |
| 5 | Dumbbell chart | regions | `fold` wide→long, layered line + point, shared colour scale for stroke and fill |
| 6 | Heatmap | seasonality_quarterly | `rect`, diverging scale with `domainMid`, north-to-south `sort` by latitude |
| 7 | Cycle plot | arrivals_monthly | `facet` by month, layered line + mean `rule` |
| 8 | Radial heatmap | reef_quarterly | `arc` with explicit `theta`/`theta2` radians (`scale: null`), ring radii by year, clamped scale |
| 9 | Streamgraph | arrivals_monthly | `area` with `stack: "center"`, `datetime()`, `order` channel |
| 10 | Waffle chart | marine_sectors | `sequence()` + `flatten`, modulo grid maths |
| 11 | Marimekko chart | regions | two `stack` transforms with `normalize`, `x`/`x2`/`y`/`y2` rects |
| 12 | Jittered strip plot | regions | `yOffset`, deterministic pseudo-random jitter, log scale, `rank` labelling |
| 13 | Slope chart | regions | `fold` two years, direction via `calculate`, log scale, ranked end labels |

### Three idioms were substituted
Vega-Lite has no treemap, Sankey or force-directed beeswarm layout; those need full Vega.
This project uses a **waffle** instead of a treemap, a **Marimekko** instead of a Sankey, and a
**jittered strip plot** instead of a beeswarm. Chart 8 was planned as a twelve-month radial
chart, but the reef data is published quarterly, so it became a radial heatmap — angle is the
quarter, each ring a year.

## Column reference

**regions.csv** — one row per tourism region (76)

| Column | Meaning |
|---|---|
| `region`, `state` | Tourism region and state |
| `coastal` | `Coastal` or `Inland` — my classification, not an official one |
| `capital` | `Yes` for capital-city regions; charts 4, 5 and 13 exclude them |
| `lat`, `lon` | Approximate region centre, for the maps |
| `visitors_k`, `nights_k`, `spend_m` | Overnight visitors ('000), nights ('000), spend ($m) |
| `dom_spend_m`, `intl_spend_m` | Domestic and international split of spend |
| `tourism_gva_m_2324/2425` | Direct tourism gross value added ($m) |
| `tourism_jobs_k_2324/2425` | Direct tourism filled jobs ('000) |
| `tourism_jobs_total_k_2425` | Direct + indirect filled jobs ('000) |
| `tourism_consumption_m_2425` | Tourism consumption ($m) |
| `jobs_change_pct` | Change in direct jobs, 2023-24 → 2024-25 |
| `state_jobs_share_1819/2425` | Tourism's share of all filled jobs, **state level** |

**flows.csv** — `origin`, `origin_lat`, `origin_lon`, `dest_region`, `dest_state`,
`dest_lat`, `dest_lon`, `trips_k`

**seasonality_quarterly.csv** — `region`, `state`, `coastal`, `lat`, `quarter` (1–4),
`quarter_label`, `seasonal_index` (1.0 = that region's average quarter)

**arrivals_monthly.csv** — `year`, `month`, `state`, `arrivals`. ABS Table 11, 2015 to Aug 2026.

**reef_quarterly.csv** — `year`, `quarter`, `quarter_label`, `full_day`, `part_day`, `exempt`,
`scenic_flights`, `coral_viewing`, `total_visits`, `seasonal_index`. 2016 to mid-2026.

**marine_sectors.csv** — `sector`, `order`, `group`, `output_m_fy21/22/23`, `share_pct`
(whole numbers summing to 100). **marine_industries.csv** — all 19 industries, FY23.

## Methodology notes for your write-up

Three discontinuities affect this data and all three are worth naming:

1. **NVS → DoTS (January 2025).** TRA replaced the National Visitor Survey with Domestic
   Tourism Statistics. The two are not comparable; TRA says so explicitly.
2. **New sub-national TSA model (2024–25).** The State and Regional TSA models were replaced.
   Results were back-cast to 2018–19 at state level but only to **2023–24** at region level,
   which is why chart 13 spans one year. NSW's 2018–19 tourism share of filled jobs is 4.13%
   under the old model and 3.91% under the new one.
3. **Employment revisions.** Direct tourism filled jobs for 2018–19 were revised from 700,900
   to 632,000 between publications. Both years in any comparison here come from the same release.

Also worth stating: the coastal/inland split is my own judgement, not an official category;
reporting periods differ by state (NSW and QLD year-ending June 2026, WA calendar 2025,
SA year-ending December 2024); and several regions
have figures suppressed as `n/p` where samples were too small.

### Validation
The jobs figures were checked against TRA's own published output. State totals match Table 5
to within rounding (NSW 203.4 vs 203.2; national 695.7 vs 695.9), and the growth distribution
reproduces TRA's Figure 2 exactly — 23 regions declining, 41 growing up to 10%, 9 growing
10–20%, 2 growing 20–40%, 1 growing 40% or more — including the per-state decline counts.
