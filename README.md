# UIJP Donations

An interactive D3 explorer of donations published by the Utah Investigative Journalism Project, compiled by [Tod Robbins](https://todrobbins.com) with AI assistance.

## View or host

Open `index.html` in a browser. It embeds the styles, D3, data, and application code and works without a server or build step. Publish this directory on GitHub Pages or Netlify; `index.html` is the only required deployment file. The CSV files can also be published for transparency.

TT Firs Text Trial is referenced but not bundled. Visitors without the font use a system fallback.

## Update the data or design

Python 3 is sufficient; no additional packages are needed.

```sh
python3 clean_data.py
python3 build.py
```

`clean_data.py` extracts the saved public-page table and historical CSV, restores whitespace, and consolidates exact date/name/amount matches. `build.py` embeds `data.json`, `styles.css`, and `d3.min.js` into `index.html`. Rebuild the HTML after changing those files.

## Sources and documentation

- Public ledger: https://www.utahinvestigative.org/transparency/ (snapshot retrieved November 16, 2026).
- Historical CSV: `sources/UIJP-donations-2016-through-2020.csv`, supplied by UIJP.
- Cleaned export: `donations.csv`.
- Original duplicate review: `duplicate-rows.csv`, preserved unchanged; its row numbers refer to the original combined export.
- Import and cleanup records: `import-report.json`, `deduplication-report.json`, and `name-spacing-corrections.json`.
- Design and validation history: `DESIGN.md`.

The cleaned ledger contains 4,075 donations totaling $295,581.49. Data for 2021–2024 was not supplied. Missing data does not imply zero donations.
