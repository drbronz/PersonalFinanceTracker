import json
import os

from Ledger import Ledger
from Income import Income
from Expense import Expense


class StorageManager:
    def save(self, filename, ledger):
        data = {
            "transactions": []
        }

        for t in ledger.list_all():
            data["transactions"].append(t.to_dict())

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self, filename):
        ledger = Ledger()

        if not os.path.exists(filename):
            return ledger

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        items = data.get("transactions", [])

        for d in items:
            t_type = (d.get("type") or "").lower()
            trans_id = d.get("id")
            date = d.get("date")
            amount = float(d.get("amount"))
            category = d.get("category")
            description = d.get("description", "")

            if t_type == "income":
                t = Income(trans_id, date, amount, category, description)
            elif t_type == "expense":
                t = Expense(trans_id, date, amount, category, description)
            else:
                continue

            ledger.add_transaction(t)

        return ledger
