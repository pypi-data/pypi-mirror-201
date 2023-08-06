import typer
import rich
import json
import sys
import re

from pathlib import Path
from rich.table import Table
from rich.rule import Rule

from yamlup import SetupFile, cerr, cout
from yamlup import cli
from ix_cli import cli as ix

import typer
import rich
import json
import sys
import re

from pathlib import Path
from rich.table import Table
from rich.rule import Rule

from .display import setupRun
from .build import build, build_save, build_upload

app = typer.Typer(
    name="yamlrun",
    help=f"A small CLI that's packaged with the yaml-scripts lib",
    no_args_is_help=True,
    rich_help_panel="rich",
    rich_markup_mode="rich",
)

script = typer.Typer(
    name="script",
    help=f"The scripts maker",
    no_args_is_help=True,
    rich_help_panel="rich",
    rich_markup_mode="rich",
)

app.add_typer(cli.app, name="setup")
app.add_typer(script, name="script")
app.add_typer(ix.app, name='upload')

@script.command("tasks", help="Lists tasks which are declared in the setup file.")
def tasks(
    setupfile: Path = typer.Argument(
        ...,
        help="The YAML setup file",
        )
    ):
    setup = SetupFile(setupfile)
    cout.print(f"Tasks listed in [yellow]{setup.path}[/yellow]:")
    
    fmt = '[magenta]\n --> [/magenta]'.join(setup.tasks())
    cout.print('[magenta]\n --> [/magenta]' + fmt, style='cyan')

@script.command("task-plan", help="Display the task running schedule in the console.")
def task_summary(
    task: str = typer.Argument(
        ...,
        help="The task for which to display the intended build steps"
    ),
    setupfile: Path = typer.Argument(
        ...,
        help="The YAML setup file",
        ),
    ):
    setup = SetupFile(setupfile)
    cout.print(Rule("Task Identification"))
    if task in setup.tasks():
        cout.print("[bold magenta]🤖 Task {task} chosen[/bold magenta], presence [green]confirmed ✅[/green] in the setup file.")
        cout.print(f"[dim] Setup file location: [yellow]{setup.path}[/yellow][/dim]")
    else:
        cout.print("[bold magenta]🤖 Task {task} chosen[/bold magenta], [red]absent ❌[/green] from the setup file.")
        cout.print(f"[dim] Setup file location: [yellow]{setup.path}[/yellow][/dim]")
        typer.Exit(0)

    runs = setup.run_order(task)

    cout.print(Rule("Run Order"))

    cout.print("[bold magenta]🤖 Task {task}[/bold magenta] will execute steps in the following order:")

    jpat = '\n -->'

    fmt = jpat + jpat.join(runs)

    cout.print(Rule("Detail of each step"))

    treeRunDetail = setupRun(setup, task)

    cout.print(treeRunDetail)

@script.command('build', help="Build as powershell script out of the YAML setup file.",
    no_args_is_help=True
    )
def build_pwsh(
    task: str = typer.Argument(
        ...,
        help="The task (high level setup group) you wish to build a script for",

    ),
    setupfile: Path = typer.Argument(
        ...,
        help="The YAML setup file",
        ),
    outfile: Path = typer.Option(
        None, '-o', '--out-file',
        help="The YAML setup file",
        file_okay=True,
        )
    ):
    setup = SetupFile(setupfile)
    if not outfile:
        outfile = Path().cwd() / 'setup.ps1'
    cout.print('🤖 Building script ..', style="bold magenta")
    build_save(setup, task=task, outpath=outfile)

    cout.print(f'✅ Done building script for [yellow]task {task} 🚀[/yellow]', style="bold green")
    cout.print(f'👉 [yellow] Script location: [/yellow]{outfile.absolute()}')


@script.command('BOL', help="Alias for  [magenta]`build-one-liner` [/magenta]",
    no_args_is_help=True
    )
def BOL_pwsh(
    task: str = typer.Argument(
        ...,
        help="The task (high level setup group) you wish to build a script for",

    ),
    setupfile: Path = typer.Argument(
        ...,
        help="The YAML setup file",
        ),
    outfile: Path = typer.Option(
        None, '-o', '--out-file',
        help="The YAML setup file",
        file_okay=True,
        )
    ):
    """One-liner script install. This script is equivalent to:

    - Building the PS1 core script [magenta]`yamlrun script build <task> <path/to/setup.yml>`[/magenta]
    - Uploading the PS1 core script [magenta]`yamlrun upload f <path/to/setup.ps1>`[/magenta]
    - The previous step [red]should give you an URL[/red] of the kind [yellow]`http://ix.io/[letters or numbers]`[/yellow]
    - Your resulting one liner is just:
    `[magenta]Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force ; irm <url> | iex`[/magenta]
    """
    setup = SetupFile(setupfile)
    if not outfile:
        outfile = Path().cwd() / 'setup.ps1'
    cout.print('🤖 Building script + one-liner (😎) ..', style="bold magenta")
    oneliner = build_upload(setup, task=task, outpath=outfile)

    cout.print(f'✅ Done building one liner for [yellow]task {task} 🚀[/yellow]', style="bold green")
    cout.print(f'👉 [yellow] Script location: [/yellow]{outfile.absolute()}', style="dim")
    cout.print(f'👉 [yellow] One-liner location: [/yellow]{outfile.parent / "one_liner.txt"}', style="dim")
    cout.print(f'\n')
    cout.print(f'Your one liner is:', style="bold green")
    cout.print(oneliner, style='magenta')


