import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from shiny import App, reactive, render, ui

df = pd.read_csv("data/raw/spotify_songs.csv")
df = df.drop_duplicates(subset="track_id")
df["duration_s"] = (df["duration_ms"] / 1000).round(1)

app_ui = ui.page_fillable(
    ui.panel_title("SPOTIFIND"),
    ui.layout_sidebar(
        ui.sidebar("Filter control", open="desktop"),
        
        ui.layout_columns(
            ui.value_box(
                "Songs Found",
                ui.output_text("kpi_count"),
                showcase=ui.tags.span("🎵"),
            ),
            ui.value_box(
                "Avg Energy",
                ui.output_text("kpi_energy"),
                showcase=ui.tags.span("⚡"),
            ),
            ui.value_box(
                "Avg Danceability",
                ui.output_text("kpi_dance"),
                showcase=ui.tags.span("🕺"),
            ),
            col_widths=[4, 4, 4],
        ),
        ui.layout_columns(
            ui.value_box("Drop down", "X, Y drop down for scatter plot"),
            ui.card(ui.card_header("Top genre")),
            fill=False,
        ),
        ui.layout_columns(
            ui.card(ui.card_header("Scatter plot"), full_screen=True),
            ui.card(ui.card_header("Song search"), full_screen=True),
            col_widths=[6, 6],
        ),

        ui.hr(),
        ui.p(
            ui.HTML(
                "Spotifind | Data: TidyTuesday Spotify Songs | "
                "Authors: Rahiq Raees, Nguyen Nguyen, Shuhang Li, Jose Davila | "
                "<a href='https://github.com/UBC-MDS/DSCI-532_2026_37_Spotifind' target='_blank'>GitHub Repo</a> | "
                "Last updated: February 2026"
            ),
            style="color: grey; font-size: 0.8em; text-align: center;"
        ),
    ),
)

def server(input, output, session):
    @render.text
    def kpi_count():
        return f"{len(filtered_df()):,} songs"

    @render.text
    def kpi_energy():
        data = filtered_df()
        if data.empty:
            return "—"
        return f"{data['energy'].mean():.2f} / 1.0"

    @render.text
    def kpi_dance():
        data = filtered_df()
        if data.empty:
            return "—"
        return f"{data['danceability'].mean():.2f} / 1.0"

app = App(app_ui, server)