# App Specification

## 2.1 Updated Job Stories

## 2.2 Component Inventory

## 2.3 Reactivity Diagram

## 2.4 Calculation Details

### `filtered_df`

- **Depends on:** `input_danceability`, `input_tempo`, `input_acousticness`, `input_valence`, `input_energy`, `input_duration_s`, `input_popularity`, `input_genre_filter`
- **Transformation:** Filters the dataset to rows where danceability, tempo, acousticness, valence, energy, duration, and popularity fall within the selected slider ranges. If a specific genre is selected, further filters to only rows matching that genre.
- **Consumed by:** `kpi_count`, `kpi_energy`, `kpi_dance`, `plot_mood_map`, `tbl_results`, `tbl_top_genre`