import subprocess
from astrodown.constants import default_config
from rich import print
import typer
import yaml
from astrodown.cli.install import PackageManager
import os


def run_shell(cmd: str, verbose: bool = True, **kwargs):
    if verbose:
        prompt_success(
            " running command: ", "`", colored_text(cmd, color="blue"), "`", sep=""
        )
    try:
        _completed_process = subprocess.run(cmd, shell=True, check=True, **kwargs)
    except Exception as e:
        prompt_error(f"command `{cmd}` failed with reason: {e}")
        raise typer.Exit(1)


def colored_text(text: str, color: str = "green", bold: bool = True):
    begin_tag = f"[bold {color}]" if bold else f"[{color}]"
    end_tag = f"[/bold {color}]" if bold else f"[/{color}]"
    return f"{begin_tag}{text}{end_tag}"


def prompt_error(*text: any, bold: bool = True):
    print(colored_text("\[astrodown]:", color="red", bold=bold), *text)


def prompt_success(*text: any, bold: bool = True, **print_args):
    print(colored_text("\[astrodown]:", color="green", bold=bold), *text, **print_args)


def config_exists(config_file: str = "_astrodown.yml") -> bool:
    return os.path.exists(config_file)


def get_astrodown_config(config_file: str = "_astrodown.yml", verbose: bool = True):
    config_file = os.path.join(os.getcwd(), config_file)
    if not config_exists(config_file):
        if verbose:
            prompt_error(f"config file {config_file} not found, using defaults instead")
        return default_config

    with open(config_file, "r") as f:
        try:
            config = yaml.safe_load(f)
            for key in default_config.keys():
                if key not in config:
                    config[key] = default_config[key]
            return config
        except Exception as e:
            if verbose:
                prompt_error(
                    f"""config file {config_file} is not valid: {e}
                    using defaults instead"""
                )
            return default_config


def get_package_manager(
    config_file: str = "_astrodown.yml", verbose: bool = True
) -> PackageManager:
    config = get_astrodown_config(config_file, verbose=verbose)
    if config is not None:
        return config["node"]["package_manager"]
    else:
        if verbose:
            prompt_success(
                "using default package manager",
            )
        return PackageManager.npm
