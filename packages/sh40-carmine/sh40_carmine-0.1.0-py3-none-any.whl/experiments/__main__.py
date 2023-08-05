from carmine import Carmine


def command() -> int:
    """My Carmine project."""

    return 0


def command_example(name: str, age: int = -1) -> int:
    """Prints out your name and age."""

    age_text = "I don't know your age." if age == -1 else f"You are {age}."

    print(f"Hello, {name}. {age_text}")


def main(argv: list[str] | None = None) -> None:
    """Runs the application."""

    with Carmine(argv) as cli:
        cli += command

        cli += command_example


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
