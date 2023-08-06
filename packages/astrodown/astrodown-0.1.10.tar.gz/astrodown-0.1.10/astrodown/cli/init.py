import enum
import typer

from astrodown.cli.utils import prompt_error


class Template(str, enum.Enum):
    basic = "basic"
    full = "full"


def create_project(template_path: str, **cookiecutter_args: dict):
    from cookiecutter.main import cookiecutter

    try:
        result_path = cookiecutter(template_path, no_input=True, **cookiecutter_args)
    except Exception as e:
        prompt_error("creating project", e)
        raise typer.Exit()

    return result_path
