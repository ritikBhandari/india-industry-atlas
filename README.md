# India Industry Atlas

Interactive, expandable analytics dashboard for India's Annual Survey of Industries (ASI), NIC 2008, FY 2008–09 through FY 2023–24.

**Data integrity:** The GitHub Pages workflow downloads and validates all 42 published source tables before publishing. A failed download or validation blocks deployment; absence of real data is never presented as success.

## Features
- Build multiple comparative time series for different ASI indicators, NIC industries and regions.
- Toggle 2-, 3-, 4-digit NIC classifications nationally; state-level 2-digit industry comparisons; all-state totals.
- Compare raw values, indexed series (100 at the first valid overlapping year), year-on-year changes, and percent changes.
- Explore derived ratios such as value-added per worker, capital intensity, wage per worker, profit margins, workforce composition and fuel intensity.
- Coverage dashboard shows loaded files, available time series and missing observations.
- Download chart results as CSV.

## Deployment
Under **Settings → Pages**, set Source to **GitHub Actions**. The workflow starts on pushes to `master`, runs monthly and can be manually dispatched.

The workflow uses data from [Measure of India ASI tables](https://measure.thisindianlife.today/guides/factories/every-cut/asi-tables-2008/) (source: MoSPI NSO). See `scripts/sync_data.py` and `scripts/verify_data.py`.

## Data limitations
State-by-NIC3/NIC4 intersections are not present in the 42-table published collection; the UI does not invent those. Monetary data are nominal. NIC levels must not be added together. Changes in state boundaries can affect comparability. The 2023–24 4-digit all-industries copies for indicators 36–49 have a known source issue and should not be used for all-industry totals.

## Source verification
The source collection advertises 63,455 time series in 42 files. This is a source claim **until** the GitHub workflow downloads and verifies the actual data. Exact counts and manifest checks are written to `data/coverage-report.json`.
## State map geography, provenance and accuracy
The choropleth uses the 36-state/UT low-resolution GeoJSON from [Vardhan Systems' vardhan-maps](https://github.com/Vardhan-Systems/vardhan-maps), built from OpenStreetMap and editorial boundary adjustments. **Map data © OpenStreetMap contributors, ODbL 1.0**. [Attribution and license terms](https://github.com/Vardhan-Systems/vardhan-maps/blob/main/ATTRIBUTION.md); [OpenStreetMap copyright](https://www.openstreetmap.org/copyright).

This is an illustrative administrative geography layer, not an official Survey of India map. Contemporary states/UTs differ from some historical ASI reporting regions; the map does not infer comparable series for restructured regions. The automated browser test checks 36 shapes, at least 10,000 boundary vertices, Indian coordinate extent, state colouring and that state shapes respond to clicks. The geometry file retains the source ODbL licensing terms.

## User-provided India State Boundary shapefile (current map)
The live map now uses the uploaded `India_State_Boundary.shp/.dbf/.prj` geometry, **not** the prior OpenStreetMap boundary layer. The source is a Lambert Conformal Conic WGS84 projection; the exported `data/india-states.geojson` is in EPSG:4326 (longitude/latitude), simplified to approximately 2.4 km for interactive display. Its features are mapped to ASI regions by official LGD state identifiers (36 names), not fragile label matching. Four separate disputed features in the source have been excluded from state-specific choropleth coloring; they are not assigned to a state without evidence. The accompanying conversion file is `india-states-from-user-shapefile.geojson`, available as a generated artifact in the ChatGPT conversation. Data coverage and historic boundary comparability remain subject to the ASI reporting classifications.
