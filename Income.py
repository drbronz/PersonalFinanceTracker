from Transaction import Transaction

# Inheritance: Income inherits from Transaction
class Income(Transaction):
    def __init__(self, trans_id, date, amount, category, description):
        super().__init__(trans_id, date, amount, category, description)

    # Polymorphism: same method name, different behavior
    def signed_amount(self):
        return float(self.amount)
