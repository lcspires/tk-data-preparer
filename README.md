# Tk Data Preparer - MVP

**Tk Data Preparer** is a simple Python Tkinter GUI tool to clean, preprocess, and export Excel (`.xls`, `.xlsx`), CSV, and TXT files to a formatted TXT file.

This is the **Day 1 MVP** version: basic GUI with file selection, column listing, and minimal data cleaning.

---

## Features

- Import Excel, CSV, or TXT files.
- Remove extra spaces from all string columns.
- Filter rows based on a minimum character length in the first column.
- Remove duplicates based on the first column.
- Export cleaned data to a semicolon-delimited TXT file.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/lcspires/tk-data-preparer.git
cd tk-data-preparer
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the GUI application:

```bash
python -m tk_data_preparer.app
```

1. Select an Excel, CSV, or TXT file.
2. View the columns in the listbox.
3. Click "Generate TXT" to save the cleaned data.

## Test

Tests are written using pytest. To run:

```bash
python -m pytest -q
```

## Project Structure

```bash
tk-data-preparer/
├── tk_data_preparer/
│   ├── __init__.py
│   ├── app.py
│   ├── logic.py
│   └── tooltip.py
├── tests/
│   └── test_logic.py
├── requirements.txt
└── README.md
```
---

## License

This project is licensed under the **MIT License**.  
You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this software, provided that the original copyright notice and this permission notice are included in all copies or substantial portions of the software.

## Author

**Lucas Ferreira**  
[LinkedIn: https://www.linkedin.com/in/lucasopf/]