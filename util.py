from datetime import datetime


def is_valid_date(date_str: str) -> bool:
    try:
        # Attempt to parse the date string in the format "dd/mm/yy"
        datetime.strptime(date_str, "%d/%m/%y")
        return True
    except ValueError:
        return False


def expand_ranges(arr: list[int]):
    expanded = []

    for ar in range(0, len(arr), 2):
        f = arr[ar]
        s = arr[ar + 1]
        for i in range(f, s + 1):
            expanded.append(i)

    return expanded


def parse_acc_value(value: str) -> float:
    value = value.replace(",", "")
    if value.endswith("-"):
        # Remove the trailing '-' and subtract 1
        return -float(value[:-1])
    elif value.endswith("+"):
        # Remove the trailing '+' and add 1
        return float(value[:-1])
    else:
        # If no '+' or '-' at the end, just return the integer
        return float(value)
