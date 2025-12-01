import argparse
from datetime import datetime
import json
import os
from json import JSONDecodeError
import sys

# File where all expenses are stored as JSON
EXPENSE_TRACKER_FILE = 'expensetracker.json'


# ---------- Helper validator functions for argparse ----------

def positive_amount(value: str) -> float:
    """
    argparse type validator:
    - Converts the input to float
    - Ensures the value is strictly positive (> 0)
    Used for: --amount
    """
    amount = float(value)
    if amount <= 0:
        raise argparse.ArgumentTypeError("Amount must be a positive number.")
    return amount


def positive_int(value: str) -> int:
    """
    argparse type validator:
    - Converts the input to int
    - Ensures the value is strictly positive (> 0)
    Used for: --id
    """
    num = int(value)
    if num <= 0:
        raise argparse.ArgumentTypeError("ID must be a positive integer.")
    return num


def month_int(value: str) -> int:
    """
    argparse type validator:
    - Converts the input to int
    - Ensures the value is between 1 and 12 (valid months)
    Used for: --month
    """
    month = int(value)
    if month < 1 or month > 12:
        raise argparse.ArgumentTypeError("Month must be between 1 and 12.")
    return month


# ---------- Core Expense Tracker Class ----------

class ExpenseTracker:
    """Handles loading, saving, and operating on expense data."""

    def __init__(self):
        # Load expenses from file into a list when the object is created
        self.expense = self.load_json()

    def load_json(self):
        """
        Loads the JSON file.
        - If file doesn't exist, creates an empty one.
        - If file is corrupted, resets it to an empty list.
        Returns: list of expenses.
        """
        if not os.path.exists(EXPENSE_TRACKER_FILE):
            # If file does not exist, create an empty list file
            with open(EXPENSE_TRACKER_FILE, 'w') as f:
                json.dump([], f, indent=4)
            return []

        try:
            with open(EXPENSE_TRACKER_FILE, 'r') as json_file:
                return json.load(json_file)
        except JSONDecodeError:
            # If JSON is invalid/corrupt, reset it
            with open(EXPENSE_TRACKER_FILE, 'w') as json_file:
                json.dump([], json_file, indent=4)
            return []

    def get_id(self) -> int:
        """
        Returns the next available ID.
        - If there are no expenses, returns 1.
        - Otherwise, returns max existing ID + 1.
        """
        if not self.expense:
            return 1
        return max(item['id'] for item in self.expense) + 1

    def save_json(self):
        """Writes the current in-memory expense list back to the JSON file."""
        with open(EXPENSE_TRACKER_FILE, 'w') as json_file:
            json.dump(self.expense, json_file, indent=4)

    def add_expense(self, description: str, amount: float):
        """
        Adds a new expense with:
        - auto-generated ID
        - today's date (YYYY-MM-DD)
        - provided description and amount
        """
        exp = {
            'id': self.get_id(),
            'date': datetime.today().strftime('%Y-%m-%d'),
            'description': description,
            'amount': amount
        }
        self.expense.append(exp)
        self.save_json()
        print(f"✅ Expense added successfully. ID({exp['id']})")

    def list_expense(self):
        """
        Prints all expenses in a simple table format.
        """
        if not self.expense:
            print("No expenses recorded yet.")
            return

        # Header row
        print(f"{'ID':<5}{'Date':<15}{'Description':<30}{'Amount':>10}")
        print("-" * 60)

        # Data rows
        for expense in self.expense:
            desc = expense['description']
            # Truncate very long descriptions for neat output
            if len(desc) > 27:
                desc = desc[:27] + "..."

            print(
                f"{expense['id']:<5}"
                f"{expense['date']:<15}"
                f"{desc:<30}"
                f"{expense['amount']:>10.2f}"
            )

    def print_summary(self):
        """
        Prints the total of all expenses.
        """
        total = float(sum(expense['amount'] for expense in self.expense))
        print(f"💰 Total Expenses: ${total:.2f}")

    def delete_expense(self, id: int):
        """
        Deletes an expense by ID.
        - If found, removes it and saves the file.
        - If not found, prints a neat error message.
        """
        if id is None:
            print("❌ Error: Please provide --id for 'delete' command.")
            return

        for expense in self.expense:
            if expense['id'] == id:
                self.expense.remove(expense)
                self.save_json()
                print("✅ Expense deleted successfully.")
                return

        print(f"❌ Error: Expense with ID {id} does not exist.")

    def print_monthly_expense(self, month: int):
        """
        Prints the total expense for a given month (1-12),
        across all years.
        """
        total = 0.0
        for expense in self.expense:
            # Assumes date format is always 'YYYY-MM-DD'
            check_month = int(expense['date'].split('-')[1])
            if check_month == month:
                total += expense['amount']

        print(f"📅 Total Expense for month {month}: ${total:.2f}")


