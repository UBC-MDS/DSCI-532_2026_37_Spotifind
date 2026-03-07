import os
import pandas as pd
import matplotlib.pyplot as plt
from shiny import App, reactive, render, ui
import plotly.express as px
from dotenv import load_dotenv
from querychat import QueryChat

# Load ANTHROPIC_API_KEY
load_dotenv()

# Data loading
df = pd.read_csv("data/raw/spotify_songs.csv")
df = df.drop_duplicates(subset="track_id")
df["duration_s"] = (df["duration_ms"] / 1000).round(1)

# QueryChat 
AI_COLS = [
    "track_name", "track_artist", "track_album_name",
    "track_album_release_date", "playlist_genre",
    "track_popularity", "danceability", "energy",
    "valence", "acousticness", "tempo", "duration_s",
]
qc = QueryChat(
    df[AI_COLS],
    "spotify_songs",
    client="anthropic/claude-haiku-4-5-20251001",
)

# UI
app_ui = ui.page_navbar(

    # Original Dashboard 
    ui.nav_panel(
        "🎵 Dashboard",

        ui.layout_sidebar(

            # Sidebar with accordion-grouped filters
            ui.sidebar(
                ui.h5("Filter Controls"),
                ui.hr(),
                ui.accordion(
                    ui.accordion_panel(
                        "Audio Features",
                        ui.input_slider("danceability", "Danceability", 0.0, 1.0, value=[0.0, 1.0], step=0.01),
                        ui.input_slider("energy", "Energy", 0.0, 1.0, value=[0.0, 1.0], step=0.01),
                        ui.input_slider("valence", "Valence (Mood)", 0.0, 1.0, value=[0.0, 1.0], step=0.01),
                        ui.input_slider("acousticness", "Acousticness", 0.0, 1.0, value=[0.0, 1.0], step=0.01),
                    ),
                    ui.accordion_panel(
                        "Track Properties",
                        ui.input_slider("tempo", "Tempo (BPM)", 0, 250, value=[0, 250], step=1),
                        ui.input_slider("duration_s", "Duration (seconds)", 0, 600, value=[0, 600], step=1),
                        ui.input_slider("popularity", "Popularity (0–100)", 0, 100, value=[0, 100], step=1),
                        ui.input_select(
                            "genre_filter",
                            "Genre",
                            choices=["All"] + sorted(df["playlist_genre"].dropna().unique().tolist()),
                            selected="All",
                        ),
                    ),
                    open=["Audio Features", "Track Properties"],
                ),
                ui.hr(),
                ui.input_action_button(
                    "reset_all", "Reset Filters",
                    class_="btn-outline-secondary btn-sm w-100"
                ),
                width=260,
                open="desktop",
            ),

            # KPI value boxes
            ui.layout_columns(
                ui.value_box(
                    "Songs Found",
                    ui.output_text("kpi_count"),
                    showcase=ui.tags.span("🎵", style="font-size:2.5rem;"),
                    theme="primary",
                ),
                ui.value_box(
                    "Avg Energy",
                    ui.output_text("kpi_energy"),
                    showcase=ui.tags.span("⚡", style="font-size:2.5rem;"),
                    theme="success",
                ),
                ui.value_box(
                    "Avg Danceability",
                    ui.output_text("kpi_dance"),
                    showcase=ui.tags.span("🕺", style="font-size:2.5rem;"),
                    theme="info",
                ),
                col_widths=[4, 4, 4],
            ),

            # Mood Map card
            ui.card(
                ui.card_header("Mood Map — Valence vs Energy"),
                ui.output_ui("plot_mood_map"),
                full_screen=True,
            ),

            # Results Table and Top Genres cards
            ui.layout_columns(
                ui.card(
                    ui.card_header("Results Table"),
                    ui.output_data_frame("tbl_results"),
                    full_screen=True,
                ),
                ui.card(
                    ui.card_header("Top Genres"),
                    ui.output_plot("tbl_top_genre"),
                ),
                col_widths=[8, 4],
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
    ),

    # AI Explorer 
    ui.nav_panel(
        "🤖 AI Explorer",

        ui.layout_sidebar(

            # querychat chat interface in the sidebar
            qc.sidebar(),

            # Main content area
            ui.h4("AI-Filtered Results", class_="mb-3"),

            # Download button
            ui.download_button(
                "download_ai_data",
                "⬇️ Download Filtered Data",
                class_="btn-success mb-3",
            ),

            # Filtered dataframe table
            ui.card(
                ui.card_header("Filtered Songs"),
                ui.output_data_frame("ai_tbl_results"),
                full_screen=True,
            ),

            # Visualizations driven by the AI-filtered dataframe
            ui.layout_columns(
                ui.card(
                    ui.card_header("Mood Map — AI Filtered"),
                    ui.output_ui("ai_plot_mood_map"),
                    full_screen=True,
                ),
                ui.card(
                    ui.card_header("Top Genres — AI Filtered"),
                    ui.output_plot("ai_tbl_top_genre"),
                ),
                col_widths=[8, 4],
            ),
        ),
    ),

    # App-level header 
    title=ui.div(
        ui.span("🎵 Spotifind", class_="fw-bold"),
        ui.span(" · Spotify Song Explorer", class_="opacity-75 small ms-2"),
    ),
    bg="#0d6efd",
    inverse=True,
    theme=ui.Theme("flatly"),
)


# Server
def server(input, output, session):

    # Initialize querychat
    qc_state = qc.server()

    # existing server

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

    @reactive.effect
    @reactive.event(input.reset_all)
    def _reset_filters():
        ui.update_slider("danceability", value=[0.0, 1.0])
        ui.update_slider("energy", value=[0.0, 1.0])
        ui.update_slider("valence", value=[0.0, 1.0])
        ui.update_slider("acousticness", value=[0.0, 1.0])
        ui.update_slider("tempo", value=[0, 250])
        ui.update_slider("duration_s", value=[0, 600])
        ui.update_slider("popularity", value=[0, 100])
        ui.update_select("genre_filter", selected="All")

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

    @render.ui
    def plot_mood_map():
        data = filtered_df()
        if data.empty:
            return ui.p("No songs match filters", style="text-align:center; padding:2rem;")
        sample = data.sample(min(500, len(data)), random_state=42)
        fig = px.scatter(
            sample, x="valence", y="energy", color="danceability",
            color_continuous_scale="viridis",
            hover_data={"track_name": True, "track_artist": True,
                        "danceability": ":.2f", "valence": ":.2f", "energy": ":.2f"},
            labels={"valence": "Valence (Sadness → Happiness)",
                    "energy": "Energy (Calm → Intense)", "danceability": "Danceability"},
            title=f"Mood Map  —  {len(data):,} songs", opacity=0.6,
        )
        fig.add_shape(type="rect", x0=0, x1=0.5, y0=0.5, y1=1.0, fillcolor="#c0d9f5", opacity=0.25, line_width=0)
        fig.add_shape(type="rect", x0=0.5, x1=1.0, y0=0.5, y1=1.0, fillcolor="#f5e6c0", opacity=0.25, line_width=0)
        fig.add_shape(type="rect", x0=0, x1=0.5, y0=0.0, y1=0.5, fillcolor="#d4c0f5", opacity=0.25, line_width=0)
        fig.add_shape(type="rect", x0=0.5, x1=1.0, y0=0.0, y1=0.5, fillcolor="#c0f5d0", opacity=0.25, line_width=0)
        fig.add_hline(y=0.5, line_dash="dash", line_color="#555555", line_width=1.5, opacity=0.8)
        fig.add_vline(x=0.5, line_dash="dash", line_color="#555555", line_width=1.5, opacity=0.8)
        for x, y, text, color in [
            (0.02, 0.98, "Sad & Intense", "#2a5fa5"),
            (0.52, 0.98, "Happy & Intense", "#a57a2a"),
            (0.02, 0.02, "Sad & Calm", "#6a2aa5"),
            (0.52, 0.02, "Happy & Calm", "#2aa55a"),
        ]:
            fig.add_annotation(x=x, y=y, text=f"<b>{text}</b>", xref="paper", yref="paper",
                               showarrow=False, font=dict(size=11, color=color), opacity=0.75)
        fig.update_layout(height=400, margin=dict(l=40, r=40, t=50, b=40),
                          xaxis=dict(range=[0, 1]), yaxis=dict(range=[0, 1]))
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=True))

    @render.data_frame
    def tbl_results():
        data = filtered_df()[
            ["track_name", "track_artist", "track_album_name",
             "track_album_release_date", "playlist_genre", "track_popularity"]
        ].rename(columns={
            "track_name": "Song", "track_artist": "Artist",
            "track_album_name": "Album", "track_album_release_date": "Released",
            "playlist_genre": "Genre", "track_popularity": "Popularity",
        }).sort_values("Popularity", ascending=False).reset_index(drop=True)
        high_pop_rows = data.index[data["Popularity"] >= 70].tolist()
        styles = [{"rows": high_pop_rows, "style": {"background-color": "#d4edda"}}]
        return render.DataGrid(data, height="250px", width="100%", styles=styles)

    @render.plot
    def tbl_top_genre():
        data = filtered_df()
        fig, ax = plt.subplots(figsize=(4, 3))
        if data.empty:
            ax.text(0.5, 0.5, "No songs match filters", ha="center", va="center", fontsize=12)
            ax.axis("off")
            return fig
        top = (
            data["playlist_genre"].value_counts().reset_index()
            .rename(columns={"playlist_genre": "Genre", "count": "Count"})
            .head(6).sort_values("Count", ascending=True)
        )
        bars = ax.barh(top["Genre"], top["Count"], color="#1DB954", edgecolor="none")
        for bar, val in zip(bars, top["Count"]):
            ax.text(bar.get_width() + 20, bar.get_y() + bar.get_height() / 2,
                    f"{val:,}", va="center", fontsize=9)
        ax.set_xlabel("Number of Songs", fontsize=10)
        ax.set_title("Top Genres", fontsize=11, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xlim(0, top["Count"].max() * 1.15)
        fig.tight_layout()
        return fig

    # AI Explorer server logic
    @reactive.calc
    def ai_filtered_df():
        return qc_state.df()

    @render.data_frame
    def ai_tbl_results():
        data = ai_filtered_df()[
            ["track_name", "track_artist", "track_album_name",
             "track_album_release_date", "playlist_genre", "track_popularity"]
        ].rename(columns={
            "track_name": "Song", "track_artist": "Artist",
            "track_album_name": "Album", "track_album_release_date": "Released",
            "playlist_genre": "Genre", "track_popularity": "Popularity",
        }).sort_values("Popularity", ascending=False).reset_index(drop=True)
        high_pop_rows = data.index[data["Popularity"] >= 70].tolist()
        styles = [{"rows": high_pop_rows, "style": {"background-color": "#d4edda"}}]
        return render.DataGrid(data, height="300px", width="100%", styles=styles)

    @render.download(filename="spotifind_ai_filtered.csv")
    def download_ai_data():
        yield ai_filtered_df().to_csv(index=False)

    # AI tab visualizations
    @render.ui
    def ai_plot_mood_map():
        data = ai_filtered_df()
        if data.empty:
            return ui.p("No songs match filters", style="text-align:center; padding:2rem;")
        sample = data.sample(min(500, len(data)), random_state=42)
        fig = px.scatter(
            sample, x="valence", y="energy", color="danceability",
            color_continuous_scale="viridis",
            hover_data={"track_name": True, "track_artist": True,
                        "danceability": ":.2f", "valence": ":.2f", "energy": ":.2f"},
            labels={"valence": "Valence (Sadness → Happiness)",
                    "energy": "Energy (Calm → Intense)", "danceability": "Danceability"},
            title=f"Mood Map  —  {len(data):,} songs", opacity=0.6,
        )
        fig.add_shape(type="rect", x0=0, x1=0.5, y0=0.5, y1=1.0, fillcolor="#c0d9f5", opacity=0.25, line_width=0)
        fig.add_shape(type="rect", x0=0.5, x1=1.0, y0=0.5, y1=1.0, fillcolor="#f5e6c0", opacity=0.25, line_width=0)
        fig.add_shape(type="rect", x0=0, x1=0.5, y0=0.0, y1=0.5, fillcolor="#d4c0f5", opacity=0.25, line_width=0)
        fig.add_shape(type="rect", x0=0.5, x1=1.0, y0=0.0, y1=0.5, fillcolor="#c0f5d0", opacity=0.25, line_width=0)
        fig.add_hline(y=0.5, line_dash="dash", line_color="#555555", line_width=1.5, opacity=0.8)
        fig.add_vline(x=0.5, line_dash="dash", line_color="#555555", line_width=1.5, opacity=0.8)
        for x, y, text, color in [
            (0.02, 0.98, "Sad & Intense", "#2a5fa5"),
            (0.52, 0.98, "Happy & Intense", "#a57a2a"),
            (0.02, 0.02, "Sad & Calm", "#6a2aa5"),
            (0.52, 0.02, "Happy & Calm", "#2aa55a"),
        ]:
            fig.add_annotation(x=x, y=y, text=f"<b>{text}</b>", xref="paper", yref="paper",
                               showarrow=False, font=dict(size=11, color=color), opacity=0.75)
        fig.update_layout(height=400, margin=dict(l=40, r=40, t=50, b=40),
                          xaxis=dict(range=[0, 1]), yaxis=dict(range=[0, 1]))
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=True))

    @render.plot
    def ai_tbl_top_genre():
        data = ai_filtered_df()
        fig, ax = plt.subplots(figsize=(4, 3))
        if data.empty:
            ax.text(0.5, 0.5, "No songs match filters", ha="center", va="center", fontsize=12)
            ax.axis("off")
            return fig
        top = (
            data["playlist_genre"].value_counts().reset_index()
            .rename(columns={"playlist_genre": "Genre", "count": "Count"})
            .head(6).sort_values("Count", ascending=True)
        )
        bars = ax.barh(top["Genre"], top["Count"], color="#1DB954", edgecolor="none")
        for bar, val in zip(bars, top["Count"]):
            ax.text(bar.get_width() + 20, bar.get_y() + bar.get_height() / 2,
                    f"{val:,}", va="center", fontsize=9)
        ax.set_xlabel("Number of Songs", fontsize=10)
        ax.set_title("Top Genres — AI Filtered", fontsize=11, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xlim(0, top["Count"].max() * 1.15)
        fig.tight_layout()
        return fig


app = App(app_ui, server)