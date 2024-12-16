# MayBank email statement delivery to CSV or JSON (Monthly)

This project extracts financial data from Maybank statement to JSON or CSV.

### Features

- output it in either JSON and CSV formats.
- read folder extract data into single or individual files
  -The extracted data includes date, description, transaction amount, balance exactly as the statement.

Example of the JSON output:

```json
[
  {
    "date": "01/01/2024",
    "desc": "Deposit from client",
    "trans": 50.0,
    "bal": 1050.0
  },
  {
    "date": "02/01/2024",
    "desc": "Purchase - Office Supplies",
    "trans": -20.0,
    "bal": 1030.0
  }
]
```

Example of the CSV output:

```csv
date,desc,trans,bal
01/01/2024,Deposit from client,50.00,1050.00
02/01/2024,Purchase - Office Supplies,-20.00,1030.00
```

## Getting Started

Follow these steps to set up and run the project:

### 1. Navigate to the Project Directory

```bash
cd <project-folder>
```

### 2. Install Virtual Environment

Create a virtual environment:

```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

- **On Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```
- **On Windows:**
  ```bash
  venv\Scripts\activate
  ```

### 4. Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### 5. Run the Application

To execute the program, use:

```bash
python3 main.py --path=example.pdf --pwd=01Mar2000
```

### 6. View Help Options

For more details on usage:

```bash
python3 main.py --help
```

---

## Usage

### Command:

```bash
main.py [OPTIONS]
```

### Options:

| Option                    | Description                                                             |
| ------------------------- | ----------------------------------------------------------------------- |
| `--path TEXT`             | Path to the file or folder containing PDF statements.                   |
| `--pwd TEXT`              | Password for PDF statements, assuming the same password for every file. |
| `--format TEXT`           | Output file format, either `csv` or `json`.                             |
| `--print-summary BOOLEAN` | Print a summary of the account statement.                               |
| `--merge BOOLEAN`         | Output only a single merged file.                                       |
| `--help`                  | Show help information and exit.                                         |

---

### Example Command:

To process a PDF file with the password `01Mar2000`:

```bash
python3 main.py --path=example.pdf --pwd=01Mar2000
python3 main.py --path=statements-folder --pwd=01Mar2000 #example extracting all data from folder containing PDFs
```
