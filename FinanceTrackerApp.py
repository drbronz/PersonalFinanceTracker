import uuid

from StorageManager import StorageManager
from Ledger import Ledger
from Income import Income
from Expense import Expense
from InputValidator import InputValidator

class FinanceTrackerApp:

    def __init__(self, data_file: str = "finance_data.json"):
        self.data_file = data_file
        self.storage = StorageManager()
        self.validator = InputValidator()
        self.ledger = self.storage.load(self.data_file)  # Auto-load on start

    def autosave(self):
        self.storage.save(self.data_file, self.ledger)

    @classmethod
    def run(cls, data_file: str = "finance_data.json"):
        app = cls(data_file)
        app._main_loop()

    def _main_loop(self):
        try:
            while True:
                print("\n=== Personal Finance Tracker ===")
                print("1) Transactions")
                print("2) Reports")
                print("3) Exit")

                choice = input("Choose an option: ").strip()

                if choice == "1":
                    self._transactions_menu()
                elif choice == "2":
                    self._reports_menu()
                elif choice == "3":
                    self.autosave()  # Auto-save on exit
                    print("Goodbye.")
                    break
                else:
                    print("Invalid choice. Try again.")
        except KeyboardInterrupt:
            self.autosave()
            print("\nSaved. Goodbye.")

    def _transactions_menu(self):
        while True:
            print("\n--- Transactions Menu ---")
            print("1) Add Transaction")
            print("2) List All")
            print("3) Delete by ID")
            print("4) Back")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self._add_transaction()
            elif choice == "2":
                self._list_all()
            elif choice == "3":
                self._delete_by_id()
            elif choice == "4":
                return
            else:
                print("Invalid choice. Try again.")

    def _add_transaction(self):
        print("\nAdd Transaction")
        print("1) Income")
        print("2) Expense")
        t_choice = input("Choose type: ").strip()

        if t_choice == "1":
            t_class = Income
            t_type = "Income"
        elif t_choice == "2":
            t_class = Expense
            t_type = "Expense"
        else:
            print("Invalid type.")
            return

        date = self.validator.get_valid_date("Step 1: Enter date (YYYY-MM-DD): ")
        amount = self.validator.get_positive_number("Step 2: Enter amount (> 0): ")
        category = self.validator.get_non_empty("Step 3: Enter category (not empty): ")
        description = input("Step 4: Enter description (optional): ").strip()

        trans_id = str(uuid.uuid4())[:8]
        t = t_class(trans_id, date, amount, category, description)

        self.ledger.add_transaction(t)
        self.autosave()
        print(f"{t_type} added with ID: {trans_id}")

    def _list_all(self):
        tx = self.ledger.list_all()
        if not tx:
            print("No transactions yet.")
            return

        print("\nID | Date | Category | Amount | Description")
        print("-" * 60)
        for t in tx:
            print(str(t))

    def _delete_by_id(self):
        trans_id = input("Enter transaction ID to delete: ").strip()
        ok = self.ledger.delete_transaction(trans_id)
        if ok:
            self.autosave()
            print("Deleted.")
        else:
            print("Transaction not found.")

    def _reports_menu(self):
        while True:
            print("\n--- Reports Menu ---")
            print("1) Totals (income, expense, net)")
            print("2) Totals by Category")
            print("3) Monthly Summary")
            print("4) Back")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self._report_totals()
            elif choice == "2":
                self._report_by_category()
            elif choice == "3":
                self._report_monthly()
            elif choice == "4":
                return
            else:
                print("Invalid choice. Try again.")

    def _report_totals(self):
        income = self.ledger.total_income()
        expense = self.ledger.total_expense()
        net = self.ledger.net_balance()
        print(f"Total Income:  {income:.2f}")
        print(f"Total Expense: {expense:.2f}")
        print(f"Net Balance:   {net:.2f}")

    def _report_by_category(self):
        totals = self.ledger.totals_by_category()
        if not totals:
            print("No transactions yet.")
            return
        print("\nCategory Totals (net):")
        for cat, val in totals.items():
            sign = "+" if val >= 0 else "-"
            print(f"- {cat}: {sign}{abs(val):.2f}")

    def _report_monthly(self):
        yyyy_mm = input("Enter month (YYYY-MM): ").strip()
        if not self.validator.valid_month(yyyy_mm):
            print("Invalid month format. Use YYYY-MM (example: 2026-01).")
            return

        summary = self.ledger.monthly_summary(yyyy_mm)
        print(f"\nMonthly Summary: {summary['month']}")
        print(f"Income:  {summary['income']:.2f}")
        print(f"Expense: {summary['expense']:.2f}")
        print(f"Net:     {summary['net']:.2f}")
