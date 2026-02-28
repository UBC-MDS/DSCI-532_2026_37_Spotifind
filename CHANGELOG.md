# Changelog

## [0.2.0] - 2026-02-28

### Added
- Functional Shiny dashboard prototype (`src/app.py`) with full reactivity
- Sidebar with 7 filter controls grouped into two accordion sections: **Audio Features** (danceability, energy, valence, acousticness) and **Track Properties** (tempo, duration, popularity, genre)
- `filtered_df` `@reactive.calc` depending on all 8 inputs
- Mood Map scatter plot (valence vs energy, coloured by danceability via viridis) with colour-coded quadrant backgrounds and labels
- Results Table showing filtered songs sorted by popularity (descending) with conditional row highlighting for songs with popularity ≥ 70
- Top Genres table showing top 6 genres by count for the current filter state
- 3 KPI value boxes (Songs Found, Avg Energy, Avg Danceability) that update reactively with filters
- Bootstrap `flatly` theme via `ui.Theme("flatly")`
- Styled dashboard header using Bootstrap utilities (`bg-primary`, `text-white`, `d-flex`, `justify-content-between`)
- **Complexity Enhancement:** Reset Filters button using `@reactive.effect` + `@reactive.event(input.reset_all)` — restores all sliders and genre dropdown to defaults in one click
- `reports/m2_spec.md` with job stories, component inventory, reactivity diagram, calculation details, and complexity enhancement section
- `requirements.txt` with pinned package versions for deployment
- Footer with authors, GitHub repo link, and last updated date

### Changed
- Simplified dashboard from original M1 sketch: removed custom scatter plot (X/Y axis dropdowns) and song search detail card in favour of a cleaner layout focused on the mood map
- Data loading changed from URL to local `data/raw/spotify_songs.csv` for faster load times and offline support
- Added duration and popularity sliders to fully cover all three job stories
- Sidebar filters grouped into collapsible accordion sections to reduce visual clutter
- Replaced `ui.panel_title` with a full Bootstrap-styled header div
- Switched from `ui.page_fluid` to `ui.page_fillable` so cards stretch to fill the viewport (better for dashboards per lecture)

### Fixed
- Results table now stretches to full card width
- Removed Mac-only (`pyobjc`) and dev-only packages from `requirements.txt` to prevent deployment failures

### Known Issues
- Mood map samples up to 500 points for rendering performance; with very narrow filters the plot may look sparse
- `ui.Theme` requires `libsass` — must be included in `requirements.txt`

### Reflection

**Implementation Status:** All three job stories are now implemented or revised:
- Story #1 (gym playlist): ✅ Implemented: energy and tempo sliders filter songs directly; the results table lets Alex pick his top 15 songs sorted by popularity.
- Story #2 (study playlist): ✅ Implemented:  valence, acousticness, and duration sliders are all present and functional.
- Story #3 (dance floor discovery): 🔄 Revised: danceability and popularity sliders implemented; the mood map replaces the original scatter plot as the primary visual discovery tool.

**Deviations:** The original M1 sketch included a custom scatter plot with X/Y axis dropdowns, a song search detail card, and static KPI boxes. After building the full version, the dashboard felt cluttered. Following the "be concise" design principle from Lecture 2, we simplified to a single large mood map, a results table, and a top genres table. KPI value boxes were added back in minimal form (3 boxes) to satisfy the "include context" design principle. Filters were grouped into accordion sections following the Lecture 6 guidance on using `ui.accordion()` to respect Miller's Law (7±2 chunks).

**Known Issues:** The mood map samples up to 500 songs for rendering performance. With very tight filters the plot may look sparse, but the results table accurately shows all matching songs. The `ui.Theme("flatly")` requires `libsass` which must be present in `requirements.txt` and installed on Posit Connect Cloud.

**Best Practices:** The viridis colormap was chosen for the mood map as it is colorblind-friendly. Axis labels, a title with live song count, quadrant labels, and KPI boxes with units are all included to provide context for numbers. Conditional row highlighting in the results table uses a single green signal for high-popularity songs, consistent with the Lecture 6 principle of using colour purposefully — one signal per table.

**Self-Assessment:** The prototype successfully covers all job stories and has a clean, polished layout following lecture design principles. The complexity enhancement (reset button) meaningfully improves usability. Future improvements could include hover tooltips on the mood map and a CSV export button for the filtered results table.

## [0.1.0] - 2026-02-10

### Added
- Initial project setup with repository structure
- Teamwork contract
- Dashboard proposal (`reports/m1_proposal.md`) with dataset selection, motivation, job stories, EDA, and app sketch
- Layout-only skeleton app (`src/app.py`)
- `environment.yml` for local development