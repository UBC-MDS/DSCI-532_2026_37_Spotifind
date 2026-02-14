from shiny import App, ui

app_ui = ui.page_fillable(
    ui.panel_title("SPOTIFIND"),
    ui.layout_sidebar(
        ui.sidebar("Filter control", open="desktop"),
        
        ui.layout_columns(
            ui.card(ui.card_header("Results tables"), full_screen=True),
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
    ),
)

def server(input, output, session):
    pass

app = App(app_ui, server)