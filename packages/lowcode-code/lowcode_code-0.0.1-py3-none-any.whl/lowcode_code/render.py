from pathlib import Path
import json
import jsonschema
from lowcode_code.schema import DefaultValidatingDraft7Validator
import os
from lowcode_code.jinja import create_template_env
from typing import Iterable, Callable
from lowcode_code.settings import settings
from jinja2.environment import Environment
import logging
import uuid
from case_convert import camel_case, snake_case, pascal_case

loggeer = logging.getLogger()


class FileRender:
    default_filters = (camel_case, snake_case, pascal_case)

    default_handlers = ()

    schema_suffix = settings.get("SCHEMA_SUFFIX", ".json")

    template_suffix = settings.get("TEMPLATE_SUFFIX", ".tpl")

    filter_scope = settings.get("FILTER_SCOPE", "__scope__")

    handler_scope = settings.get("FILTER_SCOPE", "__scope__")

    def __init__(
        self,
        filters: Iterable[Callable] = None,
        handlers: Iterable[Callable] = None,
    ):
        self._filters = filters or []
        self._handlers = handlers or []
        self._filters.extend(self.default_filters)
        self._handlers.extend(self.default_handlers)

    @property
    def filters(self):
        filters = {}
        for _filter in self._filters:
            filters[f"{self.filter_scope}.{_filter.__name__}"] = _filter
        return filters

    @property
    def handlers(self):
        handlers = {}
        for _handler in self._handlers:
            handlers[f"{self.handler_scope}.{_handler.__name__}"] = _handler
        return handlers

    def register_env_filters(self, env: Environment):
        env.filters.update(self.filters)
        return env

    def register_env_handlers(self, env: Environment):
        env.globals.update(self.handlers)
        return env

    def render(self, tpl_file: Path, schema_file: Path):
        env = create_template_env(tpl_file)

        self.register_env_filters(env)
        self.register_env_handlers(env)

        tpl = env.get_template(tpl_file.name)

        schema = json.loads(schema_file.read_text())
        resolver = jsonschema.RefResolver(f"file://{schema_file.parent}", schema)

        DefaultValidatingDraft7Validator(schema, resolver)

        content = tpl.render(schema=schema)
        return content


class DirRender:
    def __init__(
        self,
        tpl_dir: Path,
        output: Path = None,
        filters: Iterable[Callable] = None,
        handlers: Iterable[Callable] = None,
    ):
        self.tpl_dir = tpl_dir
        self.output = output if output else Path.cwd() / ".lowcode" / str(uuid.uuid4())
        if filters is None:
            self.filters = []
        if handlers is None:
            self.handlers = []

        if not self.output.exists():
            self.output.mkdir(parents=True)

        if not self.output.is_absolute():
            self.output = self.output.absolute()

        self.file_renderer = FileRender(filters=self.filters, handlers=self.handlers)

    def render(self):
        for root, _dirs, files in os.walk(self.tpl_dir):
            root = Path(root)
            for file_ in files:
                tpl_file = root / file_
                if not tpl_file.suffix == self.file_renderer.template_suffix:
                    continue
                file_ = file_.split(".")[0]
                schema_file = root / f"{file_}.json"
                if schema_file.is_symlink():
                    schema_file = schema_file.readlink()
                elif not schema_file.exists():
                    continue
                schema = json.loads(schema_file.read_text())
                suffix = schema.get("_meta", {}).get("suffix", "")
                content = self.file_renderer.render(
                    tpl_file=tpl_file, schema_file=schema_file
                )
                relpath = tpl_file.relative_to(self.tpl_dir)
                file_output = self.output / str(relpath).replace(
                    tpl_file.suffix, suffix
                )
                if not file_output.parent.exists():
                    file_output.parent.mkdir()
                file_output.write_text(content)
                logging.info(f"render file {relpath} SUCCESS.")
