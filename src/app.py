import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from shiny import App, reactive, render, ui
import plotly.express as px
from querychat import QueryChat
import ibis
import plotly.graph_objects as go

# Load ANTHROPIC_API_KEY from .env
load_dotenv()

# DuckDB + Ibis connection
con = ibis.duckdb.connect()
songs = con.read_parquet("data/processed/spotify_songs.parquet")

# QueryChat — initialized once at module level with a small column subset
# to keep the schema prompt concise and reduce token usage
AI_COLS = [
    "track_name", "track_artist", "track_album_name",
    "track_album_release_date", "playlist_genre",
    "track_popularity", "danceability", "energy",
    "valence", "acousticness", "tempo", "duration_s",
]
ai_df = songs.select(*AI_COLS).to_pandas()
qc = QueryChat(
    ai_df,
    "spotify_songs",
    client="anthropic/claude-haiku-4-5-20251001",
)

genre_choices = ["All"] + sorted(
    songs.select("playlist_genre")
    .distinct()
    .to_pandas()["playlist_genre"]
    .dropna()
    .tolist()
)

QUADRANTS = {
    "sad_intense":   dict(v=(0.0, 0.5), e=(0.5, 1.0), color="#c0d9f5", label="😢 Sad & Intense",   text_color="#2a5fa5"),
    "happy_intense": dict(v=(0.5, 1.0), e=(0.5, 1.0), color="#f5e6c0", label="😄 Happy & Intense", text_color="#a57a2a"),
    "sad_calm":      dict(v=(0.0, 0.5), e=(0.0, 0.5), color="#d4c0f5", label="😔 Sad & Calm",      text_color="#6a2aa5"),
    "happy_calm":    dict(v=(0.5, 1.0), e=(0.0, 0.5), color="#c0f5d0", label="😊 Happy & Calm",    text_color="#2aa55a"),
}

