from pathlib import Path
from jinja2.loaders import FileSystemLoader
from jinja2.environment import Environment
from lowcode_code.settings import settings


def create_template_file_loader(tpl_file: Path):
    loader = FileSystemLoader(tpl_file.parent)
    return loader


def create_template_env(tpl_file: Path):
    loader = create_template_file_loader(tpl_file)
    env = Environment(loader=loader)

    env.variable_start_string = settings.get('jinja2.variable_start_string', '{{')
    env.variable_end_string = settings.get('jinja2.variable_end_string', '}}')

    return env
