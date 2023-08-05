from __future__ import annotations

import logging
import sys
import re
from dataclasses import dataclass, field
from inspect import Signature, signature, cleandoc
from typing import Any, NamedTuple, TypeVar, Callable, Protocol

from griffe.dataclasses import Docstring
from griffe.docstrings.parsers import Parser, parse
from zenith import markup, Palette

Empty = object()

T = TypeVar("T")

RE_REPR = re.compile(r"[\'|\"](.*?)[\'|\"]")

INDENT = 2 * " "

HELP = """\
{usage}

{doc}

{options}
{commands}"""

logging.getLogger("griffe").setLevel(logging.ERROR)

Palette.from_hex("#D70040").alias()


@dataclass
class CLIException(Exception):
    """An exception raised during the preparation or execution of a CLI."""

    def __init__(self, value: str, code: int = 1) -> None:
        self.value = value
        self.code = code


class CLIParserError(CLIException):
    """An exception raised during the preparation of a CLI."""


class CLIRuntimeError(CLIException):
    """An exception raised during the execution of a CLI."""


class CLIArgumentError(CLIException):
    """An exception raised when invalid arguments are passed to the CLI."""


class Parameter(NamedTuple):
    """Represents an Python signature parameter."""

    factory: Callable[[Any], T]
    default: T | Empty


class Command(NamedTuple):
    """Represents a command that can execute using CLI arguments."""

    doc: str
    executor: Callable[list[str], None]

    def __call__(self, argv: list[str]) -> None:
        self.executor(argv)


class Choice:
    """Represents a multiple-choice argument type."""

    def __init__(self, *choices: T) -> None:
        self.choices = choices

    def __call__(self, item: object) -> T:
        if not item in self.choices:
            raise CLIArgumentError(f"Choice {item!r} is not in {self.choices!r}.")

        return item


def _boolean_flag(item: bool) -> bool:
    """Returns the opposite of the given item."""

    return not item


def _get_schema(
    command: Callable[..., None], include_help: bool = True
) -> dict[str, Parameter]:
    """Generates a schema from the given command's signature."""

    schema: dict[str, Parameter] = {}

    for name, param in signature(command).parameters.items():
        annotation = param.annotation

        if annotation is bool:
            annotation = _boolean_flag

        default = Empty if param.default is Signature.empty else param.default
        schema[name] = Parameter(factory=annotation, default=default)

    schema["help"] = Parameter(factory=_boolean_flag, default=False)
    return schema


def _parse_arguments(argv: list[str], schema: dict[str, Parameter]) -> dict[str, Any]:
    """Parses the given arguments."""

    def _handle_key_using_default(key: str) -> None:
        param = schema[key]
        arguments[key] = param.factory(param.default)

    arguments: dict[str, Any] = {key: param.default for key, param in schema.items()}
    positionals: list[str] = [
        key for key, param in schema.items() if param.default is Empty
    ]

    def _expand(arg: str) -> str:
        for key in schema:
            if key in positionals:
                continue

            if key.startswith(arg):
                return key

        raise CLIRuntimeError(f"Unknown shorthand {arg!r}.")

    key = None
    pos_index = 0

    for arg in argv:
        if arg.startswith("-"):
            arg = arg.lstrip("-")

            if len(arg) == 1:
                arg = _expand(arg)

            key = arg.replace("-", "_")

            if schema[key].factory is _boolean_flag:
                _handle_key_using_default(key)
                key = None

            continue

        if key is not None:
            param = schema[key]
            arguments[key] = param.factory(arg)

            key = None
            continue

        if pos_index >= len(positionals):
            raise CLIArgumentError(f"Got unexpected positional argument {arg!r}.")

        positional = positionals[pos_index]
        pos_index += 1

        param = schema[positional]
        arguments[positional] = param.factory(arg)

    if not arguments["help"]:
        for key, value in arguments.items():
            if value is Empty:
                raise CLIArgumentError(f"Missing positional argument {key!r}.")

    return arguments


class HelpPrinter(Protocol):
    def __call__(
        self,
        exec_line: str,
        documentation: list[str],
        options: list[tuple[str, str | None, type, str]],
        positionals: list[str],
        commands: dict[str, str],
    ) -> None:
        """Prints helper text from the given arguments.

        Args:
            exec_line: The CLI command used to run the file, without any arguments. For
                example, `my-program cmd arg1 arg2` would give `my-program cmd`.
            documenation: This command's documentation, cleaned using `inspect.cleandoc`
                and split into lines.
            options: A list of (key, shorthand, documentation) tuples for the options
                that are taken by this command.
            positionals: A list of all positional arguments this command takes.
            commands: The commands available within this command. This is set to {} in
                all but the main (named "command") command.
        """


