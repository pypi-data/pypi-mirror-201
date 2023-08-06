from astrodown.cli.init import Template
import os


def get_template_path(template: Template):
    import importlib.resources

    return os.path.join((importlib.resources.files(__package__)), template.value)
