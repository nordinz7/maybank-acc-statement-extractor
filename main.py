import click
from util import (
    get_filtered_data,
    get_mapped_data,
    kebab_to_snake,
    process_output,
    read_pdfs,
)


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
    arr = read_pdfs(kwargs["path"], kwargs["pwd"])

    processed = []

    for ar in arr:
        filtered_data = get_filtered_data(ar)

        mapped_data = get_mapped_data(filtered_data)

        if kwargs["merge"]:
            processed.extend(mapped_data)
            continue

        process_output(mapped_data, kwargs)

    if processed:
        process_output(processed, kwargs)


if __name__ == "__main__":
    main()
