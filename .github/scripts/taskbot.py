def sync_tasks():
    for repo in ["core", "signal", "media"]:
        tasks = parse_markdown(f"{repo}/TASKS.md")
        update_kanban(tasks)
