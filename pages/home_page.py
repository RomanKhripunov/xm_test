import re

from playwright.sync_api import expect, Page

from constants import BASE_URL
from pages.economic_calendar_page import EconomicCalendarPage


class HomePage:
    URL = BASE_URL

    def __init__(self, page: Page):
        self.page = page

    def load(self, skip_privacy_dialog: bool = True) -> None:
        self.page.goto(self.URL)

        if skip_privacy_dialog:
            privacy_modal = self.page.locator("div.modal-dialog")
            self.page.locator('button.gtm-acceptDefaultCookieFirstVisit').click(timeout=3000, no_wait_after=True)
            expect(privacy_modal).not_to_be_visible()

    def open_economic_calendar(self):
        research_nav = self.page.locator("li.main_nav_research")
        research_nav.click()
        expect(research_nav).to_have_class(re.compile(r"selected"))

        research_dropdown = research_nav.locator("div.dropdown")
        expect(research_dropdown).to_be_visible()
        expect(research_dropdown).to_have_css("display", "block")

        economic_calendar = research_dropdown.locator("li.menu-research").filter(has_text="Economic Calendar")
        economic_calendar.click()
        self.page.wait_for_load_state()
        expect(self.page).to_have_url(re.compile(fr".*{EconomicCalendarPage.URL_PATH}"))
