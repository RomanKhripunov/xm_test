import calendar
import datetime
import re

from playwright.sync_api import expect

from pages.economic_calendar_page import SliderPeriods


def test_select_today(home_page, economic_calendar_page):
    home_page.load()
    home_page.open_economic_calendar()

    today = datetime.datetime.today()
    today_cld_btn = economic_calendar_page.calendar_day_locator(today.day)

    expect(economic_calendar_page.month_short_name).to_have_text(today.strftime("%b").upper())
    expect(today_cld_btn).to_have_attribute("aria-pressed", "false")
    expect(today_cld_btn).not_to_have_class("mat-calendar-body-selected")
    expect(economic_calendar_page.tb_header_row).not_to_have_count(1)
    expect(economic_calendar_page.past_events_btn).to_be_visible()
    events_before = [str(e) for e in economic_calendar_page.tb_event_row.all()]

    economic_calendar_page.select_period(period=SliderPeriods.Today)

    expect(economic_calendar_page.past_events_btn).not_to_be_visible()
    expect(economic_calendar_page.month_short_name).to_have_text(today.strftime("%b").upper())
    expect(today_cld_btn).to_have_attribute('aria-pressed', 'true')
    expect(today_cld_btn.locator('div.mat-calendar-body-cell-content')).to_have_class(
        re.compile(r"mat-calendar-body-selected"))
    expect(economic_calendar_page.tb_header_row).to_have_count(1)
    expect(economic_calendar_page.tb_header_row).to_have_text(
        re.compile(fr'{today.year} {today.strftime("%b")} {today.strftime("%d")}')
    )
    events_after = [str(e) for e in economic_calendar_page.tb_event_row.all()]

    assert events_before != events_after


def test_select_tomorrow(home_page, economic_calendar_page):
    home_page.load()
    home_page.open_economic_calendar()

    today = datetime.datetime.today()
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow_cld_btn = economic_calendar_page.calendar_day_locator(tomorrow.day)

    expect(economic_calendar_page.month_short_name).to_have_text(today.strftime("%b").upper())
    expect(tomorrow_cld_btn).to_have_attribute('aria-pressed', 'false')
    expect(tomorrow_cld_btn).not_to_have_class(re.compile(r"mat-calendar-body-selected"))
    expect(economic_calendar_page.tb_header_row).not_to_have_count(1)
    expect(economic_calendar_page.past_events_btn).to_be_visible()
    events_before = [str(e) for e in economic_calendar_page.tb_event_row.all()]

    economic_calendar_page.select_period(period=SliderPeriods.Tomorrow)

    expect(economic_calendar_page.past_events_btn).not_to_be_visible()
    expect(economic_calendar_page.month_short_name).to_have_text(tomorrow.strftime("%b").upper())
    expect(tomorrow_cld_btn).to_have_attribute('aria-pressed', 'true')
    expect(tomorrow_cld_btn.locator('div.mat-calendar-body-cell-content')).to_have_class(
        re.compile(r"mat-calendar-body-selected"))
    expect(economic_calendar_page.tb_header_row).to_have_count(1)
    expect(economic_calendar_page.tb_header_row).to_have_text(
        re.compile(fr'{tomorrow.year} {tomorrow.strftime("%b")} {tomorrow.strftime("%d")}')
    )
    events_after = [str(e) for e in economic_calendar_page.tb_event_row.all()]

    assert events_before != events_after


