import enum
from pathlib import Path

import typer
from astrodown.cli.utils import get_astrodown_config, prompt_error, prompt_success


class ComponentType(str, enum.Enum):
    analysis = "analysis"
    data = "data"
    model = "model"
    shiny = "shiny"


def new_component(component_type: ComponentType, name: str):
    config = get_astrodown_config()
    dir = Path(config[component_type.value + "_dir"])
    if not dir.is_dir():
        dir.mkdir()

    if component_type == ComponentType.shiny:
        path = dir / f"{name}.py"
        if path.exists():
            prompt_error(f"{path} already exists")
            return typer.Exit(1)
        path.write_text(
            """from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.input_slider("n", "N", 0, 100, 20),
    ui.output_text_verbatim("txt"),
)

def server(input, output, session):
    @output
    @render.text
    def txt():
        return f"n*2 is {input.n() * 2}"


app = App(app_ui, server)"""
        )

    else:
        path = dir / f"{name}.qmd"
        if path.exists():
            prompt_error(f"{path} already exists")
            return typer.Exit(1)
        path.write_text(
            f"""---
title: {name}
---"""
        )

    prompt_success(f"created new {component_type.value} at {path}")
