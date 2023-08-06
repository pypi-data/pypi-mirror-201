# Creating auto install scripts from YAML config files

## Features

- [Pydantic-like Schema validation](#schema-valid): the YAML schema has precise syntax and the build pipeline will yield warnings or stop if your file has errors in it
- A **set of CLIs** to interact with config files:
    - `yamlrun` shows the commands
    - `yamlrun script` is the script building subcommand
    - `yamlrun upload` is the script temp hosting subcommand
    - `yamlrun pack` locates a `setup.yml` file within the current directory and runs all the commands.


## An explanation

Running the command

```powershell
yamlrun ?
```

Or equivalently `yamlrun explain` will output this explanation in the terminal:

---
### The setup file
---

The YAML setup file (which can also be JSON), is a way for you to describle exactly what type of package/program you
want to auto-install using a single installer.

---
### File structure 
---
The file is structured in the following way:
```yaml
<task name 1>:
    description: <textual description if you wish, OPTIONAL>
    items:
        <item name 1>:
            description: <textual description if you wish, OPTIONAL>
            type: <type description, if it's a CLI, GUI, what purpose, REQUIRED>
            priority: <how important it is to install it within the setup REQUIRED>
            commands:
                - <powershell line 1>
                - <powershell line 2>
        <item name 2>:
            ...
        <item name 3>:
            ...
    run:
        # order in which the items are going to be installed
        steps:
            - <item name 1>
            - <item name 3> # look you just swapped the order !
            - <item name 2>
<task name 2>:
    ...
<task name 3>:
    ...
```

---
### Script & Executable Builder 
---

Two options:

(1) One-liner script install. This script is equivalent to:

    - Building the PS1 core script `yamlrun script build <task> <path/to/setup.yml>`
    - Uploading the PS1 core script `yamlrun upload f <path/to/setup.ps1>`
    - The previous step should give you an URL of the kind http://ix.io/<letters or numbers>
    - Your resulting one liner is just:
    `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force ; irm <url> | iex`

this is the `yamlrun script BOL` or `yamlrun script build-one-liner` command.

(2) Doing any of the steps above on its own.

# Sample setup file

You can peek at the contents of this [setup.yml file](setup.yml).

The resulting script from calling `yamlrun script build` is [the setup.ps1 file](setup.ps1).

Finally, calling `yamlrun setup render <name>` will generate a [markdown formatted version of your setup file like setup.md](setup.md)

# Installation

Just `pip install` it if you have it, but an executable is underway 😎

```powershell
pip install yaml-scripts
```
