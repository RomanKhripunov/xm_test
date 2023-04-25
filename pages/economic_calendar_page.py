import re
from enum import Enum

from playwright.sync_api import Page, Locator, expect

from constants import BASE_URL


class SliderPeriods(Enum):
    Recent = 0, "Recent & Next"
    Today = 1, "Today"
    Tomorrow = 2, "Tomorrow"
    ThisWeek = 3, "This Week"
    NextWeek = 4, "Next Week"
    ThisMonth = 5, "This Month"
    NextMonth = 6, "Next Month"

    def __new__(cls, value, string_value):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.str_value = string_value
        return obj


class EconomicCalendarPage:
    URL = BASE_URL
    URL_PATH = "research/economicCalendar"

    def __init__(self, page: Page):
        self.page = page
        self.econ_frame = self.page.frame_locator('#iFrameResizer0')

        self.tb_header_row = self.econ_frame.locator('div.tc-economic-calendar-item-header')
        self.tb_event_row = self.econ_frame.locator('tc-economic-calendar-row')
        self.past_events_btn = self.econ_frame.get_by_role('button').filter(has_text="Past Events")

        self.calendar_header = self.econ_frame.locator('div.mat-calendar-header')
        self.prev_month_btn = self.calendar_header.locator("button.mat-calendar-previous-button")
        self.next_month_btn = self.calendar_header.locator("button.mat-calendar-next-button")

        self.calendar_body = self.econ_frame.locator('tbody.mat-calendar-body')
        self.month_short_name = self.calendar_body.locator('td.mat-calendar-body-label').filter(
            has_text=re.compile(r"\w")
        )

    def load(self) -> None:
        self.page.goto(f"{self.URL}/{self.URL_PATH}")

    def calendar_day_locator(self, day: int | str) -> Locator:
        return self.calendar_body.get_by_role("gridcell").filter(
            has_text=re.compile(fr"\s{day}\s")).get_by_role('button')

    def select_period(self, period: SliderPeriods = SliderPeriods.Today) -> None:
        slider = self.econ_frame.get_by_role("slider")
        slider.focus()

        slider_max_tick_ind = slider.get_attribute('aria-valuemax')
        assert (slider_max_tick_ind == (len(SliderPeriods) - 1), "Slider has ticks more than we expect")

        slider.click(position=self._calc_period_position(slider, period))
        expect(self.econ_frame.locator('span.tc-finalval-tmz')).to_have_text(re.compile(period.str_value))

    @staticmethod
    def _calc_period_position(slider: Locator, period: SliderPeriods) -> dict:
        slider_box = slider.bounding_box()
        tick_step = slider_box['width'] / (len(SliderPeriods) - 1)

        periods_ticks = [0]
        for i in range(1, len(SliderPeriods) - 1):
            position = tick_step * i
            periods_ticks.append(position)
        periods_ticks.append(slider_box['width'] - 1)  # Hack to avoid click out of the box

        return {
            'x': periods_ticks[period.value],
            'y': slider_box['height'] / 2
        }
