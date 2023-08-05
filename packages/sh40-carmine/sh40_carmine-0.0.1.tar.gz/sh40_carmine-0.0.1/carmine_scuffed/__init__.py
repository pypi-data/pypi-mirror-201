from __future__ import annotations

import sys
from inspect import signature, Signature
from dataclasses import dataclass
from typing import Any, NamedTuple, TypeVar, Iterable, Type, Literal, get_origin
from types import TracebackType
import re

from griffe.dataclasses import Docstring
from griffe.docstrings.parsers import Parser, parse

from zenith import markup, Palette

T = TypeVar("T")

EMPTY = Signature.empty
HELPTEXT_MAX_HANDLE_LENGTH = 35
HELPTEXT_INDENT = 2

Palette.from_hex("#D60C3F").alias()

RE_REPR = re.compile(r"[\'|\"](.*?)[\'|\"]")


def mprint(mkp: str) -> str:
    print(markup(mkp))


@dataclass
class CLIException(Exception):
    value: str

    def __str__(self) -> str:
        return self.value


@dataclass
class CLIParserError(CLIException):
    value: str


@dataclass
class CLIRuntimeError(CLIException):
    value: str


@dataclass
class Choices:
    options: tuple[T, ...]
    kind: Type[T]

    def __iter__(self) -> Iterable[T]:
        return iter(self.options)

    def __call__(self, new: Any) -> T:
        kinded = self.kind(new)

        if not kinded in self.options:
            raise CLIParserError(f"Unknown option {new!r} from {self.options!r}.")

        return kinded


def _parse_args(
    argv: list[str], schema: dict[str, tuple[Type[T], T | Signature.empty]]
) -> dict[str, Any]:
    def _expand_shorthand(char: str) -> str:
        options = [key for key in schema if key.startswith(char)]

        if len(options) == 0:
            raise CLIRuntimeError(f"Unknown shorthand {key!r}.")

        return options[0]

    def _convert_arg(arg: str, default: T, annotation: Type[T]) -> T:
        if annotation is bool:
            return not default

        return annotation(arg)

    positionals = [key for key, (_, default) in schema.items() if default is EMPTY]
    positional_index = 0

    output = {key: default for key, (_, default) in schema.items()}
    key = None

    for arg in argv:
        if arg.startswith("-"):
            if key is not None:
                annotation, default = schema[key]
                output[key] = _convert_arg(arg, default, annotation)

            arg = arg.lstrip("-")
            if len(arg) == 1:
                arg = _expand_shorthand(arg)

            key = arg.replace("-", "_")
            continue

        if key is not None:
            annotation, default = schema[key]
            output[key] = _convert_arg(arg, default, annotation)

            continue

        positional = positionals[positional_index]
        annotation = schema[positional][0]
        output[positional] = annotation(arg)

        positional_index += 1

    if key is not None:
        annotation, default = schema[key]
        output[key] = _convert_arg(arg, default, annotation)

    for key, value in output.copy().items():
        if value is EMPTY:
            del output[key]

            if not output.get("help"):
                raise CLIRuntimeError(f"Missing positional argument {key!r}.")

    return output


