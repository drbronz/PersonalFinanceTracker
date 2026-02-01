from datetime import datetime

class InputValidator:
    """Handles validated user input so the app never crashes on bad input."""

    def get_valid_date(self, prompt: str) -> str:
        while True:
            raw = input(prompt).strip()
            try:
                datetime.strptime(raw, "%Y-%m-%d")
                return raw
            except ValueError:
                print("Invalid date. Use YYYY-MM-DD (example: 2026-01-28).")

    def get_positive_number(self, prompt: str) -> float:
        while True:
            raw = input(prompt).strip()
            try:
                val = float(raw)
                if val > 0:
                    return val
                print("Amount must be greater than 0.")
            except ValueError:
                print("Please enter a valid number.")

    def get_non_empty(self, prompt: str) -> str:
        while True:
            raw = input(prompt).strip()
            if raw:
                return raw
            print("This field cannot be empty.")

    def valid_month(self, yyyy_mm: str) -> bool:
        try:
            datetime.strptime(yyyy_mm, "%Y-%m")
            return True
        except ValueError:
            return False
