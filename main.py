import click
from util import (
    get_filtered_data,
    get_mapped_data,
    kebab_to_snake,
    output_extracted_data,
    print_acc_summary,
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
    "--single",
    default=False,
    help="merge output into single file if folder or multiple PDF passed",
)
@click.option(
    "--sort",
    default=False,
    help="sort by transaction date",
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
def main(*args, **kwargs):
    def getv(k):
        return kwargs[kebab_to_snake(k)]

    arr = read_pdfs(getv("path"), getv("pwd"))

    for ar in arr:
        filtered_data = get_filtered_data(ar)

        mapped_data = get_mapped_data(filtered_data)

        output_extracted_data(mapped_data, getv("format"))

        if getv("print-summary"):
            print_acc_summary(mapped_data)


if __name__ == "__main__":
    main()
