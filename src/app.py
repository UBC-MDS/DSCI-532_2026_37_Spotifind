import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from shiny import App, reactive, render, ui

# =============================================================================
# RAHIQ — Data loading and sidebar filter controls
# Branch: feat/filter-controls
# =============================================================================

df = pd.read_csv("data/raw/spotify_songs.csv")
df = df.drop_duplicates(subset="track_id")
df["duration_s"] = (df["duration_ms"] / 1000).round(1)

# ── UI ────────────────────────────────────────────────────────────────────────
app_ui = ui.page_fillable(
    ui.panel_title("🎵 Spotifind"),
    ui.layout_sidebar(

        # RAHIQ — Sidebar with all filter sliders and genre dropdown
        ui.sidebar(
            ui.h5("Filter Controls"),
            ui.hr(),
            ui.input_slider("danceability", "Danceability", 0.0, 1.0, value=[0.0, 1.0], step=0.01),
            ui.input_slider("energy", "Energy", 0.0, 1.0, value=[0.0, 1.0], step=0.01),
            ui.input_slider("valence", "Valence (Mood)", 0.0, 1.0, value=[0.0, 1.0], step=0.01),
            ui.input_slider("acousticness", "Acousticness", 0.0, 1.0, value=[0.0, 1.0], step=0.01),
            ui.input_slider("tempo", "Tempo (BPM)", 0, 250, value=[0, 250], step=1),
            ui.input_slider("duration_s", "Duration (seconds)", 0, 600, value=[0, 600], step=1),
            ui.input_slider("popularity", "Popularity (0–100)", 0, 100, value=[0, 100], step=1),
            ui.hr(),
            ui.input_select(
                "genre_filter",
                "Genre",
                choices=["All"] + sorted(df["playlist_genre"].dropna().unique().tolist()),
                selected="All",
            ),
            width=260,
            open="desktop",
        ),
    ),
)

# ── Server ────────────────────────────────────────────────────────────────────
def server(input, output, session):

    # =========================================================================
    # RAHIQ — filtered_df reactive calc
    # Branch: feat/filter-controls
    # =========================================================================
    @reactive.calc
    def filtered_df():
        data = df.copy()
        data = data[
            (data["danceability"].between(*input.danceability())) &
            (data["energy"].between(*input.energy())) &
            (data["valence"].between(*input.valence())) &
            (data["acousticness"].between(*input.acousticness())) &
            (data["tempo"].between(*input.tempo())) &
            (data["duration_s"].between(*input.duration_s())) &
            (data["track_popularity"].between(*input.popularity()))
        ]
        if input.genre_filter() != "All":
            data = data[data["playlist_genre"] == input.genre_filter()]
        return data

app = App(app_ui, server)