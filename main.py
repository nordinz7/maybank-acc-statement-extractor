import pdfplumber
import numpy as np
import json
import csv
from dotenv import load_dotenv
import os

from util import is_valid_date, expand_ranges, parse_acc_value

from typing import List, TypedDict

load_dotenv()

START_ENTRY = "BEGINNING BALANCE"
END_ENTRY = "TOTAL DEBIT"

NOTE_START_ENTRY = "Perhation / Note"
NOTE_END_ENTRY = (
    "ENTRY DATE TRANSACTION DESCRIPTION TRANSACTION AMOUNT STATEMENT BALANCE"
)

Output = TypedDict("Output", {"date": str, "desc": str, "bal": float, "trans": float})

text_splitted = []
# Open the PDF file
with pdfplumber.open(
    os.getenv("FILE_PATH"), password=os.getenv("FILE_PASSWORD")
) as pdf:
    # Extract text from each page
    with open("output.txt", "w") as output_file:
        for page_number, page in enumerate(pdf.pages):
            text = page.extract_text()  # Extract text from the page
            output_file.write(text)
            text_splitted.append(text.split("\n"))

all_chars: List[str] = [x for text in text_splitted for x in text]

indexes = [0, len(all_chars)]

for i, x in enumerate(all_chars):
    if x.startswith(START_ENTRY):
        indexes[0] = i
    elif x.startswith(END_ENTRY):
        indexes[1] = i + 1
        break

filtered = all_chars[indexes[0] : indexes[1]]


temp = np.array(filtered)
notes_indices = np.where(
    np.char.startswith(temp, NOTE_START_ENTRY)
    | np.char.startswith(temp, NOTE_END_ENTRY)
)[0].tolist()

expanded = expand_ranges(notes_indices)

arr = []

# Iterate over the array
for i, v in enumerate(temp):
    if i not in expanded:
        arr.append(v)

rtn = []
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
        rtn.append(obj)
    elif is_valid_date(splitted[0]):
        obj["date"] = splitted[0]
        obj["trans"] = parse_acc_value(splitted[-2])
        obj["bal"] = parse_acc_value(splitted[-1])
        obj["desc"] = " ".join(splitted[1:-2])

        i += 1
        while i < len(arr) and not is_valid_date(arr[i].split()[0]):
            obj["desc"] = obj["desc"] + " " + " ".join(arr[i].split())
            i += 1
        rtn.append(obj)
        continue
    i += 1

with open("extracted.json", "w") as json_file:
    json.dump(rtn, json_file, indent=4)

# Writing to a CSV file
with open("extracted.csv", "w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, ["date", "desc", "trans", "bal"])
    writer.writeheader()  # Write the header row
    writer.writerows(rtn)  # Write the data rows

tracking_bal = 0.0
tracking_cred = 0.0
tracking_deb = 0.0

# Define ANSI escape codes for colors
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"

for i, obj in enumerate(rtn):
    if i == 0:
        # Display beginning balance in cyan
        print(f"{CYAN}BEGINNING BALANCE{RESET}: {GREEN}{obj['bal']:.2f}{RESET}")
        tracking_bal = obj["bal"]
    else:
        is_credit = obj["trans"] > 0
        if is_credit:
            tracking_cred += obj["trans"]
        else:
            tracking_deb += obj["trans"]

        transaction_color = GREEN if is_credit else RED

        # Format transaction and balance
        transaction = f"BAL:{round(tracking_bal,2)} => {transaction_color}{obj['trans']:.2f}{RESET}"
        new_balance = f"{BLUE}{obj['bal']:.2f}{RESET}"

        # Check if the balance is correct and highlight
        balance_check = (
            f"{YELLOW}✅{RESET}"
            if round(tracking_bal + obj["trans"], 2) == obj["bal"]
            else f"{YELLOW}❌{RESET}"
        )

        # Print formatted output
        print(f"{transaction}....NEW BAL: {new_balance} {balance_check}")

        # Update tracking balance
        tracking_bal += obj["trans"]

print(
    f"TOTAL BALANCE: {BLUE}{round(tracking_bal,2)}{RESET}, TOTAL CREDIT: {GREEN}{round(tracking_cred,2)}{RESET}, TOTAL DEBIT: {RED}{round(tracking_deb,2)}{RESET}"
)
