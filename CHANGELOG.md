# Changelog

## [0.4.0] - 2026-03-14

### Added

- Switched data layer to Parquet + DuckDB via ibis for lazy query execution; all filtering now happens at the database level before data enters memory (#58).
- Added `filtered_summary` reactive calc that runs a DuckDB aggregation for KPI values, avoiding full DataFrame materialization on every filter change (#58).
- Implemented Option D advanced feature: clickable quadrant interaction on the Mood Map. Clicking a quadrant filters the entire dashboard to songs within that mood region, with visual highlighting and a sidebar badge indicating the active filter (#54).
- Added Playwright behavior tests and pytest unit tests covering core dashboard logic (#56).

### Changed

- Avg Energy and Avg Danceability KPI boxes now display as percentages (e.g. `70%`) instead of fractions (e.g. `0.70 / 1.0`) for improved readability. Addressed feedback from Tiantong Yin (#57) via #62.
- Mood Map quadrant labels for right-side quadrants ("Happy & Intense", "Happy & Calm") repositioned using `xanchor="right"` to prevent offset caused by colorbar shrinking paper coordinate space. Addressed feedback from Diana Cornescu (#57) via #61.
- Removed whitespace below Mood Map caused by hidden `clicked_quadrant_raw` input rendering as a visible empty text box. Addressed feedback from Diana Cornescu (#57) via #61.
- Mood Map color gradient now pins to unfiltered dataset min/max danceability values for consistent coloring regardless of active filters. Addressed feedback from Tiantong Yin (Critical, #57) via #59.
- AI tab chat now scrolls independently from the main page content. Addressed feedback from Daniel (Critical, #57) via #60.
- AI Explorer filtered table now displays before visualizations for a clearer top-down reading flow. Addressed feedback from Diana Cornescu (#57) via #69.
- Dataframe now fills the full card width. Addressed feedback from Daniel (#57) via #71.
- Test UI results updated to display in percentage format for consistency with KPI boxes (#67).

### Fixed

- Bugs resolved since M3 are captured in the feedback items above (#59, #60, #61, #62, #67).

- **Feedback prioritization issue link:** #48

### Known Issues

- Input sliders do not support direct text entry; users must drag to set values. Noted in feedback from Tiantong Yin (#57) but not addressed this milestone due to time constraints.
- Chatbot conversation grows the sidebar on very long sessions despite the independent scroll fix on the main page.

### Release Highlight: Mood Map Quadrant Click Interaction

Clicking any of the four quadrant regions on the Mood Map (Sad & Intense, Happy & Intense, Sad & Calm, Happy & Calm) now filters the entire dashboard: sliders, results table, KPIs, and top genres chart to songs within that mood region. A sidebar badge and checkmark on the map indicate the active quadrant. Clicking the same quadrant again deselects it. This makes mood-based song discovery faster and more intuitive, directly supporting the primary use case of finding songs by feel rather than by numeric audio features alone.

- **Option chosen:** D
- **PR:** #54
- **Why this option over the others:** Option D directly enhances the primary visual discovery use case without requiring external services, additional API costs, or experimental notebooks. It turns the Mood Map, already the centrepiece of the dashboard, into an interactive filter, giving users a more intuitive entry point than dragging sliders.
- **Feature prioritization issue link:** #57

### Collaboration

- **CONTRIBUTING.md:** Updated with M3 retrospective and M4 collaboration norms via #63.
- **M3 retrospective:** Work distribution was unbalanced in M3 and several PRs were merged without review. For M4 we explicitly divided ownership so each member resolved at least one feedback item end-to-end, and enforced at least one approving review before merging.
- **M4:** All PRs received peer review before merging. Team aimed to complete work by Saturday March 14 ahead of the Tuesday deadline to allow time for final testing and the release.

### Reflection

The dashboard reliably handles all three job stories and the Mood Map click interaction meaningfully improves the discovery experience beyond what sliders alone provide. Current limitations include the lack of text entry on sliders and occasional layout stretch in the AI chat sidebar on long sessions. No intentional deviations from DSCI 531 visualization best practices were made; the Mood Map quadrant background colors were chosen to be perceptually distinct while remaining accessible.

The feedback prioritization process was straightforward: the two critical items (color scaling accuracy and chat scroll) were clear accuracy/UX breaks that had to be fixed first; the remaining non-critical items were distributed across team members with lower-impact ones marked not planned due to time constraints. Full rationale is in #57 and the ### Changed section above.

The querychat and DuckDB/ibis lectures were most directly applicable this milestone. Better coverage of Plotly event handling in Shiny (e.g. `plotly_click` with hidden inputs) would have saved significant debugging time.

## [0.3.0] - 2026-03-06

### Added
- AI Explorer tab powered by querychat with natural language data filtering
- querychat chat sidebar with auto-generated suggestions for exploring Spotify data
- AI-filtered dataframe table with popularity highlighting (green for songs ≥ 70)
- Mood Map and Top Genres visualizations driven by AI-filtered data
- Download button to export AI-filtered dataframe as CSV
- Converted `page_fluid` to `page_navbar` to support multi-tab layout
- New dependencies: `querychat`, `chatlas`, `duckdb`, `python-dotenv`

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