def test_select_this_week(home_page, economic_calendar_page):
    home_page.load()
    home_page.open_economic_calendar()

    today = datetime.datetime.today()
    start_this_week_day = today - datetime.timedelta(days=today.weekday())
    end_this_week_day = start_this_week_day + datetime.timedelta(days=6)

    this_month_days = []
    next_month_days = []
    for day in [start_this_week_day + datetime.timedelta(days=i) for i in range(7)]:
        if day.month == today.month:
            this_month_days.append(day)
        else:
            next_month_days.append(day)

    start_cld_btn = economic_calendar_page.calendar_day_locator(start_this_week_day.day)
    end_cld_btn = economic_calendar_page.calendar_day_locator(end_this_week_day.day)

    expect(economic_calendar_page.month_short_name).to_have_text(today.strftime("%b").upper())
    expect(economic_calendar_page.tb_header_row).not_to_have_count(1)
    expect(economic_calendar_page.past_events_btn).to_be_visible()
    events_before = [str(e) for e in economic_calendar_page.tb_event_row.all()]

    economic_calendar_page.select_period(period=SliderPeriods.ThisWeek)

    expect(economic_calendar_page.past_events_btn).not_to_be_visible()
    expect(economic_calendar_page.month_short_name).to_have_text(start_this_week_day.strftime("%b").upper())
    expect(start_cld_btn).to_have_attribute('aria-pressed', 'true')
    expect(start_cld_btn.locator('div.mat-calendar-body-cell-content')).to_have_class(
        re.compile(r"mat-calendar-body-selected")
    )
    expect(economic_calendar_page.tb_header_row.first).to_have_text(
        re.compile(fr'{start_this_week_day.year} '
                   fr'{start_this_week_day.strftime("%b")} '
                   fr'{start_this_week_day.strftime("%d")}')
    )

    for d in this_month_days:
        day_locator = economic_calendar_page.calendar_day_locator(d.day)
        expect(day_locator).to_have_class(re.compile(r"mat-calendar-body-in-range"))

    expect(start_cld_btn).to_have_class(re.compile(r"mat-calendar-body-range-start"))
    expect(start_cld_btn).to_have_class(re.compile(r"mat-calendar-body-in-range"))

    if next_month_days:
        economic_calendar_page.next_month_btn.click()

    for d in next_month_days:
        day_locator = economic_calendar_page.calendar_day_locator(d.day)
        expect(day_locator).to_have_class(re.compile(r"mat-calendar-body-in-range"))

    expect(economic_calendar_page.month_short_name).to_have_text(end_this_week_day.strftime("%b").upper())
    expect(end_cld_btn).to_have_attribute('aria-pressed', 'true')
    expect(end_cld_btn.locator('div.mat-calendar-body-cell-content')).to_have_class(
        re.compile(r"mat-calendar-body-selected")
    )
    expect(end_cld_btn).to_have_class(re.compile(r"mat-calendar-body-range-end"))
    expect(end_cld_btn).to_have_class(re.compile(r"mat-calendar-body-in-range"))

    events_after = [str(e) for e in economic_calendar_page.tb_event_row.all()]

    assert events_before != events_after


def test_select_next_week(home_page, economic_calendar_page):
    home_page.load()
    home_page.open_economic_calendar()

    today = datetime.datetime.today()
    start_next_week_day = today + datetime.timedelta(days=7 - today.weekday())
    end_next_week_day = start_next_week_day + datetime.timedelta(days=6)

    this_month_days = []
    next_month_days = []
    for day in [start_next_week_day + datetime.timedelta(days=i) for i in range(7)]:
        if day.month == today.month:
            this_month_days.append(day)
        else:
            next_month_days.append(day)

    start_cld_btn = economic_calendar_page.calendar_day_locator(start_next_week_day.day)
    end_cld_btn = economic_calendar_page.calendar_day_locator(end_next_week_day.day)

    expect(economic_calendar_page.month_short_name).to_have_text(today.strftime("%b").upper())
    expect(economic_calendar_page.tb_header_row).not_to_have_count(1)
    expect(economic_calendar_page.past_events_btn).to_be_visible()
    events_before = [str(e) for e in economic_calendar_page.tb_event_row.all()]

    economic_calendar_page.select_period(period=SliderPeriods.NextWeek)

    expect(economic_calendar_page.past_events_btn).not_to_be_visible()
    expect(economic_calendar_page.month_short_name).to_have_text(start_next_week_day.strftime("%b").upper())
    expect(start_cld_btn).to_have_attribute('aria-pressed', 'true')
    expect(start_cld_btn.locator('div.mat-calendar-body-cell-content')).to_have_class(
        re.compile(r"mat-calendar-body-selected")
    )
    expect(economic_calendar_page.tb_header_row.first).to_have_text(
        re.compile(fr'{start_next_week_day.year} '
                   fr'{start_next_week_day.strftime("%b")} '
                   fr'{start_next_week_day.strftime("%d")}')
    )

    for d in this_month_days:
        day_locator = economic_calendar_page.calendar_day_locator(d.day)
        expect(day_locator).to_have_class(re.compile(r"mat-calendar-body-in-range"))

    expect(start_cld_btn).to_have_class(re.compile(r"mat-calendar-body-range-start"))
    expect(start_cld_btn).to_have_class(re.compile(r"mat-calendar-body-in-range"))

    if this_month_days and next_month_days:
        economic_calendar_page.next_month_btn.click()

    for d in next_month_days:
        day_locator = economic_calendar_page.calendar_day_locator(d.day)
        expect(day_locator).to_have_class(re.compile(r"mat-calendar-body-in-range"))

    expect(economic_calendar_page.month_short_name).to_have_text(end_next_week_day.strftime("%b").upper())
    expect(end_cld_btn).to_have_attribute('aria-pressed', 'true')
    expect(end_cld_btn.locator('div.mat-calendar-body-cell-content')).to_have_class(
        re.compile(r"mat-calendar-body-selected")
    )
    expect(end_cld_btn).to_have_class(re.compile(r"mat-calendar-body-range-end"))
    expect(end_cld_btn).to_have_class(re.compile(r"mat-calendar-body-in-range"))

    events_after = [str(e) for e in economic_calendar_page.tb_event_row.all()]

    assert events_before != events_after


