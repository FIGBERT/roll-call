import things
from bleprinter import Printer


def todos(printer: Printer) -> None:
    printer.textln("TODOS", size=2, bold=True)

    tasks = things.today()

    for task in tasks:
        line = f"[ ] {task['title']}"
        if "heading" in task:
            line += f" ({things.tasks(uuid=task['heading'])['project_title']})"
        elif "project_title" in task:
            line += f" ({task['project_title']})"
        printer.textln(line)
