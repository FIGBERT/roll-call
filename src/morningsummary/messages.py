from os import path
from datetime import datetime, date, time, timedelta
from typing import Final
from imessage_reader import fetch_data

APPLE_DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"


def messages() -> str:
    text = "MESSAGES\n"

    db = fetch_data.FetchData(path.expanduser("~/Library/Messages/chat.db"))
    messages = filter_messages(db.get_messages())
    grouped = group_messages(messages)

    for sender in grouped:
        text += f"{sender}\n"
        for msg in grouped[sender]:
            text += f"\t{msg[1]}\n"

    return text.strip()


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
