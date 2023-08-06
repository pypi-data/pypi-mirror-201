from rich.tree import Tree

__all__ = ["setupRun"]

def setupRun(setup, task):
    items = setup.task_items(task)
    order = setup.run_order(task)
    root = Tree(f"[bold magenta]Task {task} running plan[/bold magenta]")
    for i, rank in enumerate(order):
        step = root.add(f"Step ({i}) = {rank}", style="bold red")
        details = next(filter(lambda itm: itm.get("name") == rank, items)).get("commands")
        for scriptline in details:
            step.add(f"[bold blue] $pwsh [/bold blue][magenta] --> [/magenta] [yellow]{scriptline}[/yellow]")

    return root
