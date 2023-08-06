# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['astrodown',
 'astrodown.cli',
 'astrodown.templates',
 'astrodown.templates.basic.{{ cookiecutter.project_name }}.scripts',
 'astrodown.templates.full.{{ cookiecutter.project_name }}.apps.my-app',
 'astrodown.templates.full.{{ cookiecutter.project_name }}.scripts']

package_data = \
{'': ['*'],
 'astrodown.templates': ['basic/*',
                         'basic/{{ cookiecutter.project_name }}/*',
                         'basic/{{ cookiecutter.project_name }}/analysis/*',
                         'basic/{{ cookiecutter.project_name }}/data/*',
                         'basic/{{ cookiecutter.project_name }}/src/*',
                         'basic/{{ cookiecutter.project_name '
                         '}}/src/components/*',
                         'basic/{{ cookiecutter.project_name '
                         '}}/src/components/analysis/*',
                         'basic/{{ cookiecutter.project_name '
                         '}}/src/components/data/*',
                         'basic/{{ cookiecutter.project_name '
                         '}}/src/components/shared/*',
                         'basic/{{ cookiecutter.project_name }}/src/content/*',
                         'basic/{{ cookiecutter.project_name }}/src/layouts/*',
                         'basic/{{ cookiecutter.project_name }}/src/lib/*',
                         'basic/{{ cookiecutter.project_name }}/src/pages/*',
                         'basic/{{ cookiecutter.project_name '
                         '}}/src/pages/analysis/*',
                         'basic/{{ cookiecutter.project_name '
                         '}}/src/pages/data/*',
                         'basic/{{ cookiecutter.project_name '
                         '}}/src/pages/graph/*',
                         'basic/{{ cookiecutter.project_name }}/src/styles/*',
                         'full/*',
                         'full/{{ cookiecutter.project_name }}/*',
                         'full/{{ cookiecutter.project_name }}/analysis/*',
                         'full/{{ cookiecutter.project_name '
                         '}}/analysis/python/*',
                         'full/{{ cookiecutter.project_name }}/analysis/r/*',
                         'full/{{ cookiecutter.project_name }}/data/*',
                         'full/{{ cookiecutter.project_name }}/data/diamonds/*',
                         'full/{{ cookiecutter.project_name }}/data/iris/*',
                         'full/{{ cookiecutter.project_name }}/models/*',
                         'full/{{ cookiecutter.project_name }}/src/*',
                         'full/{{ cookiecutter.project_name '
                         '}}/src/components/*',
                         'full/{{ cookiecutter.project_name '
                         '}}/src/components/analysis/*',
                         'full/{{ cookiecutter.project_name '
                         '}}/src/components/data/*',
                         'full/{{ cookiecutter.project_name '
                         '}}/src/components/shared/*',
                         'full/{{ cookiecutter.project_name }}/src/content/*',
                         'full/{{ cookiecutter.project_name }}/src/layouts/*',
                         'full/{{ cookiecutter.project_name }}/src/lib/*',
                         'full/{{ cookiecutter.project_name }}/src/pages/*',
                         'full/{{ cookiecutter.project_name '
                         '}}/src/pages/analysis/*',
                         'full/{{ cookiecutter.project_name '
                         '}}/src/pages/data/*',
                         'full/{{ cookiecutter.project_name '
                         '}}/src/pages/graph/*',
                         'full/{{ cookiecutter.project_name }}/src/styles/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'cookiecutter>=2.1.1,<3.0.0',
 'pyodide-http>=0.2.0,<0.3.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['astrodown = astrodown.commands:app']}

setup_kwargs = {
    'name': 'astrodown',
    'version': '0.1.10',
    'description': 'A framework for creating shareable data science websites',
    'long_description': '# `astrodown`\n\n[bold blue]Astrodown[/bold blue] is a toolkit to build interactive websites for data science projects.\n\nSee a live example at https://astrodown-playground.qiushiyan.dev :sparkles:\n\n**Usage**:\n\n```console\n$ astrodown [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n\n    Report [bold red]bugs[/bold red] on [link=https://github.com/astrodown/astrodown-web/]Github[/link]\n    \n\n**Commands**:\n\n* `check`: Check for availabilities of programs...\n* `dev`: [bold blue]Preivew[/bold blue] the website\n* `docs`: [bold blue]Open[/bold blue] documentation...\n* `init`: [bold blue]Create[/bold blue] an astrodown...\n* `install`: [bold blue]Install[/bold blue] JavaScript...\n* `new`: [bold blue]Create[/bold blue] the folder...\n* `render`: [bold blue]Render[/bold blue] all Quarto...\n\n## `astrodown check`\n\nCheck for availabilities of programs required by astrodown\n\n**Usage**:\n\n```console\n$ astrodown check [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `astrodown dev`\n\n[bold blue]Preivew[/bold blue] the website\n\n**Usage**:\n\n```console\n$ astrodown dev [OPTIONS]\n```\n\n**Options**:\n\n* `--package-manager [npm|yarn|pnpm]`: package manager to use  [default: PackageManager.npm]\n* `--port INTEGER`: port to run the website  [default: 3000]\n* `--render-quarto / --no-render-quarto`: rerender quarto documents first  [default: no-render-quarto]\n* `--help`: Show this message and exit.\n\n## `astrodown docs`\n\n[bold blue]Open[/bold blue] documentation websites for relevant tools, e.g. Quarto, Python, etc.\n\n**Usage**:\n\n```console\n$ astrodown docs [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `astrodown init`\n\n[bold blue]Create[/bold blue] an astrodown project.\n\nMust have Quarto Node.js installed and avaiable in PATH variables, use `astrodown check` for health checks.\n\n**Usage**:\n\n```console\n$ astrodown init [OPTIONS]\n```\n\n**Options**:\n\n* `-p, --path TEXT`: path to create the project, default to the current working directory  [default: /Users/qiushi/workspace/astrodown/astrodown-python]\n* `-n, --name TEXT`: name of the project\n* `-pm, --package-manager [npm|yarn|pnpm]`: package manager to use, default to npm  [default: npm]\n* `-t, --template [basic|full]`: template to use, default to basic  [default: basic]\n* `--help`: Show this message and exit.\n\n## `astrodown install`\n\n[bold blue]Install[/bold blue] JavaScript dependencies.\n\nOnly need to be run once per project.\n\n**Usage**:\n\n```console\n$ astrodown install [OPTIONS]\n```\n\n**Options**:\n\n* `--package-manager [npm|yarn|pnpm]`: package manager to use  [default: PackageManager.npm]\n* `--help`: Show this message and exit.\n\n## `astrodown new`\n\n[bold blue]Create[/bold blue] the folder structure for a new analysis, dataset, model, api, etc.\n\n**Usage**:\n\n```console\n$ astrodown new [OPTIONS] COMPONENT_TYPE:{analysis|dataset|model|shinyapp|api}\n```\n\n**Arguments**:\n\n* `COMPONENT_TYPE:{analysis|dataset|model|shinyapp|api}`: the type of the component to be created  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `astrodown render`\n\n[bold blue]Render[/bold blue] all Quarto documents.\n\nShould be run every time a Quarto document has changed. Edit _quarto.yml to include/exclude files.\n\n**Usage**:\n\n```console\n$ astrodown render [OPTIONS]\n```\n\n**Options**:\n\n* `--package-manager [npm|yarn|pnpm]`: package manager to use  [default: PackageManager.npm]\n* `--help`: Show this message and exit.\n',
    'author': 'Qiushi Yan',
    'author_email': 'qiushi.yann@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
