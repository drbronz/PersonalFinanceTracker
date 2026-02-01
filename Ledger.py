# Ledger encapsulates and manages transactions
class Ledger:
    def __init__(self):
        # Encapsulation: internal list (do not edit from outside directly)
        self._transactions = []

    def add_transaction(self, transaction):
        self._transactions.append(transaction)

    def delete_transaction(self, trans_id):
        for t in self._transactions:
            if t.id == trans_id:
                self._transactions.remove(t)
                return True
        return False


    def list_all(self):
        return list(self._transactions)

    def filter_by_month(self, yyyy_mm):
        result = []
        for t in self._transactions:
            if str(t.date).startswith(yyyy_mm):
                result.append(t)
        return result

    # Polymorphism in action: Income returns +, Expense returns -
    def net_balance(self):
        total = 0.0
        for t in self._transactions:
            total += t.signed_amount()
        return total

    def total_income(self):
        total = 0.0
        for t in self._transactions:
            if t.signed_amount() > 0:
                total += t.signed_amount()
        return total

    def total_expense(self):
        total = 0.0
        for t in self._transactions:
            if t.signed_amount() < 0:
                total += abs(t.signed_amount())
        return total

    def totals_by_category(self):
        totals = {}
        for t in self._transactions:
            if t.category not in totals:
                totals[t.category] = 0.0
            totals[t.category] += t.signed_amount()
        return totals

    def monthly_summary(self, yyyy_mm):
        tx = self.filter_by_month(yyyy_mm)
        income = 0.0
        expense = 0.0
        net = 0.0

        for t in tx:
            value = t.signed_amount()
            net += value
            if value > 0:
                income += value
            else:
                expense += abs(value)

        return {"month": yyyy_mm, "income": income, "expense": expense, "net": net}

    def clear(self):
        self._transactions.clear()

    def count(self):
        return len(self._transactions)
