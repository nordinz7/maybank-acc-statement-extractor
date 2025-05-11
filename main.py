import click
from util import process_output, read_from_file_or_folder
from itertools import chain


@click.command()
@click.option(
    "--path",
    required=True,
    help="Path to file or folder containing PDF statements",
)
@click.option(
    "--pwd",
    required=True,
    help="Password for PDF statement assuming same for every file",
)
@click.option(
    "--format",
    type=click.Choice(["csv", "json"], case_sensitive=False),
    default="csv",
    show_default=True,
    help="Output file format either csv or json",
)
@click.option(
    "--print-summary",
    is_flag=True,
    default=False,
    show_default=True,
    help="Print summary of the account statement",
)
@click.option(
    "--merge",
    is_flag=True,
    default=True,
    show_default=True,
    help="Output only single merged file",
)
@click.option(
    "--output",
    type=click.Path(),
    help="Output file path. If not provided, output will be printed to terminal",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose mode for detailed output",
)
def main(*args, **kwargs):
    path = kwargs["path"]
    pwd = kwargs["pwd"]

    data = read_from_file_or_folder(path, pwd)
    if kwargs["merge"]:
        # Ensure data is a list of lists before flattening
        if data and not isinstance(data[0], (list, tuple)):
            data = [data]
        data = list(chain.from_iterable(data))
    process_output(data, kwargs)


if __name__ == "__main__":
    main()