def build_mood_map(data, selected_quadrant=""):
    sample = data.sample(min(500, len(data)), random_state=42)
    fig = go.Figure()
    quadrant_centers = {
        "sad_intense": (0.25, 0.75), "happy_intense": (0.75, 0.75),
        "sad_calm":    (0.25, 0.25), "happy_calm":    (0.75, 0.25),
    }

    # FIX 1: Use paper coords but anchor right-side labels to the right edge
    # so the colorbar doesn't push them toward the center divider.
    label_positions = {
        "sad_intense":   (0.02, 0.97),
        "happy_intense": (0.97, 0.97),
        "sad_calm":      (0.02, 0.03),
        "happy_calm":    (0.97, 0.03),
    }
    label_xanchor = {
        "sad_intense":   "left",
        "happy_intense": "right",
        "sad_calm":      "left",
        "happy_calm":    "right",
    }

    for qname, qinfo in QUADRANTS.items():
        is_selected = (qname == selected_quadrant)
        fig.add_shape(
            type="rect",
            x0=qinfo["v"][0], x1=qinfo["v"][1],
            y0=qinfo["e"][0], y1=qinfo["e"][1],
            fillcolor=qinfo["color"],
            opacity=0.65 if is_selected else 0.2,
            line=dict(color=qinfo["text_color"], width=3 if is_selected else 0),
        )
        cx, cy = quadrant_centers[qname]
        fig.add_trace(go.Scatter(
            x=[cx], y=[cy], mode="markers",
            marker=dict(size=90, opacity=0, color=qinfo["color"]),
            name=f"quadrant_{qname}",
            hovertemplate=f"<b>{qinfo['label']}</b><br>Click to filter data<extra></extra>",
            showlegend=False,
        ))
    fig.add_trace(go.Scatter(
        x=sample["valence"], y=sample["energy"], mode="markers",
        marker=dict(color=sample["danceability"], colorscale="viridis",
                    cmin=data["danceability"].min(),
                    cmax=data["danceability"].max(),
                    size=6, opacity=0.6, colorbar=dict(title="Danceability")),
        customdata=sample[["track_name", "track_artist", "danceability", "valence", "energy"]].values,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>Artist: %{customdata[1]}<br>"
            "Danceability: %{customdata[2]:.2f}<br>Valence: %{customdata[3]:.2f}<br>"
            "Energy: %{customdata[4]:.2f}<extra></extra>"
        ),
        name="songs", showlegend=False,
    ))
    fig.add_hline(y=0.5, line_dash="dash", line_color="#555555", line_width=1.5, opacity=0.8)
    fig.add_vline(x=0.5, line_dash="dash", line_color="#555555", line_width=1.5, opacity=0.8)

    # FIX 1 (continued): add xanchor and yanchor so right-side labels stay
    # pinned inside their quadrant regardless of colorbar width.
    for qname, qinfo in QUADRANTS.items():
        is_selected = (qname == selected_quadrant)
        lx, ly = label_positions[qname]
        fig.add_annotation(
            x=lx, y=ly,
            text=f"<b>{qinfo['label']}</b>" + (" ✔" if is_selected else ""),
            xref="paper", yref="paper", showarrow=False,
            xanchor=label_xanchor[qname],
            yanchor="top" if ly > 0.5 else "bottom",
            font=dict(size=13 if is_selected else 11, color=qinfo["text_color"]),
            opacity=1.0 if is_selected else 0.75,
        )

    title_suffix = f"  ·  Selected: {QUADRANTS[selected_quadrant]['label']}" if (selected_quadrant and selected_quadrant in QUADRANTS) else ""
    fig.update_layout(
        height=420, margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(range=[0, 1], title="Valence (Sadness → Happiness)"),
        yaxis=dict(range=[0, 1], title="Energy (Calm → Intense)"),
        title=f"Mood Map  —  {len(data):,} songs{title_suffix}",
        plot_bgcolor="white", paper_bgcolor="white", clickmode="event", dragmode=False,
    )
    return fig

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
                            choices=genre_choices,
                            selected="All",
                        ),
                    ),
                    open=["Audio Features", "Track Properties"],
                ),
                ui.hr(),
                ui.output_ui("active_quadrant_badge"),
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
                ui.card_header(
                    ui.div(
                        "Mood Map — Valence vs Energy",
                        ui.span(
                            "Click on any quadrant to filter data, then click Cancel again.",
                            style="font-size:0.75rem; color:#6c757d; font-weight:normal;"
                        ),
                    )
                ),
                ui.output_ui("plot_mood_map"),

                # FIX 2: Hide the internal text input so it doesn't render
                # as a visible empty box, causing white space below the chart.
                ui.div(
                    ui.input_text("clicked_quadrant_raw", label="", value=""),
                    style="display:none;",
                ),

                ui.tags.script(ui.HTML("""
                    function attachQuadrantClick() {
                        var moodDiv = document.getElementById('plot_mood_map');
                        if (!moodDiv) return;
                        var plotlyDiv = moodDiv.querySelector('.plotly-graph-div');
                        if (!plotlyDiv || !plotlyDiv._fullLayout) return;
                        plotlyDiv.removeAllListeners('plotly_click');
                        plotlyDiv.on('plotly_click', function(data) {
                            var point = data.points[0];
                            if (!point.data.name || !point.data.name.startsWith('quadrant_')) return;
                            var quadrant = point.data.name.replace('quadrant_', '');
                            var inputEl = document.getElementById('clicked_quadrant_raw');
                            if (inputEl) {
                                inputEl.value = (inputEl.value === quadrant) ? '' : quadrant;
                                inputEl.dispatchEvent(new Event('input', { bubbles: true }));
                                inputEl.dispatchEvent(new Event('change', { bubbles: true }));
                            }
                        });
                    }
                    document.addEventListener('DOMContentLoaded', function() {
                        setInterval(attachQuadrantClick, 500);
                    });
                """)),
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

        ui.tags.style("""
            .bslib-sidebar-layout > .sidebar {
                height: calc(100vh - 80px);
                overflow-y: auto;
                position: sticky;
                top: 60px;
            }
        """),

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

            # Filtered dataframe table
            ui.card(
                ui.card_header("Filtered Songs"),
                ui.output_data_frame("ai_tbl_results"),
                full_screen=True,
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

    qc_state = qc.server()

    clicked_quadrant = reactive.value("")

    @reactive.effect
    def _sync_quadrant():
        raw = input.clicked_quadrant_raw()
        clicked_quadrant.set(raw if raw else "")

    @reactive.calc
    def filtered_query():
        q = songs.filter(
            songs.danceability.between(input.danceability()[0], input.danceability()[1]) &
            songs.energy.between(input.energy()[0], input.energy()[1]) &
            songs.valence.between(input.valence()[0], input.valence()[1]) &
            songs.acousticness.between(input.acousticness()[0], input.acousticness()[1]) &
            songs.tempo.between(input.tempo()[0], input.tempo()[1]) &
            songs.duration_s.between(input.duration_s()[0], input.duration_s()[1]) &
            songs.track_popularity.between(input.popularity()[0], input.popularity()[1])
        )

        if input.genre_filter() != "All":
            q = q.filter(songs.playlist_genre == input.genre_filter())

        qname = clicked_quadrant()
        if qname and qname in QUADRANTS:
            qinfo = QUADRANTS[qname]
            q = q.filter(
                songs.valence >= qinfo["v"][0],
                songs.valence < qinfo["v"][1],
                songs.energy >= qinfo["e"][0],
                songs.energy < qinfo["e"][1],
            )

        return q

    @reactive.calc
    def filtered_df():
        return filtered_query().to_pandas()

    @reactive.calc
    def filtered_summary():
        q = filtered_query()
        summary = q.aggregate(
            n=q.count(),
            avg_energy=q.energy.mean(),
            avg_danceability=q.danceability.mean(),
        )
        return summary.to_pandas().iloc[0]

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
        ui.update_text("clicked_quadrant_raw", value="")
        clicked_quadrant.set("")

    @render.ui
    def active_quadrant_badge():
        qname = clicked_quadrant()
        if not qname or qname not in QUADRANTS:
            return ui.p(ui.tags.em("No quadrant selected"),
                        style="font-size:0.8rem; color:#6c757d; margin:0;")
        qinfo = QUADRANTS[qname]
        return ui.div(
            ui.span("Mood quadrant filter active:", style="font-size:0.8rem; color:#495057;"),
            ui.br(),
            ui.span(qinfo["label"], class_="badge",
                    style=f"font-size:0.85rem; background-color:{qinfo['text_color']}; color:white; padding:4px 8px; border-radius:4px;"),
            ui.p(ui.tags.em("Click the same quadrant again to deselect, or click 'Reset Filters'"),
                style="font-size:0.75rem; color:#6c757d; margin-top:4px;"),
        )

    @render.text
    def kpi_count():
        s = filtered_summary()
        return f"{int(s['n']):,} songs"

    @render.text
    def kpi_energy():
        s = filtered_summary()
        if pd.isna(s["avg_energy"]):
            return "—"
        return f"{s['avg_energy']:.0%}"

    @render.text
    def kpi_dance():
        s = filtered_summary()
        if pd.isna(s["avg_danceability"]):
            return "—"
        return f"{s['avg_danceability']:.0%}"

    @render.ui
    def plot_mood_map():
        data = filtered_df()
        if data.empty:
            return ui.p("No songs match filters", style="text-align:center; padding:2rem;")
        fig = build_mood_map(data, selected_quadrant=clicked_quadrant())
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
        return render.DataGrid(data, height="100%", width="100%", styles=styles)

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
        return render.DataGrid(data, height="100%", width="100%", styles=styles)

    @render.download(filename="spotifind_ai_filtered.csv")
    def download_ai_data():
        yield ai_filtered_df().to_csv(index=False)

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
        for x, y, text, color, xanchor in [
            (0.02, 0.98, "Sad & Intense",   "#2a5fa5", "left"),
            (0.97, 0.98, "Happy & Intense", "#a57a2a", "right"),
            (0.02, 0.02, "Sad & Calm",      "#6a2aa5", "left"),
            (0.97, 0.02, "Happy & Calm",    "#2aa55a", "right"),
        ]:
            fig.add_annotation(
                x=x, y=y, text=f"<b>{text}</b>",
                xref="paper", yref="paper", showarrow=False,
                xanchor=xanchor,
                yanchor="top" if y > 0.5 else "bottom",
                font=dict(size=11, color=color), opacity=0.75,
            )
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
