from pathlib import Path
import click
from lowcode_code.settings import settings
from lowcode_code.commands import render
from lowcode_code.render import FileRender


@click.group(help="Low code command line tool.")
def cli():
    ...


@click.command(help="Render template files using json files.")
@click.option(
    "--schema-file", "-sf", help="json file, it will be used as jinja2 variables."
)
@click.option("--tpl-file", "-tf", help="template file, supports jinja syntax.")
@click.option(
    "--save-file", required=False, help="output result code to file or terminal."
)
def render_file(tpl_file: str, schema_file: str, save_file: str = None):
    tpl_file = Path(tpl_file)
    if not tpl_file.is_absolute():
        tpl_file = tpl_file.absolute()

    schema_file = Path(schema_file)
    if not schema_file.is_absolute():
        schema_file = schema_file.absolute()

    if save_file:
        save_file = Path(save_file)
        if not save_file.is_absolute():
            save_file = save_file.absolute()

    content = render.render_file(tpl_file, schema_file)
    if save_file:
        save_file.write_text(content)
    else:
        print(content)


@click.command(
    help="Iterate a directory, and render each pair of template and json files in the directory into code."
)
@click.option(
    "--dir",
    "-d",
    required=True,
    type=str,
    help="Directory that contains templates and json files.",
)
@click.option("--output", "-o", required=False, type=str, help="Output directory.")
def render_dir(dir: str, output: str):
    dir = Path(dir)

    if not dir.exists():
        click.echo("template dir is not exists.")
        return
    render.render_dir(dir, output)


@click.command(help="Show global jinja filters.")
def show_filter():
    renderer = FileRenderer()
    filters = (item for item in FileRenderer().filters)
    result = ', '.join(filters)
    print(result)

@click.command(help="Show global jinja handlerss.")
def show_handle():
    renderer = FileRenderer()
    handles = (item for item in FileRenderer().handlers)
    result = ', '.join(handles)
    print(result)


cli.add_command(render_file)
cli.add_command(render_dir)
cli.add_command(show_filter)
cli.add_command(show_handle)

if __name__ == "__main__":
    cli()