def _generate_help_text(
    command: Callable[..., int],
    schema: dict[str, tuple[Type[T], T | Signature.empty]],
    available_commands: list[Callable[..., int]] | None = None,
) -> str:

    if not hasattr(command, "__doc__"):
        raise CLIParserError(f"Command {command.__name__!r} doesn't have a docstring.")

    docstring = Docstring(command.__doc__, lineno=1)
    parsed = parse(docstring, parser=Parser.google)

    description = parsed[0]
    params = parsed[1].as_dict()["value"] if len(parsed) > 1 else []

    title, *body = description.value.splitlines()

    param_to_doc: dict[str, str] = {"help": "Prints this message and exits."}

    for param in params:
        param_to_doc[param.name] = " ".join(param.description.split("\n"))
        default = schema[param.name][1]

        if default is not EMPTY:
            param_to_doc[param.name] += f" Defaults to {default!r}."

    indent = HELPTEXT_INDENT * " "

    options = ""
    used_shorthands = []

    handle_length = max(len(item) for item in schema) + 10
    positionals = []

    for key, (kind, default) in schema.items():
        if default is EMPTY:
            positionals.append(key)
            continue

        handle = f"--{key.replace('_', '-')}"

        if not key[0] in used_shorthands:
            handle = f"-{key[0]}, " + handle
            used_shorthands.append(key[0])

        if isinstance(kind, Choices):
            handle += f" [{'|'.join(kind)}]"

        padding = handle_length - len(indent + handle)
        line = f"{indent}{handle + padding * ' '}"

        if len(line) > handle_length:
            line += f"\n{(handle_length) * ' '}"

        options += line + param_to_doc[key] + "\n"

    helptext = f"""\

{indent}{title}

Options:
{options}"""

    if available_commands is not None:
        usage = f"usage: {sys.argv[0].split('/')[-1]} [OPTIONS] COMMAND [ARGS]..."

        helptext += "\nCommands:\n"
        command_length = max(len(item[0]) for item in available_commands) + 5

        for name, doc in available_commands:
            if name == "":
                continue

            helptext += f"{indent}{name:<{command_length}}{doc.splitlines()[0]}\n"

    else:
        usage = (
            f"usage: {sys.argv[0].split('/')[-1]}"
            + f" {command.__name__.removeprefix('command_')} [OPTIONS] "
            + " ".join([key.upper() for key in positionals])
        )

    return usage + "\n" + helptext


class Carmine:
    def __init__(self, argv: list[str] | None = None) -> None:
        self._argv = argv or sys.argv[1:]
        self._commands: dict[str, tuple[Callable[..., int], str]] = {}

    def __enter__(self) -> Carmine:
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc: BaseException | None,
        traceback: Traceback | None,
    ) -> None:
        self.run()

    def __iadd__(self, command: object) -> Carmine:
        if not callable(command):
            raise TypeError(
                "Can only register commands to the CLI, not {type(command)!r}."
            )

        self.register(command)
        return self

    def register(self, command: Callable[..., bool]) -> None:
        """Registers a new comand."""

        sig = signature(command)

        arguments: dict[str, tuple[Type[T], T | EMPTY]] = {}

        for name, param in sig.parameters.items():
            if param.default is Signature.empty:
                arguments[name] = (param.annotation, EMPTY)
                continue

            annotation = param.annotation

            if get_origin(annotation) == Literal:
                options = annotation.__args__
                # TODO:                       Why????
                annotation = Choices(options, type(options[0]))

            arguments[name] = (annotation, param.default)

        arguments["help"] = bool, False

        name = command.__name__.removeprefix("command").lstrip("_").replace("_", "-")

        def _execute(argv: list[str]) -> None:
            if argv == []:
                argv = ["--help"]

            kwargs = _parse_args(argv, schema=arguments)

            if kwargs == {"help": True}:
                command()

            if kwargs["help"]:
                print(
                    _generate_help_text(
                        command,
                        arguments,
                        [(name, doc) for name, (_, doc) in self._commands.items()]
                        if name == ""
                        else None,
                    )
                )
                return

            del kwargs["help"]

            command(**kwargs)

        self._commands[name] = _execute, command.__doc__

    def run(self) -> None:
        def _run_wrapped(argv: list[str], command: Callable[..., int] | None = None):
            try:
                if command is None:
                    command = self._argv[0]

                if command not in self._commands:
                    raise CLIRuntimeError(f"Unknown command {command!r}.")

                self._commands[command][0](argv)

            except CLIException as exc:
                value = RE_REPR.sub(r"[success]'\1'[/fg]", exc.value)
                mprint(f"[bold error]Error:[/] {value}")

        if len(self._argv) == 0 or self._argv[0].startswith("-"):
            _run_wrapped(self._argv[0:], "")
            return

        _run_wrapped(self._argv[1:])
