## MayBank Monthly Account Statement Data Extraction (Personal/Individual Account)

This project extracts financial data from MBB PDF account statement.

### Features

- output it in either JSON and CSV formats.
- read folder extract data in single or individual files
  -The extracted data includes date, description, transaction amount, balance exactly as the statement.

Example of the JSON output:

```json
[
  {
    "date": "01/01/2024",
    "desc": "Deposit from client",
    "bal": 1050.0,
    "trans": 50.0
  },
  {
    "date": "02/01/2024",
    "desc": "Purchase - Office Supplies",
    "bal": 1030.0,
    "trans": -20.0
  }
]
```

Example of the CSV output:

```csv
date,desc,trans,bal
01/01/2024,Deposit from client,50.00,1050.00
02/01/2024,Purchase - Office Supplies,-20.00,1030.00
```

## Getting started:

1. cd into the project folder.
2. install virtual enviroment:
   `python -m venv venv`
3. activate virtual enviroment:

- on linux =>`source venv/bin/activate`
  -on windows =>`venv\Scripts\activate`

4. install dependencies
   `pip install -r requirements.txt`

5. on terminal, run
   `python3 main.py --file-path=account_statement.pdf --file-password=01Mar2000`

6. for more, run
   ` python3 main.py --help`