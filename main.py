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
    help="path to file or folder containing PDF statements",
)
@click.option(
    "--pwd",
    help="password for PDF statement assuming same for every file",
)
@click.option(
    "--format",
    default="csv",
    help="output file format either csv or json",
)
@click.option(
    "--print-summary",
    default=False,
    help="print summary of the account statement",
)
@click.option(
    "--merge",
    default=True,
    help="output only single merged file.",
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
