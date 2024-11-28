from morningsummary.header import title, subtitle
from morningsummary.todos import todos
from morningsummary.events import events
from morningsummary.messages import messages
from escpos.printer import Usb


def main() -> None:
    p = Usb(0x04B8, 0x0E28)

    p.set(align="center", font="b", bold=True, custom_size=True, width=4, height=4)
    p.textln(title())

    p.set(normal_textsize=True)
    p.set(double_height=True, double_width=True)
    p.textln(subtitle())

    p.set(align="left", normal_textsize=True)
    messages(p)
    p.ln()

    todos(p)
    p.ln()

    events(p)
    p.cut()
