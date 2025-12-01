

# 📘 Expense Tracker CLI (Python)

A simple and beginner-friendly **Command Line Expense Tracker** built in Python.
It supports adding, listing, deleting, and summarizing expenses.
Data is stored locally in a JSON file.

---

## ⭐ Features

* Add expenses with description, amount, and auto-generated ID
* View all expenses in a clean table format
* Delete expenses by ID
* View total expenses
* View monthly expenses
* Validates input using `argparse`
* Stores all data in `expensetracker.json`

---

## 📁 Project Structure

```
.
├── expensetracker.json   # Auto-created storage file
├── app.py                # Main CLI application
└── README.md             # Documentation
```

---

## 🔧 Installation

### 1. Clone the repository

```
git clone <your-repo-url>
cd <project-folder>
```

### 2. Run with Python

Make sure Python 3.x is installed.

```
python app.py --help
```

---

## 🚀 Usage

### 📌 1. Add an Expense

```
python app.py add --description "Lunch" --amount 120
```

### 📌 2. List All Expenses

```
python app.py list
```

### 📌 3. Delete an Expense

```
python app.py delete --id 3
```

### 📌 4. Show Total Summary

```
python app.py summary
```

### 📌 5. Show Monthly Summary

```
python app.py summary --month 3
```

---

## 📝 Commands Overview

### **add**

| Argument        | Required | Description                    |
| --------------- | -------- | ------------------------------ |
| `--description` | Yes      | What you spent on              |
| `--amount`      | Yes      | Amount spent (positive number) |

```
python app.py add --description "Snacks" --amount 50
```

---

### **list**

Displays all expenses.
❌ Does **not** allow: `--id`, `--amount`, `--description`, `--month`

```
python app.py list
```

---

### **delete**

| Argument | Required | Description                 |
| -------- | -------- | --------------------------- |
| `--id`   | Yes      | ID of the expense to delete |

```
python app.py delete --id 2
```

---

### **summary**

Two modes:

#### ★ Full summary

```
python app.py summary
```

#### ★ Monthly summary

```
python app.py summary --month 4
```

❌ `--id`, `--description`, `--amount` are **not allowed** here.

---

## 💾 Data Format (JSON)

Each expense is stored like this:

```json
{
    "id": 1,
    "date": "2025-01-16",
    "description": "Lunch",
    "amount": 120
}
```

---

## 🛡 Validation Rules

* Amount must be **positive number**
* ID must be **positive integer**
* Month must be **between 1 and 12**
* Required fields must be provided depending on the command
* Optional arguments must not be used with some commands

---

## 🤝 Credits

This project is created for learning Python CLI tools, JSON storage, and argument parsing using `argparse`.

This project is inspired by the **GitHub User Activity** challenge on Roadmap.sh:  
➡️ https://roadmap.sh/projects/expense-tracker