# ---------- Argument Parsing and Command Handling ----------

def parse_arguments():
    """
    Sets up argparse and returns (parser, args).
    Keeping parser so we can use parser.error() later.
    """
    parser = argparse.ArgumentParser(
        description="Simple CLI Expense Tracker"
    )

    # Main command: what action to perform
    parser.add_argument(
        "command",
        choices=['add', 'delete', 'list', 'summary'],
        help="Command to run: add, delete, list, summary"
    )

    # Optional flags used by different commands
    parser.add_argument(
        "--description",
        type=str,
        help="Description of the expense (used with 'add')"
    )
    parser.add_argument(
        "--amount",
        type=positive_amount,
        help="Amount of expense (used with 'add')"
    )
    parser.add_argument(
        "--id",
        type=positive_int,
        help="ID of the expense (used with 'delete')"
    )
    parser.add_argument(
        "--month",
        type=month_int,
        help="Month number (1-12) for monthly summary (used with 'summary')"
    )

    args = parser.parse_args()
    return parser, args


def main():
    parser, args = parse_arguments()
    expenses = ExpenseTracker()

    # ---- Command: add ----
    if args.command == 'add':
        # Ensure both description and amount are provided
        if args.description is None or args.amount is None:
            parser.error("For 'add', both --description and --amount must be provided.")
        expenses.add_expense(args.description, args.amount)

    # ---- Command: list ----
    elif args.command == 'list':
        # For 'list', no extra options are allowed
        not_allowed = ['id', 'month', 'description', 'amount']
        if any(getattr(args, name) is not None for name in not_allowed):
            parser.error("For 'list', usage: python appname.py list")
        expenses.list_expense()

    # ---- Command: summary ----
    elif args.command == 'summary':
        # If month is provided, show monthly summary
        if args.month is not None:
            # For 'summary --month', no other extras should be present
            not_allowed_with_month = ['id', 'description', 'amount']
            if any(getattr(args, name) is not None for name in not_allowed_with_month):
                parser.error("For 'summary --month', only --month is allowed.")
            expenses.print_monthly_expense(args.month)
        else:
            # No month: overall summary
            not_allowed = ['id', 'description', 'amount']
            if any(getattr(args, name) is not None for name in not_allowed):
                parser.error("For 'summary', usage: python appname.py summary")
            expenses.print_summary()

    # ---- Command: delete ----
    elif args.command == 'delete':

        # List of arguments that should NOT be used with delete
        not_allowed = ['description', 'amount', 'month']

        if any(getattr(args, name) is not None for name in not_allowed):
            parser.error("For 'delete', only --id is allowed.")

        # Now ensure ID is provided
        if args.id is None:
            parser.error("For 'delete', --id must be provided.")

        expenses.delete_expense(args.id)


    else:
        # This should never hit because argparse restricts choices,
        # but kept as a safety net.
        parser.error(f"Command {args.command} not recognized.")


if __name__ == '__main__':
    main()
