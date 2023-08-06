# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yaml_scripts']

package_data = \
{'': ['*']}

install_requires = \
['ix-cli>=0.1.2,<0.2.0', 'yaml-setup>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['yamlrun = yaml_scripts.cli:app',
                     'ymlr = yaml_scripts.cli:app']}

setup_kwargs = {
    'name': 'yaml-scripts',
    'version': '0.1.1',
    'description': 'Creating windows auto install scripts from YAML config files',
    'long_description': "# Creating auto install scripts from YAML config files\n\n## Features\n\n- [Pydantic-like Schema validation](#schema-valid): the YAML schema has precise syntax and the build pipeline will yield warnings or stop if your file has errors in it\n- A **set of CLIs** to interact with config files:\n    - `yamlrun` shows the commands\n    - `yamlrun script` is the script building subcommand\n    - `yamlrun upload` is the script temp hosting subcommand\n    - `yamlrun pack` locates a `setup.yml` file within the current directory and runs all the commands.\n\n\n## An explanation\n\nRunning the command\n\n```powershell\nyamlrun ?\n```\n\nOr equivalently `yamlrun explain` will output this explanation in the terminal:\n\n---\n### The setup file\n---\n\nThe YAML setup file (which can also be JSON), is a way for you to describle exactly what type of package/program you\nwant to auto-install using a single installer.\n\n---\n### File structure \n---\nThe file is structured in the following way:\n```yaml\n<task name 1>:\n    description: <textual description if you wish, OPTIONAL>\n    items:\n        <item name 1>:\n            description: <textual description if you wish, OPTIONAL>\n            type: <type description, if it's a CLI, GUI, what purpose, REQUIRED>\n            priority: <how important it is to install it within the setup REQUIRED>\n            commands:\n                - <powershell line 1>\n                - <powershell line 2>\n        <item name 2>:\n            ...\n        <item name 3>:\n            ...\n    run:\n        # order in which the items are going to be installed\n        steps:\n            - <item name 1>\n            - <item name 3> # look you just swapped the order !\n            - <item name 2>\n<task name 2>:\n    ...\n<task name 3>:\n    ...\n```\n\n---\n### Script & Executable Builder \n---\n\nTwo options:\n\n(1) One-liner script install. This script is equivalent to:\n\n    - Building the PS1 core script `yamlrun script build <task> <path/to/setup.yml>`\n    - Uploading the PS1 core script `yamlrun upload f <path/to/setup.ps1>`\n    - The previous step should give you an URL of the kind http://ix.io/<letters or numbers>\n    - Your resulting one liner is just:\n    `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force ; irm <url> | iex`\n\nthis is the `yamlrun script BOL` or `yamlrun script build-one-liner` command.\n\n(2) Doing any of the steps above on its own.\n\n# Sample setup file\n\nYou can peek at the contents of this [setup.yml file](setup.yml).\n\nThe resulting script from calling `yamlrun script build` is [the setup.ps1 file](setup.ps1).\n\nFinally, calling `yamlrun setup render <name>` will generate a [markdown formatted version of your setup file like setup.md](setup.md)\n\n# Installation\n\nJust `pip install` it if you have it, but an executable is underway 😎\n\n```powershell\npip install yaml-scripts\n```\n",
    'author': 'arnos-stuff',
    'author_email': 'bcda0276@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/arnos-stuff/yaml-scripts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
