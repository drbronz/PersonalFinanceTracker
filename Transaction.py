# Base class (Abstraction idea): common fields for all transactions
class Transaction:
    def __init__(self, trans_id, date, amount, category, description):
        self.id = trans_id
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description

    # Child classes must override this (simple abstraction)
    def signed_amount(self):
        raise NotImplementedError("signed_amount() must be implemented in child classes")

    def to_dict(self):
        return {
            "type": self.__class__.__name__.lower(),   # "income" or "expense"
            "id": self.id,
            "date": self.date,
            "amount": self.amount,
            "category": self.category,
            "description": self.description
        }

    def __str__(self):
        sign = "+" if self.signed_amount() >= 0 else "-"
        return f"{self.id} | {self.date} | {self.category} | {sign}{abs(self.amount):.2f} | {self.description}"