def test_select_this_month(home_page, economic_calendar_page):
    home_page.load()
    home_page.open_economic_calendar()

    today = datetime.datetime.today()
    this_month_days = calendar.monthrange(today.year, today.month)[1]

    start_cld_btn = economic_calendar_page.calendar_day_locator(1)
    end_cld_btn = economic_calendar_page.calendar_day_locator(this_month_days)

    expect(economic_calendar_page.month_short_name).to_have_text(today.strftime("%b").upper())
    expect(economic_calendar_page.tb_header_row).not_to_have_count(1)
    expect(economic_calendar_page.past_events_btn).to_be_visible()
    events_before = [str(e) for e in economic_calendar_page.tb_event_row.all()]

    economic_calendar_page.select_period(period=SliderPeriods.ThisMonth)

    expect(economic_calendar_page.past_events_btn).not_to_be_visible()
    expect(economic_calendar_page.month_short_name).to_have_text(today.strftime("%b").upper())
    expect(start_cld_btn).to_have_attribute('aria-pressed', 'true')
    expect(start_cld_btn.locator('div.mat-calendar-body-cell-content')).to_have_class(
        re.compile(r"mat-calendar-body-selected")
    )
    expect(economic_calendar_page.tb_header_row.first).to_have_text(
        re.compile(fr'{today.year} {today.strftime("%b")} 01')
    )

    for d in range(1, this_month_days + 1):
        day_locator = economic_calendar_page.calendar_day_locator(d)
        expect(day_locator).to_have_class(re.compile(r"mat-calendar-body-in-range"))

    expect(start_cld_btn).to_have_class(re.compile(r"mat-calendar-body-range-start"))
    expect(start_cld_btn).to_have_class(re.compile(r"mat-calendar-body-in-range"))

    expect(end_cld_btn).to_have_attribute('aria-pressed', 'true')
    expect(end_cld_btn.locator('div.mat-calendar-body-cell-content')).to_have_class(
        re.compile(r"mat-calendar-body-selected")
    )
    expect(end_cld_btn).to_have_class(re.compile(r"mat-calendar-body-range-end"))
    expect(end_cld_btn).to_have_class(re.compile(r"mat-calendar-body-in-range"))

    events_after = [str(e) for e in economic_calendar_page.tb_event_row.all()]

    assert events_before != events_after


def test_select_next_month(home_page, economic_calendar_page):
    home_page.load()
    home_page.open_economic_calendar()

    today = datetime.datetime.today()

    next_month_some_day = today.replace(day=1) + datetime.timedelta(days=32)
    next_month_days = calendar.monthrange(next_month_some_day.year, next_month_some_day.month)[1]

    start_cld_btn = economic_calendar_page.calendar_day_locator(1)
    end_cld_btn = economic_calendar_page.calendar_day_locator(next_month_days)

    expect(economic_calendar_page.month_short_name).to_have_text(today.strftime("%b").upper())
    expect(economic_calendar_page.tb_header_row).not_to_have_count(1)
    expect(economic_calendar_page.past_events_btn).to_be_visible()
    events_before = [str(e) for e in economic_calendar_page.tb_event_row.all()]

    economic_calendar_page.select_period(period=SliderPeriods.NextMonth)

    expect(economic_calendar_page.past_events_btn).not_to_be_visible()
    expect(economic_calendar_page.month_short_name).not_to_have_text(today.strftime("%b").upper())
    expect(economic_calendar_page.month_short_name).to_have_text(next_month_some_day.strftime("%b").upper())
    expect(start_cld_btn).to_have_attribute('aria-pressed', 'true')
    expect(start_cld_btn.locator('div.mat-calendar-body-cell-content')).to_have_class(
        re.compile(r"mat-calendar-body-selected")
    )
    expect(economic_calendar_page.tb_header_row.first).to_have_text(
        re.compile(fr'{next_month_some_day.year} {next_month_some_day.strftime("%b")} 01')
    )

    for d in range(1, next_month_days + 1):
        day_locator = economic_calendar_page.calendar_day_locator(d)
        expect(day_locator).to_have_class(re.compile(r"mat-calendar-body-in-range"))

    expect(start_cld_btn).to_have_class(re.compile(r"mat-calendar-body-range-start"))
    expect(start_cld_btn).to_have_class(re.compile(r"mat-calendar-body-in-range"))

    expect(end_cld_btn).to_have_attribute('aria-pressed', 'true')
    expect(end_cld_btn.locator('div.mat-calendar-body-cell-content')).to_have_class(
        re.compile(r"mat-calendar-body-selected")
    )
    expect(end_cld_btn).to_have_class(re.compile(r"mat-calendar-body-range-end"))
    expect(end_cld_btn).to_have_class(re.compile(r"mat-calendar-body-in-range"))

    events_after = [str(e) for e in economic_calendar_page.tb_event_row.all()]

    assert events_before != events_after
