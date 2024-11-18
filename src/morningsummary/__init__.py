from morningsummary.header import title, subtitle
from morningsummary.todos import todos
from morningsummary.events import events


def main() -> None:
    print(title())
    print(subtitle())
    print()
    print(todos())
    print()
    print(events())
