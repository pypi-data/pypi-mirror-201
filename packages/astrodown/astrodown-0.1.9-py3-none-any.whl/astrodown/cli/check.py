import shutil
from typing import Tuple
from rich.console import Console
from rich.table import Table

from astrodown.cli.utils import (
    colored_text,
    config_exists,
    get_package_manager,
)

required_programs = {
    "node": "https://nodejs.org",
    "quarto": "https://quarto.org/docs/get-started/",
}

package_managers = {
    "npm": "https://docs.npmjs.com/downloading-and-installing-node-js-and-npm",
    "yarn": "https://yarnpkg.com/getting-started/install",
    "pnpm": "https://pnpm.io/installation",
}

console = Console()


def command_path(command: str) -> Tuple[str | None, bool]:
    path = shutil.which(command)
    return path


def print_health_table(
    program_availabilities: dict[str, bool] | None = None
) -> list[str]:
    """
    Pirnts a table of the path of the required programs and their installation link

    returns a list of missing programs
    """
    table = Table(show_lines=True)
    table.add_column("Program", style="magenta")
    table.add_column("Status")
    table.add_column("Installation")

    if program_availabilities is None:
        all_programs = [*required_programs]
        if config_exists():
            package_manager = get_package_manager()
            if package_manager is not None:
                all_programs.append(package_manager)

        program_availabilities = {
            program: command_path(program) for program in all_programs
        }

    missing_programs = []
    for program, path in program_availabilities.items():
        path = command_path(program)
        availability = (
            colored_text(path, "green") if path else colored_text("Not Found", "red")
        )
        if not path:
            missing_programs.append(program)
        installation = (
            required_programs[program]
            if program in required_programs
            else package_managers[program]
        )
        table.add_row(
            program,
            availability,
            installation,
        )

    console.print(table)

    return missing_programs
