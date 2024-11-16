from morningsummary.header import title, subtitle
from morningsummary.todos import todos


def main() -> None:
    print(title())
    print(subtitle())
    print()
    print(todos())
