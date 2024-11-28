import os
from datetime import date, datetime, time, timedelta

import caldav
import icalendar
from dotenv import load_dotenv
from escpos.printer import Usb


class SummaryEvent:
    name: str
    start: datetime
    end: datetime

    def __init__(self, name: str, start: datetime, end: datetime):
        self.name = name
        self.start = start
        self.end = end


def events(printer: Usb) -> None:
    printer.set(bold=True, double_width=False, double_height=True)
    printer.textln("CALENDAR")
    printer.set(normal_textsize=True)

    evs: list[SummaryEvent] = []

    _ = load_dotenv()
    CALENDAR_URL = os.getenv("CALENDAR_URL") or ""
    CALENDAR_USER = os.getenv("CALENDAR_USER") or ""
    CALENDAR_PASS = os.getenv("CALENDAR_PASS") or ""

    with caldav.DAVClient(
        url=CALENDAR_URL, username=CALENDAR_USER, password=CALENDAR_PASS
    ) as client:
        principal: caldav.Principal = client.principal()
        calendars = principal.calendars()

        start_of_day = datetime.combine(date.today(), time.fromisoformat("00:00:00"))

        for calendar in calendars:
            events: list[caldav.Event] = calendar.search(
                start=start_of_day,
                end=start_of_day + timedelta(days=1),
                event=True,
                expand=True,
            )

            for event in events:
                ics = icalendar.Event.from_ical(event.data)
                for component in ics.walk():
                    if component.name == "VEVENT":
                        evs.append(
                            SummaryEvent(
                                component.get("summary"),
                                component.get("dtstart").dt,
                                component.get("dtend").dt,
                            )
                        )
                        continue

    evs.sort(key=lambda ev: ev.start)

    for ev in evs:
        printer.textln(
            f"{ev.start.strftime("%H:%M")}-{ev.end.strftime("%H:%M")} {ev.name}"
        )
