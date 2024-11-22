from morningsummary.header import title, subtitle
from morningsummary.todos import todos
from morningsummary.events import events
from morningsummary.messages import messages


def main() -> None:
    print(title())
    print(subtitle())
    print()
    print(messages())
    print()
    print(todos())
    print()
    print(events())
