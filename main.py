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
    default=False,
    help="output only single merged file.",
)
def main(*args, **kwargs):
    def getv(k):
        return kwargs[kebab_to_snake(k)]

    arr = read_pdfs(getv("path"), getv("pwd"))

    processed = []

    for ar in arr:
        filtered_data = get_filtered_data(ar)

        mapped_data = get_mapped_data(filtered_data)

        if getv("merge"):
            processed.extend(mapped_data)
            continue

        process_output(mapped_data, getv("format"), getv("print-summary"))

    if processed:
        process_output(processed, getv("format"), getv("print-summary"))


if __name__ == "__main__":
    main()
