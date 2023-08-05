from pathlib import Path

from . import Carmine, CLIRuntimeError

TEMPLATE = """\
from carmine import Carmine


def command() -> None:
    \"\"\"My Carmine project.\"\"\"


def command_example(name: str, age: int = -1) -> None:
    \"\"\"Prints out your name and age.

    Args:
        name: Your name.
        age: Your age.
    \"\"\"

    age_text = "I don't know your age." if age == -1 else f"You are {age}."

    print(f"Hello, {name}. {age_text}")


def main(argv: list[str] | None = None) -> None:
    \"\"\"Runs the application.\"\"\"

    with Carmine(argv) as cli:
        cli += command

        cli += command_example


if __name__ == "__main__":
    import sys

    main(sys.argv)
"""


def command() -> int:
    """The Carmine utility."""

    return 0


def command_create(
    filepath: Path,
    force: bool = False,
) -> int:
    """Generates a new CLI-runner file to use as a template.

    Args:
        filepath: The path of the generated file.
        force: If set, an already existing file at `<directory>/<filename>` will be
            overwritten.
    """

    if filepath.exists() and not force:
        raise CLIRuntimeError(
            f"File {str(filepath)!r} already exists."
            + " Overwrite this restriction with '--force'."
        )

    with open(filepath, "w") as file:
        file.write(TEMPLATE)

    return 0


def main(argv: list[str] | None = None) -> None:
    """Runs the application."""

    with Carmine(argv) as cli:
        cli += command

        cli += command_create


if __name__ == "__main__":
    import sys

    main(sys.argv)
