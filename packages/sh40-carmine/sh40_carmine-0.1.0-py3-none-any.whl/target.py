from carmine import Carmine


def command_generate(
    directory: Path,
    filename: str = "__main__.py",
    force: bool = False,
) -> int:
    """Generates a new CLI-runner file to use as a template.

    Args:
        directory: Where the file should be stored.
        filename: The name of the file.
        force: If set, an already existing file at `<directory>/<filename>` will be
            overwritten.
    """

    if not directory.exists():
        cli.error(f"Path {str(directory)!r} does not exist.")
        return 1

    if not directory.is_dir():
        cli.error(f"Path {str(directory)!r} is not a directory.")
        return 2

    filepath = directory / filename

    if filepath.exists() and not force:
        cli.error(
            f"File {str(filepath)!r} already exists."
            + " Overwrite this restriction with --force."
        )
        return 3

    with open(filepath, "w") as file:
        file.write("This is a cool file.")

    return 0


def main(argv: list[str] | None = None) -> None:
    """Runs the application.

    Args:
        argv: A list of command line arguments.
    """

    with Carmine(argv) as cli:
        cli += command_generate


if __name__ == "__main__":
    main()
