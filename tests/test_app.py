from shiny.playwright import controller
from shiny.run import ShinyAppProc
from playwright.sync_api import Page
from shiny.pytest import create_app_fixture

app = create_app_fixture("../src/app.py")

def test_value_boxes(page: Page, app: ShinyAppProc) -> None:
    """All three value boxes show correct stats for the full dataset."""
    page.goto(app.url)
    page.wait_for_load_state("networkidle") #if test fails try that
    page.wait_for_load_state("networkidle") #or that

    controller.OutputText(page, "kpi_count").expect_value("28,356 songs")
    controller.OutputText(page, "kpi_energy").expect_value("0.70 / 1.0")
    controller.OutputText(page, "kpi_dance").expect_value("0.65 / 1.0")

def test_genre_choosing_change_value_box(page: Page, app: ShinyAppProc) -> None:
    """Choosing different genre should change the dislay value of value box"""
    page.goto(app.url)
    page.wait_for_load_state("networkidle") #if test fails try that
    page.wait_for_load_state("networkidle") #or that

    page.select_option("select#genre_filter", "pop")
    controller.OutputText(page, "kpi_count").expect_value("5,132 songs")
    controller.OutputText(page, "kpi_energy").expect_value("0.70 / 1.0")
    controller.OutputText(page, "kpi_dance").expect_value("0.64 / 1.0")

def test_webpage_not_crash_if_no_song_return_due_to_filter(page: Page, app: ShinyAppProc) -> None:
    """When change a filter that the result is O songs (super extreme filter value), the web-page should still work normally and not crashing."""
    page.goto(app.url)

    page.select_option("select#genre_filter", "latin")
    page.wait_for_load_state("networkidle") #if test fails try that
    page.wait_for_load_state("networkidle") #or that

    slider = controller.InputSliderRange(page, "duration_s")
    slider.set(("3","3"), max_err_values=15)
    controller.OutputText(page, "kpi_count").expect_value("0 songs")
    controller.OutputText(page, "kpi_energy").expect_value("—")
    controller.OutputText(page, "kpi_dance").expect_value("—")

def test_reset_filters_restore_default(page: Page, app: ShinyAppProc) -> None:
    """Reset button should restore the default dataset view and number."""
    page.goto(app.url)

    page.select_option("select#genre_filter", "edm")
    reset_btn = controller.InputActionButton(page, "reset_all")
    reset_btn.click()

    controller.OutputText(page, "kpi_count").expect_value("28,356 songs")
    controller.OutputText(page, "kpi_energy").expect_value("0.70 / 1.0")
    controller.OutputText(page, "kpi_dance").expect_value("0.65 / 1.0")
