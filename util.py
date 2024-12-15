import csv
import json
import os
import numpy as np
from datetime import datetime
from typing import TypedDict

import pdfplumber

START_ENTRY = "BEGINNING BALANCE"
END_ENTRY = "TOTAL DEBIT"
NOTE_START_ENTRY = "Perhation / Note"
NOTE_END_ENTRY = (
    "ENTRY DATE TRANSACTION DESCRIPTION TRANSACTION AMOUNT STATEMENT BALANCE"
)
OUTPUT_FILENAME = "EXTRACTED"

Output = TypedDict("Output", {"date": str, "desc": str, "bal": float, "trans": float})


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


def output_extracted_data(value, type: str = "csv"):
    is_json = type == "json"
    newline = None if is_json else ""

    with open(
        f"{OUTPUT_FILENAME}-{datetime.now()}.{type}", "w", newline=newline
    ) as o_file:
        if is_json:
            json.dump(value, o_file, indent=4)
        else:
            writer = csv.DictWriter(o_file, ["date", "desc", "trans", "bal"])
            writer.writeheader()
            writer.writerows(value)


def print_acc_summary(value):
    tracking_bal = 0.0
    tracking_cred = 0.0
    tracking_deb = 0.0

    CYAN = "\033[96m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    for i, obj in enumerate(value):
        if i == 0:

            print(f"{CYAN}BEGINNING BALANCE{RESET}: {GREEN}{obj['bal']:.2f}{RESET}")
            tracking_bal = obj["bal"]
        else:
            is_credit = obj["trans"] > 0
            if is_credit:
                tracking_cred += obj["trans"]
            else:
                tracking_deb += obj["trans"]

            transaction_color = GREEN if is_credit else RED

            transaction = f"BAL:{round(tracking_bal,2)} => {transaction_color}{obj['trans']:.2f}{RESET}"
            new_balance = f"{BLUE}{obj['bal']:.2f}{RESET}"

            balance_check = (
                f"{YELLOW}✅{RESET}"
                if round(tracking_bal + obj["trans"], 2) == obj["bal"]
                else f"{YELLOW}❌{RESET}"
            )

            print(f"{transaction}....NEW BAL: {new_balance} {balance_check}")

            tracking_bal += obj["trans"]

    print(
        f"TOTAL BALANCE: {BLUE}{round(tracking_bal,2)}{RESET}, TOTAL CREDIT: {GREEN}{round(tracking_cred,2)}{RESET}, TOTAL DEBIT: {RED}{round(tracking_deb,2)}{RESET}"
    )


def get_filtered_data(arr):
    indexes = [0, len(arr)]

    for i, x in enumerate(arr):
        if x.startswith(START_ENTRY):
            indexes[0] = i
        elif x.startswith(END_ENTRY):
            indexes[1] = i + 1
            break

    filtered = arr[indexes[0] : indexes[1]]
    temp = np.array(filtered)
    notes_indices = np.where(
        np.char.startswith(temp, NOTE_START_ENTRY)
        | np.char.startswith(temp, NOTE_END_ENTRY)
    )[0].tolist()

    expanded = expand_ranges(notes_indices)

    arr = []

    for i, v in enumerate(temp):
        if i not in expanded:
            arr.append(v)

    return arr


def get_mapped_data(arr):
    narr = []

    i = 0
    while i < len(arr):
        current = arr[i]
        splitted = current.split()
        obj: Output = {"desc": "", "bal": 0, "trans": 0, "date": ""}

        if i != 0 and (not (is_valid_date(splitted[0]))):
            i += 1
            continue
        elif i == 0:
            obj["desc"] = " ".join(splitted[0:2])
            obj["bal"] = parse_acc_value(splitted[2])
            narr.append(obj)
        elif is_valid_date(splitted[0]):
            obj["date"] = splitted[0]
            obj["trans"] = parse_acc_value(splitted[-2])
            obj["bal"] = parse_acc_value(splitted[-1])
            obj["desc"] = " ".join(splitted[1:-2])

            i += 1
            while i < len(arr) and not is_valid_date(arr[i].split()[0]):
                obj["desc"] = obj["desc"] + " " + " ".join(arr[i].split())
                i += 1
            narr.append(obj)
            continue
        i += 1

    return narr


def kebab_to_snake(kebab_str: str) -> str:
    return kebab_str.replace("-", "_")


def read_single_pdf_file(path, pwd):
    with pdfplumber.open(path, password=pwd) as pdf:
        return [
            txt
            for pg, page in enumerate(pdf.pages)
            for txt in page.extract_text().split("\n")
        ]


def read_pdfs(path, pwd):
    pdf_files = []
    try:
        for filename in os.listdir(path):
            if filename.endswith(".pdf"):  # Check if the file is a PDF
                file_path = os.path.join(path, filename)
                pdf_files.append(read_single_pdf_file(file_path, pwd))
    except NotADirectoryError as e:
        pdf_files.append(read_single_pdf_file(path, pwd))

    return pdf_files
