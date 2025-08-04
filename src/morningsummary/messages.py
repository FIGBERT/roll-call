from datetime import date, datetime, time, timedelta
from os import path
from typing import Final

import applescript
from bleprinter import Printer
from imessage_reader import fetch_data

APPLE_DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"


def messages(printer: Printer) -> None:
    printer.textln("MESSAGES", size=2, bold=True)

    db = fetch_data.FetchData(path.expanduser("~/Library/Messages/chat.db"))
    messages = filter_messages(db.get_messages())
    grouped = group_messages(messages)

    for sender in grouped:
        printer.textln(contacts_lookup(sender), underline=True)
        for msg in grouped[sender]:
            printer.textln(msg[1])


def filter_messages(messages: list) -> list:
    out = []
    UNREAD = datetime.strptime("2000-12-31 16:00:00", APPLE_DATE_FORMAT)
    START_CUTOFF = datetime.combine(
        (date.today() - timedelta(days=1)), time.fromisoformat("22:00:00")
    )

    for msg in messages:
        received = datetime.strptime(msg[2], APPLE_DATE_FORMAT)
        if received < START_CUTOFF:
            continue
        is_from_me = msg[5]
        if is_from_me == 1:
            continue
        read_date = datetime.strptime(msg[6], APPLE_DATE_FORMAT)
        if read_date != UNREAD:
            continue
        out.append(msg)

    out.sort(key=lambda msg: datetime.strptime(msg[2], APPLE_DATE_FORMAT))

    return out


def group_messages(messages: list) -> dict[str, list[str]]:
    out = {}

    for msg in messages:
        if msg[0] in out:
            out[msg[0]].append(msg)
        else:
            out[msg[0]] = [msg]

    return out


def contacts_lookup(num: str) -> str:
    num = "".join([n for n in num if n.isdigit()])

    APPLESCRIPT = f"""
    tell application "Contacts"
    set allContacts to every person

    repeat with aContact in allContacts
        set phoneNumbers to value of every phone of aContact
        repeat with aPhoneNumber in phoneNumbers
            set normalizedNumber to ""
            repeat with i from 1 to length of aPhoneNumber
                set char to character i of aPhoneNumber
                if char is in "0123456789" then
                    set normalizedNumber to normalizedNumber & char
                end if
            end repeat
            if normalizedNumber is equal to "{num}" then
                return name of aContact
            end if
            end repeat
        end repeat
    end tell

    return ""
    """

    name = applescript.run(APPLESCRIPT).out

    if name == "":
        return num
    else:
        return name
