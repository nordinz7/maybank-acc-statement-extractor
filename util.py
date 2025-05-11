import csv
import json
from datetime import datetime
import os

from maybankpdf2json import MaybankPdf2Json


OUTPUT_FILENAME = "MBB_EXTRACTED"


def output_extracted_data(value, options):
    type = options["format"]
    is_json = type == "json"
    newline = None if is_json else ""
    date = datetime.strptime(value[2]["date"], "%d/%m/%y")
    file_date = date.strftime("%Y%m %B ") if not options["merge"] else "-COMBINED"

    with open(f"{OUTPUT_FILENAME}{file_date}.{type}", "w", newline=newline) as o_file:
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
            print("==============================================================")
            print(f"{CYAN}BEGINNING BALANCE{RESET}: {GREEN}{obj['bal']:.2f}{RESET}")
            tracking_bal = obj["bal"]
        else:
            is_credit = obj["trans"] > 0
            if is_credit:
                tracking_cred += obj["trans"]
            else:
                tracking_deb += obj["trans"]

            transaction_color = GREEN if is_credit else RED

            transaction = f"{obj['date']} BAL:{round(tracking_bal,2)} => {transaction_color}{obj['trans']:.2f}{RESET}"
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


def process_output(arr, options):
    if options["output"]:
        output_extracted_data(arr, options)
    else:
        print(json.dumps(arr, indent=4))

    if options["print_summary"]:
        print_acc_summary(arr)


def read_pdf(file_path, pwd):
    with open(file_path, "rb") as file:
        reader = MaybankPdf2Json(file, pwd)
        return reader.json()


def read_from_file_or_folder(path, pwd):
    if path.endswith(".pdf"):
        return read_pdf(path, pwd)
    else:
        # Assuming the path is a folder and we need to read all PDF files in it
        data = []
        for filename in os.listdir(path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(path, filename)
                data.append(read_pdf(file_path, pwd))
        return data
