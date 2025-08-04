import asyncio

from bleprinter import Printer

from morningsummary.events import events
from morningsummary.header import subtitle, title
from morningsummary.messages import messages
from morningsummary.todos import todos


def main() -> None:
    p = Printer()

    p.textln(title(), size=4, bold=True, centered=True)
    p.textln(subtitle(), size=2, centered=True)

    messages(p)
    todos(p)
    events(p)

    asyncio.run(p.cut())
