from pathlib import Path
from datetime import datetime as dt
from socket import gethostname
from os import getlogin
from sys import platform, exit
from textwrap import wrap
from functools import reduce
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from subprocess import run

from yamlup import cout, cerr
from ix_cli.utils import uploadFromFile

waitSpin = Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}", style="bold cyan"),
    TimeElapsedColumn()
)

__all__ = ["build", "build_save", "compile", "build_upload"]

def make_metadata(i, name):
    line = f'##  Install number ({i}) = {name}  ##'
    filler = '#'*len(line)
    content = filler + '\n' + line + '\n' + filler + '\n\n'
    return content

def _fw(n):
    return n*' '

def check_command(name):
    with waitSpin as pbar:
        pbar.add_task("Checking PS2EXE ..")
        output = run(f'powershell -c $(Get-Command {name} -ErrorAction SilentlyContinue).Length', capture_output=True, shell=True)
    
    if output.returncode != 0:
        return False
    else:
        if output.stdout.isdigit():
            if int(output.stdout):
                return True
            else:
                return False
        else:
            return False
        
def ensure_exe_maker():
    if not check_command("ps2exe"):
        with waitSpin as pbar:
            task = pbar.add_task("Installing PS2EXE ..")
            res = run([
                "powershell", "-c", "Install-Module ps2exe", "-Force", "-AllowClobber"
                ], shell=True, check=True, capture_output=True,
                )
            if res.returncode:
                cerr.log(f"❌📦 Could not install module PS2EXE.", style="bold red")
                cerr.log("👉 Check this link for more info: https://github.com/MScholtes/PS2EXE")
                cerr.log("Error log:", style="red")
                cerr.log(res.stderr.decode(), style="dim red")
                cerr.log(res.stdout.decode(), style="dim")
                pbar.remove_task(task)
                exit(1)
    else:
        cout.print("✅ PS2EXE already installed.", style="green")
        pbar.remove_task(task)

def compile(script: Path, gui:bool = True, suppress: bool = True):
    if not script.exists():
        cerr.log(f"❓ Script cannot be found at [yellow]{script}[/yellow]", style="bold red")
        exit(1)
    else:
        ensure_exe_maker()
        args = [
                "-noConsole", "-noOutput",
                "-noError", "-MTA",
                "-DPIAware", "-winFormsDPIAware"
            ] if not gui else [
                "-UNICODEEncoding"
            ]
        fullpath = script.resolve()
        ps1path = fullpath.with_suffix('.ps1')
        exepath = fullpath.with_suffix('.exe')
        with waitSpin as pbar:
            task = pbar.add_task(f"Compiling [yellow]{script.name} ..")
            compiler = (
                        f""" "Invoke-PS2EXE -inputFile '{fullpath}' """ +
                        f"-outputFile '{exepath}' " +
                        f"-title {script.stem} {' '.join(args)}" +
                        """ " | Invoke-Expression"""
                    )
            
            cout.print(compiler, style='dim')
            res = run(
                [
                    "powershell", "-c", 
                    r'{}'.format(compiler)
                ],
                shell=True,
                capture_output=True
            )
        if res.returncode == 0:
            cout.print(f"✅ Compiled script into [magenta].exe 🤖[/magenta]", style="green")
            cout.print(f"👉 Path to .exe : [dim] {script.resolve().parent / 'online-setup-installer.exe'}[/dim]", style="yellow")
        else:
            cerr.print("❌ Could not create .exe \nError:\n", style="red")
            cerr.print(res.stderr.decode())
        pbar.remove_task(task)

def _fh(n:int, symbol:str):
    return '#' + symbol*(n -2) + '#'

def argmaxlen(lines):
    return max(lines, key=len)

def _wrap(text:str, symbol:str, n: int = 2, width: int = 50):
    return wrap(text, width=width)

def _pad(maxlen:int, text:str):
    if len(text) < maxlen:
        while len(text) != maxlen:
            if len(text) < maxlen - 1:
                text = f" {text} "
            elif len(text) < maxlen:
                text+= ' '
            elif len(text) > maxlen:
                text = text[:-1]
        return text
    else:
        return text

def _boxline(n:int, maxlen:int, text:str, symbol:str = '='):
    return _left(symbol, n) + _pad(maxlen, text) + _right(symbol, n)

def _box(lines:str, n:int = 2, symbol:str = '='):
    maxlen = max(map(len, lines))
    boxfn = lambda t: _boxline(n,maxlen, t, symbol)
    return list(map(boxfn, lines))

def _left(symbol:str, n:int):
    return '#'+n*symbol + _fw(n)
def _right(symbol:str, n:int):
    return  _fw(n) + symbol*n + '#' 

def make_header(task:str, signature: str = '', epilogue:str = '', symbol='=', n:int = 2):
    date = 'Build date: ' + dt.now().isoformat()
    author = f'Built by: {getlogin()} @ {gethostname()} on {platform}'
    task = f'Task name: {task}'
    sign = f'Author: {sign}' if signature else ''
    epi = f'Author\'s comments: \n {epilogue}' if epilogue else ''
    content = _box(list(filter(len, [date, author, task, sign, epi])), n, symbol)
    maxlen = max(map(len, content))
    h = _fh(maxlen, symbol)
    return '\n' + '\n'.join((h,*content,h)) + '\n'

def build(setup, task, important_notes:str = '', epilogue:str='', symbol:str = '=', n:int = 2):
    header = make_header(task, important_notes, epilogue, symbol, n)
    items = setup.task_items(task)
    order = setup.run_order(task)
    content = header
    with waitSpin as pbar:
        task = pbar.add_task('Creating powershell script ..', total=len(order))
        for i, rank in enumerate(order):
            content += f'#@STEP\n'
            content += make_metadata(i, rank)
            details = next(filter(lambda itm: itm.get("name") == rank, items)).get("commands")
            for scriptline in details:
                content += scriptline + '; \n'
            
            content += '#@END STEP\n\n'
            pbar.advance(task)
        
    return content

def build_save(setup, task, outpath: Path):
    outpath = Path(outpath)
    content = build(setup, task)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.with_suffix('.ps1').write_text(content)
    return outpath.with_suffix('.ps1')

def build_upload(setup, task, outpath: Path):
    script = build_save(setup=setup, task=task, outpath=outpath)
    url = uploadFromFile(script)
    oneliner_raw = outpath.parent / 'one-liner.txt'
    content = f'Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force ; irm {url.strip()} | iex'
    oneliner_pwsh = oneliner_raw.with_suffix('.ps1')

    oneliner_raw.write_text(content)
    oneliner_pwsh.write_text(content)
    compile(oneliner_pwsh)
    return content
