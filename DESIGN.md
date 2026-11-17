# Donation explorer design notes

Web prototype for readers examining UIJP's published donations. Existing D3 and data remain embedded in index.html; styles.css is the editable style source, and build.py regenerates the standalone HTML.

## Decisions

- Preserve the requested neutral palette, TT Firs Text Trial font preference, real donation data, all chart types, two-way supporter search, and both reset controls.
- Replace rounded, filled dashboard cards with ruled sections, a masthead, numbered figures, and an editorial reading sequence. Donation amounts use tabular numerals.
- Keep all filtering controls in the same reading order. The lower search operates the same global supporter filter; Reset in either location clears all filters.
- Replace a 2,469-row scrolling DOM with 50-row pages, showing result count and page position. CSV still exports all matching records.
- Add a skip link, explicit keyboard focus, native controls, 44px control heights, table caption and headers, a recoverable empty state, and chart bar accessible labels.
- At narrow widths, stack analysis sections and wrap controls; retain every primary action.

## Tokens

Canvas #191a18; text #e6e4df; secondary text #b1afa9; rules #4d4e49; chart bars #c3c0b7 / #939990. Corners 2px. No shadows, gradients, decorative icons, or animated entry effects. Typeface: TT Firs Text Trial with TT Firs Text and system fallbacks; font files are not bundled.

## Guidance

WCAG 2.2 AA is the quality target, not a certification. Implementation references: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html and https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html . Preserve reading order and visible focus and recompose at narrow widths.

Source: https://www.utahinvestigative.org/transparency/ . Data provenance limitations remain visible in the artifact. These design choices are expert judgments, not observed usability-study findings.

## Validation performed

Static skill check: zero reported errors or warnings. Product-native browser CSS viewports 320, 768, and 1440px reported document/body widths within the viewport. Four charts rendered. Confirmed lower search updates upper search, year filtering yields matching-year ledger entries, pagination moves to page 2, Reset returns page 1, and no-result searches display recovery guidance. Input focus remained after updates and the focused input had a solid outline. HTML preview reported no console messages. Full keyboard traversal, assistive technology testing, and a complete WCAG audit remain unperformed. Browser font check accepted the requested family, but no font file is bundled or redistributed.

## Warm amber revision

Selected comp B: chart marks now use amber (#c99755) and pale gold (#efd294), while page text and structure remain neutral. Added separate 2025 and 2026 donation-count heatmaps with fixed bands: 0, 1–4, 5–14, 15–39, 40+. Every cell displays a count; native table headers identify month and gift size. Heatmaps share the existing global filters. The 2026 table stops at October, matching the source coverage. Narrow screens can scroll the heatmap region horizontally. Static checks passed; HTML renders at 728px and 390px reported no console messages.

## System appearance

The stylesheet follows prefers-color-scheme, with color-scheme support for native form controls. Light mode uses warm paper, dark ink, and an amber heatmap that deepens with donation count. Dark mode retains charcoal with amber that brightens as counts increase. Heatmap cells and legends use the same CSS variables, so appearance changes apply immediately without rebuilding chart data or losing filters. Standalone page background, tooltip, chart marks, labels, controls, and table surfaces follow these tokens. Light and dark HTML previews returned no console messages; static checks passed.

## Historical import — November 17, 2026

Imported the user-provided UIJP-donations-2016-through-2020.csv: 1,628 rows, $80,830.46. Combined dataset: 4,097 rows, $295,697.60. Dates and amounts of all 2,469 existing records reconciled unchanged. Historical dates parsed from abbreviated month names; currency parsed with Decimal. Trimmed/collapsed whitespace without changing spelling, capitalization, or identities. One exact repeated historical row retained. Raw CSV preserved in sources/; import-report.json records its SHA-256 and annual reconciliations. Re-running clean_data.py is idempotent.

Year options and heatmaps cover 2016–2020 and 2025–2026. The monthly chart preserves chronological spacing and marks the unsupplied 2021–2024 gap explicitly. No zero-donation inference is made for missing years. Seven annual filter totals reconciled to source data. Multi-chip filtering combined with 2020, Reset to 4,097 records, seven heatmaps, and the initial 1,000 ledger rows verified in HTML preview. Static checks passed. Compact embedded tuples preserve the self-contained offline artifact while reducing its size.

## Exact duplicate consolidation — November 17, 2026

At the user's request, consolidated each exact date/donor/amount group to one record. Removed 22 extra records ($116.11); final ledger has 4,075 records totaling $295,581.49. Retained duplicate-rows.csv unchanged, with row numbers referring to the original combined CSV. deduplication-report.json records removed source positions and reconciliation. Raw sources remain intact. The import pipeline now applies this policy on every rebuild; verified that repeated imports are idempotent and no exact duplicates remain. Earlier retention notes above describe the pre-consolidation history.
