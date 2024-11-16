import things


def todos() -> str:
    text = "TODOS\n"
    tasks = things.today()

    for task in tasks:
        text += f"[ ] {task["title"]}"
        if "heading" in task:
            text += f" ({things.tasks(uuid=task["heading"])["project_title"]})"
        elif "project_title" in task:
            text += f" ({task["project_title"]})"
        text += "\n"

    return text.strip()
