# App Specification

## 2.1 Updated Job Stories

## 2.2 Component Inventory

| ID                   | Type          | Shiny widget / renderer | Depends on                                                              | Job story  |
| -------------------- | ------------- | ----------------------- | ----------------------------------------------------------------------- | ---------- |
| `input_danceability` | Input         | `ui.input_slider()`     | —                                                                       | #3         |
| `input_tempo`        | Input         | `ui.input_slider()`     | —                                                                       | #1         |
| `input_acousticness` | Input         | `ui.input_slider()`     | —                                                                       | #2         |
| `input_valence`      | Input         | `ui.input_slider()`     | —                                                                       | #2         |
| `input_energy`       | Input         | `ui.input_slider()`     | —                                                                       | #1         |
| `input_duration_s`   | Input         | `ui.input_slider()`     | —                                                                       | #2         |
| `input_popularity`   | Input         | `ui.input_slider()`     | —                                                                       | #3         |
| `input_genre_filter` | Input         | `ui.input_select()`     | —                                                                       | #1, #2, #3 |
| `filtered_df`        | Reactive calc | `@reactive.calc`        | `input_danceability`, `input_tempo`, `input_acousticness`, `input_valence`, `input_energy`, `input_duration_s`, `input_popularity`, `input_genre_filter` | #1, #2, #3 |
| `kpi_count`          | Output        | `@render.text`          | `filtered_df`                                                           | #1, #2, #3 |
| `kpi_energy`         | Output        | `@render.text`          | `filtered_df`                                                           | #1         |
| `kpi_dance`          | Output        | `@render.text`          | `filtered_df`                                                           | #3         |
| `plot_mood_map`      | Output        | `@render.plot`          | `filtered_df`                                                           | #2, #3     |
| `tbl_results`        | Output        | `@render.data_frame`    | `filtered_df`                                                           | #1, #2     |
| `tbl_top_genre`      | Output        | `@render.data_frame`    | `filtered_df`                                                           | #1, #2, #3 |

---

## 2.3 Reactivity Diagram

## 2.4 Calculation Details

### `filtered_df`

- **Depends on:** `input_danceability`, `input_tempo`, `input_acousticness`, `input_valence`, `input_energy`, `input_duration_s`, `input_popularity`, `input_genre_filter`
- **Transformation:** Filters the dataset to rows where danceability, tempo, acousticness, valence, energy, duration, and popularity fall within the selected slider ranges. If a specific genre is selected, further filters to only rows matching that genre.
- **Consumed by:** `kpi_count`, `kpi_energy`, `kpi_dance`, `plot_mood_map`, `tbl_results`, `tbl_top_genre`