def print_help(
    exec_line: str,
    documentation: list[str],
    options: list[tuple[str, str | None, type, str]],
    positionals: list[str],
    commands: dict[str, str],
) -> None:
    """Builds and prints the help text activated on --help."""

    def _find_max_len(seq: Iterable[str]) -> int:
        items = list(seq)

        if len(items) == 0:
            return 0

        return max(len(item) for item in items)

    usage_text = f"Usage: {exec_line}"

    if len(options) > 0:
        for opt, _, annotation, _ in options:
            if opt == "help":
                continue

            usage_text += f" [--{opt}"

            if annotation is not _boolean_flag:
                usage_text += " " + opt.upper().replace("-", "_")

            usage_text += "]"

    if len(commands) > 0:
        usage_text += " <command>"

    if len(positionals) > 0:
        usage_text += " " + " ".join("{" + key + "}" for key in positionals)

    options_text = "Options:\n"
    option_len = 2 * _find_max_len([key for key, *_ in options])

    for (key, shorthand, _, doc) in options:
        line = f"--{key}"

        if shorthand is not None:
            line = f"-{shorthand}, " + line

        options_text += f"{INDENT + line:<{option_len}}  {doc}\n"

    commands_text = ""
    if commands:
        commands_text += "Commands:\n"

        command_len = _find_max_len(commands) + 2
        for name, doc in commands.items():
            commands_text += f"{INDENT + name:<{command_len}}  {doc}\n"

    doc_text = INDENT + f"\n{INDENT}".join(documentation)

    output = f"{usage_text}\n\n{doc_text}\n"

    if options_text:
        output += "\n" + options_text
    if commands_text:
        output += "\n" + commands_text

    print(output.rstrip("\n"))


@dataclass
class Carmine:
    argv: list[str] | None = None
    name: str = field(init=False)
    help_printer: HelpPrinter = print_help

    _commands: dict[str, Command] = field(init=None, default_factory=dict)

    def __post_init__(self) -> None:
        if self.argv is None:
            self.argv = sys.argv

        self.name = self.argv[0].split("/")[-1]
        self.argv.pop(0)

    def __iadd__(self, obj: object) -> Carmine:
        if not callable(obj):
            raise TypeError(
                f"Can only register commands to the CLI, not {type(obj)!r}."
            )

        self.register(obj)
        return self

    def __enter__(self) -> Carmine:
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc: BaseException | None,
        traceback: Traceback | None,
    ) -> None:
        if isinstance(exc, CLIParserError):
            self.error_and_exit(exc.value, exc.code)

        try:
            self.run()

        except CLIArgumentError as exc:
            self._commands[self._command](["--help"])
            print()
            self.error_and_exit(exc.value, exc.code)

        except CLIRuntimeError as exc:
            self.error_and_exit(exc.value, exc.code)

    def register(self, command: Callable[..., None]) -> None:
        """Registers a new command."""

        schema = _get_schema(command)
        name = command.__name__.removeprefix("command_").replace("_", "-")

        docstring = Docstring(command.__doc__, lineno=1)
        parsed = parse(docstring, parser=Parser.google)

        description = parsed[0].value
        params = parsed[1].value if len(parsed) > 1 else []

        param_doc = {}
        for param in params:
            param_doc[param.name] = " ".join(param.description.splitlines())

            default = schema[param.name][1]

            if default is not Empty:
                param_doc[param.name] += f" Defaults to {default!r}."

        param_doc["help"] = "Prints this message and exits."

        positionals = [key for key, param in schema.items() if param.default is Empty]

        options = []
        used_shorthands = []

        for key, param in schema.items():
            if key in positionals:
                continue

            shorthand = key[0]
            if shorthand in used_shorthands:
                shorthand = None

            if shorthand is not None:
                used_shorthands.append(shorthand)

            options.append(
                (
                    key.replace("_", "-"),
                    shorthand,
                    param.factory,
                    param_doc.get(key, ""),
                )
            )

        def _execute(argv: list[str]) -> None:
            commands = {}

            if name == "command":
                if argv == []:
                    argv = ["--help"]

                commands = {
                    cmd_name: cmd.doc
                    for cmd_name, cmd in self._commands.items()
                    if cmd_name != "command"
                }

            args = _parse_arguments(argv, schema=schema)

            if args["help"]:
                self.help_printer(
                    exec_line=f"{self.name}{' ' + name if name != 'command' else ''}",
                    documentation=cleandoc(description).splitlines(),
                    options=options,
                    positionals=positionals,
                    commands=commands,
                )

                return

            del args["help"]
            command(**args)

        self._commands[name] = Command(description, _execute)

    def error_and_exit(self, content: str, code: int) -> None:
        """Prints out `content` and exits with given the status code."""

        content = RE_REPR.sub(r"[success]'\1'[/fg]", content)
        print(markup(f"[error bold]Error:[/] {content}"))

        sys.exit(code)

    def run(self) -> None:
        """Runs the CLI."""

        command = "command" if self.argv in ([], ["-h"], ["--help"]) else self.argv[0]

        if command not in self._commands:
            raise CLIRuntimeError(f"Unknown command {command!r}.")

        self._command = command
        self._commands[command](self.argv[1:])
