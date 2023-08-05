from pathlib import Path
from typing import Literal

from carmine import Carmine, Choice


def command() -> None:
    """The first test."""


def command_test(
    path: Path,
    loglevel: Choice("one", "two", "three") = "one",
    lcustom: int = 0,
    ignore_empty: bool = False,
) -> int:
    """Tests something.

    This is some body text.

        and this is indented!

    Args:
        path: The path to test.
        loglevel: How deeply we should log.
        lcustom: CUM
        ignore_empty: If set, we will update cum.
    """

    print(f"{path=}, {ignore_empty=}, {loglevel=}")


def main() -> None:
    with Carmine() as cli:
        cli += command

        cli += command_test


if __name__ == "__main__":
    main()