@script.command(
    'build-one-liner',
    help="Builds the script using the [magenta]`build`[/magenta] command, then uploads the script to ix.io, and gives you [bold yellow]a one-liner command line to install everything.[/bold yellow]",
    no_args_is_help=True
    )
def build_pwsh_oneliner(
    task: str = typer.Argument(
        ...,
        help="The task (high level setup group) you wish to build a script for",

    ),
    setupfile: Path = typer.Argument(
        ...,
        help="The YAML setup file",
        ),
    outfile: Path = typer.Option(
        None, '-o', '--out-file',
        help="The YAML setup file",
        file_okay=True,
        )
    ):
    """One-liner script install. This script is equivalent to:

    - Building the PS1 core script [magenta]`yamlrun script build <task> <path/to/setup.yml>`[/magenta]
    - Uploading the PS1 core script [magenta]`yamlrun upload f <path/to/setup.ps1>`[/magenta]
    - The previous step [red]should give you an URL[/red] of the kind [yellow]`http://ix.io/[letters or numbers]`[/yellow]
    - Your resulting one liner is just:
    `[magenta]Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force ; irm <url> | iex`[/magenta]
    """
    setup = SetupFile(setupfile)
    if not outfile:
        outfile = Path().cwd() / 'setup.ps1'
    cout.print('🤖 Building script + one-liner (😎) ..', style="bold magenta")
    oneliner = build_upload(setup, task=task, outpath=outfile)

    cout.print(f'✅ Done building one liner for [yellow]task {task} 🚀[/yellow]', style="bold green")
    cout.print(f'👉 [yellow] Script location: [/yellow]{outfile.absolute()}', style="dim")
    cout.print(f'👉 [yellow] One-liner location: [/yellow]{outfile.parent / "one_liner.txt"}', style="dim")
    cout.print(f'\n')
    cout.print(f'Your one liner is:', style="bold green")
    cout.print(oneliner, style='magenta')

@app.command("explain", help="Explain this whole thing, alias: `?`")
def explain():
    cout.print(Rule("The setup file"))
    content = """\nThe [blue underline]YAML setup file[/blue underline] (which can also be [blue underline]JSON[/blue underline]), is a way for you to \
describle exactly [bold blue]what type of package/program[/bold blue] you want to auto-install using a [yellow underline]single installer[/yellow underline].    
    """
    cout.print(content)
    cout.print(Rule("[bold magenta]File structure[/bold magenta]", style="magenta"))
    content = """
    The file is structured in the following way:
    
    <task name 1>:
        description: <textual description if you wish, [bold green]OPTIONAL[/bold green]>
        items:
            <item name 1>:
                description: <textual description if you wish, [bold green]OPTIONAL[/bold green]>
                type: <type description, if it's a CLI, GUI, what purpose, [bold red]REQUIRED[/bold red]>
                priority: <how important it is to install it within the setup [bold red]REQUIRED[/bold red]>
                commands:
                    - [magenta]<powershell line 1>[/magenta]
                    - [magenta]<powershell line 2>[/magenta]
            <item name 2>:
                [dim]...[/dim]
            <item name 3>:
                [dim]...[/dim]
        run:
            [dim green]# order in which the items are going to be installed[/dim green]
            steps:
                - <item name 1>
                - <item name 3> [dim green]# look you just swapped the order !
                - <item name 2>
    <task name 2>:
        [dim]...[/dim]
    <task name 3>:
        [dim]...[/dim]
    """
    cout.print(content)
    cout.print(Rule("Script & Executable Builder"))
    content = """Two options:

    (1) One-liner script install. This script is equivalent to:

    - Building the PS1 core script [magenta]`yamlrun script build <task> <path/to/setup.yml>`[/magenta]
    - Uploading the PS1 core script [magenta]`yamlrun upload f <path/to/setup.ps1>`[/magenta]
    - The previous step [red]should give you an URL[/red] of the kind [yellow underline]http://ix.io/<letters or numbers>[/yellow underline]
    - Your resulting one liner is just:
    `[magenta]Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force ; irm <url> | iex`[/magenta]
    
    this is the `yamlrun script BOL` or `yamlrun script build-one-liner` command.

    (2) Doing any of the steps above on its own. 
    """
    cout.print(content)

@app.command("?", help="Explain this whole thing, alias of: `explain`", hidden=True)
def what():
    explain()

if __name__ == "__main__":
    app()
