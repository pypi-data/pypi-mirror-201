from pathlib import Path
from typing import Union
from lowcode_code.render import FileRender, DirRender


def render_file(tpl_file: Union[str, Path], schema_file: Path):
    if isinstance(tpl_file, str):
        tpl_file = Path(tpl_file)
    fr = FileRender()
    return fr.render(tpl_file, schema_file)


def render_dir(tpl_dir: Union[str, Path], output=None):
    if isinstance(tpl_dir, str):
        tpl_dir = Path(tpl_dir)
    if isinstance(output, str):
        output = Path(output)
    dr = DirRender(tpl_dir, output)
    return dr.render()
