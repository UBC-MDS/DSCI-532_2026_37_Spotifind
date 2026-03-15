from shiny.playwright import controller
from shiny.run import ShinyAppProc
from playwright.sync_api import Page
from shiny.pytest import create_app_fixture

app = create_app_fixture("../src/app.py")

def test_value_boxes(page: Page, app: ShinyAppProc) -> None:
    """All three value boxes show correct stats for the full dataset."""
    page.goto(app.url)
    page.wait_for_load_state("networkidle") #if test fails try that

    controller.OutputText(page, "kpi_count").expect_value("28,356 songs")
    controller.OutputText(page, "kpi_energy").expect_value("70%")
    controller.OutputText(page, "kpi_dance").expect_value("65%")

def test_genre_choosing_change_value_box(page: Page, app: ShinyAppProc) -> None:
    """Choosing different genre should change the dislay value of value box"""
    page.goto(app.url)
    page.wait_for_load_state("networkidle") #if test fails try that

    page.select_option("select#genre_filter", "pop")
    controller.OutputText(page, "kpi_count").expect_value("5,132 songs")
    controller.OutputText(page, "kpi_energy").expect_value("70%")
    controller.OutputText(page, "kpi_dance").expect_value("64%")

def test_webpage_not_crash_if_no_song_return_due_to_filter(page: Page, app: ShinyAppProc) -> None:
    """When change a filter that the result is 0 songs (super extreme filter value), the web-page should still work normally and not crashing."""
    page.goto(app.url)
    page.select_option("select#genre_filter", "latin")
    page.wait_for_load_state("networkidle")
    slider = controller.InputSliderRange(page, "duration_s")
    slider.set(("3", "3"), max_err_values=15)
    slider2 = controller.InputSliderRange(page, "energy")
    slider2.set(("0.9", "0.9"), max_err_values=15)
    page.wait_for_load_state("networkidle")
    controller.OutputText(page, "kpi_count").expect_value("0 songs")
    controller.OutputText(page, "kpi_energy").expect_value("—")
    controller.OutputText(page, "kpi_dance").expect_value("—")
    
def test_reset_filters_restore_default(page: Page, app: ShinyAppProc) -> None:
    """Reset button should restore the default dataset view and number."""
    page.goto(app.url)

    page.wait_for_load_state("networkidle") #if test fails try that

    page.select_option("select#genre_filter", "edm")
    reset_btn = controller.InputActionButton(page, "reset_all")

    page.wait_for_load_state("networkidle") #if test fails try that

    reset_btn.click()
    
    controller.OutputText(page, "kpi_count").expect_value("28,356 songs")
    controller.OutputText(page, "kpi_energy").expect_value("70%")
    controller.OutputText(page, "kpi_dance").expect_value("65%")
