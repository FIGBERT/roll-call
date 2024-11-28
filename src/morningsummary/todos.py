import things
from escpos.printer import Usb


def todos(printer: Usb) -> None:
    printer.set(bold=True, double_width=False, double_height=True)
    printer.textln("TODOS")
    printer.set(normal_textsize=True)

    tasks = things.today()

    for task in tasks:
        line = f"[ ] {task["title"]}"
        if "heading" in task:
            line += f" ({things.tasks(uuid=task["heading"])["project_title"]})"
        elif "project_title" in task:
            line += f" ({task["project_title"]})"
        printer.textln(line)
