from datetime import datetime
import sys

try:
    import pandas as pd
except ImportError:
    # fallback to importlib if needed (rare), and show a helpful message if missing
    try:
        import importlib
        pd = importlib.import_module("pandas")
    except ModuleNotFoundError:
        print("Missing dependency: 'pandas'. Install into your venv and rerun.")
        print(r"C:\Users\USER\minti\venv\Scripts\python.exe -m pip install pandas openpyxl")
        sys.exit(1)

class DataManager:
    """
    This handles the reading and writing and core operations of the app
    """
    def __init__(self, filename="transactions.xlsx"):
        self.filename = filename
        self.COLUMNS = ["Date", "Type", "Category", "Amount", "Description", "Is_debt"]
        self.df = self._load_data()

    def _load_data(self):
        try:
            df = pd.read_excel(self.filename)
            print(f"💪 Data loaded successfully from {self.filename}")
        except FileNotFoundError:
            df = pd.DataFrame(columns=self.COLUMNS)
            print(f"opps! {self.filename} not found. Creating a new file")

        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        else:
            df["Date"] = pd.to_datetime(pd.Series(dtype="datetime64[ns]"))

        for col in self.COLUMNS:
            if col not in df.columns:
                df[col] = None

        return df

    def save_data(self):
        self.df.to_excel(self.filename, index=False)
        print(f"🗃️ Data was successfully saved to {self.filename}")

    def add_transaction(self, trans_data: dict) -> bool:
        try:
            if "Date" in trans_data:
                trans_data["Date"] = pd.to_datetime(trans_data["Date"], errors="coerce")
            else:
                trans_data["Date"] = pd.to_datetime(datetime.now())

            if "Amount" in trans_data and isinstance(trans_data["Amount"], str):
                cleaned = trans_data["Amount"].replace("$", "").replace(",", "")
                try:
                    trans_data["Amount"] = float(cleaned)
                except ValueError:
                    pass

            row = {col: trans_data.get(col, None) for col in self.COLUMNS}
            new_row = pd.DataFrame([row], columns=self.COLUMNS)
            self.df = pd.concat([self.df, new_row], ignore_index=True)

            self.save_data()
            print("Transaction recorded")
            return True
        except Exception as e:
            print(f"Error recording transaction: {e}")
            return False

    def record_transaction(self, trans_data: dict) -> bool:
        return self.add_transaction(trans_data)


if __name__ == "__main__":
    minti_data = DataManager()
    new_expense = {
        "Date": datetime.now(),
        "Type": "Expense",
        "Category": "Clothing",
        "Amount": 200,
        "Description": "New items",
        "Is_debt": False
    }
    minti_data.record_transaction(new_expense)
    print(minti_data.df.tail())



