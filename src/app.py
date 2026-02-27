from shiny import App, ui, render
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/raw/spotify_songs.csv") 
numeric_columns = df.select_dtypes(include="number").columns.tolist()

app_ui = ui.page_fillable(
    ui.panel_title("SPOTIFIND"),
    ui.layout_sidebar(
        ui.sidebar("Filter control", open="desktop"),
        
        ui.layout_columns(
            ui.card(ui.card_header("Results tables"), full_screen=True),
        ),
        ui.layout_columns(
            ui.value_box(
                "Drop down",
                ui.input_select("x_var", "Select X-axis", choices=numeric_columns),
                ui.input_select("y_var", "Select Y-axis", choices=numeric_columns),
            ),
            ui.card(ui.card_header("Top genre")),
            fill=False,
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Scatter plot"),
                ui.output_plot("scatter_plot"),
                full_screen=True),
            ui.card(ui.card_header("Song search"), full_screen=True),
            col_widths=[6, 6],
        ),
    ),
)

def server(input, output, session):
   
    @output
    @render.plot
    def scatter_plot():
        x = input.x_var()
        y = input.y_var()

        fig, ax = plt.subplots()
        ax.scatter(df[x], df[y])
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title(f"{x} vs {y}")

        return fig

app = App(app_ui, server)