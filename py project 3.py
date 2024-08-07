import json
import os
from datetime import datetime

class Expense:
    def __init__(self, description, amount, category, date):
        self.description = description
        self.amount = amount
        self.category = category
        self.date = date

    def to_dict(self):
        return {
            "description": self.description,
            "amount": self.amount,
            "category": self.category,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['description'], data['amount'], data['category'], data['date'])

class ExpenseTracker:
    def __init__(self, filename='expenses.json'):
        self.filename = filename
        self.expenses = self.load_expenses()

    def load_expenses(self):
        """Load expenses from a JSON file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return [Expense.from_dict(item) for item in data]
        return []

    def save_expenses(self):
        """Save expenses to a JSON file."""
        with open(self.filename, 'w') as file:
            json.dump([expense.to_dict() for expense in self.expenses], file)

    def add_expense(self, description, amount, category):
        """Add an expense to the tracker."""
        date = datetime.now().strftime("%Y-%m-%d")
        expense = Expense(description, amount, category, date)
        self.expenses.append(expense)
        self.save_expenses()
        print(f"Added expense: {expense.description} - ${expense.amount:.2f} ({expense.category}) on {expense.date}")

    def total_expenses(self):
        """Calculate the total amount spent."""
        return sum(expense.amount for expense in self.expenses)

    def monthly_summary(self):
        """Generate a summary of expenses by month."""
        summary = {}
        for expense in self.expenses:
            month = expense.date[:7]  # Get the year-month format
            summary[month] = summary.get(month, 0) + expense.amount
        return summary

    def category_summary(self):
        """Generate a summary of expenses by category."""
        summary = {}
        for expense in self.expenses:
            summary[expense.category] = summary.get(expense.category, 0) + expense.amount
        return summary

    def display_expenses(self):
        """Display all recorded expenses."""
        if not self.expenses:
            print("No expenses recorded.")
            return
        print("Expenses:")
        for expense in self.expenses:
            print(f"{expense.date} - {expense.description}: ${expense.amount:.2f} [{expense.category}]")

def main():
    tracker = ExpenseTracker()

    while True:
        print("\nExpense Tracker Menu")
        print("1. Add Expense")
        print("2. View Total Expenses")
        print("3. View Monthly Summary")
        print("4. View Category Summary")
        print("5. Display All Expenses")
        print("6. Exit")

        choice = input("Choose an option: ")

        try:
            if choice == '1':
                description = input("Enter expense description: ")
                amount = float(input("Enter expense amount: "))
                category = input("Enter expense category: ")
                tracker.add_expense(description, amount, category)
            elif choice == '2':
                print(f"Total Expenses: ${tracker.total_expenses():.2f}")
            elif choice == '3':
                summary = tracker.monthly_summary()
                print("Monthly Summary:")
                for month, total in summary.items():
                    print(f"{month}: ${total:.2f}")
            elif choice == '4':
                summary = tracker.category_summary()
                print("Category Summary:")
                for category, total in summary.items():
                    print(f"{category}: ${total:.2f}")
            elif choice == '5':
                tracker.display_expenses()
            elif choice == '6':
                print("Exiting the Expense Tracker.")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter numerical values for amounts.")

if __name__ == "__main__":
    main()
