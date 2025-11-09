from fileinput import filename
from datetime import datetime
import pandas as pd

class DataManager:
    """
    This handles the reading and writing and core operations of the app
    """
    def __init__(self, filename="transactions.xlsx"):
        self.filename = filename
        # Use column names consistent with other modules (e.g., app.py)
        self.COLUMNS = ["Date", "Type", "Category", "Amount", "Description", "Is_debt"]
        self.df = self._load_data()

    def _load_data(self):
        "This loads the data from the excel file (or creates an empty DataFrame)"
        try:
            df = pd.read_excel(self.filename)
            print(f"💪 Data loaded successfully from {self.filename}")
        except FileNotFoundError:
            df = pd.DataFrame(columns=self.COLUMNS)
            print(f"opps! {self.filename} not found. Creating a new file")

        # Ensure Date column exists and is datetime dtype
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        else:
            df["Date"] = pd.to_datetime(pd.Series(dtype="datetime64[ns]"))

        # Make sure all expected columns exist
        for col in self.COLUMNS:
            if col not in df.columns:
                df[col] = None

        return df

    def save_data(self):
        self.df.to_excel(self.filename, index=False)
        print(f"🗃️ Data was successfully saved to {self.filename}")

    def add_transaction(self, trans_data: dict) -> bool:
        """
        Adds a transaction dict to the DataFrame and saves it.
        trans_data keys should match self.COLUMNS (case-sensitive).
        """
        try:
            # Accept "Date" as string or datetime
            if "Date" in trans_data:
                trans_data["Date"] = pd.to_datetime(trans_data["Date"], errors="coerce")
            else:
                trans_data["Date"] = pd.to_datetime(datetime.now())

            # Ensure Amount is numeric if possible (strip $ and commas)
            if "Amount" in trans_data and isinstance(trans_data["Amount"], str):
                cleaned = trans_data["Amount"].replace("$", "").replace(",", "")
                try:
                    trans_data["Amount"] = float(cleaned)
                except ValueError:
                    pass

            # Build new row ensuring all columns present
            row = {col: trans_data.get(col, None) for col in self.COLUMNS}
            new_row = pd.DataFrame([row], columns=self.COLUMNS)
            self.df = pd.concat([self.df, new_row], ignore_index=True)

            self.save_data()
            print("Yess gurl! Your transaction has been recorded successfully💃")
            return True
        except Exception as e:
            print(f"Opps! There was an error recording your transaction :{e}")
            return False

    def record_transaction(self, trans_data: dict) -> bool:
        """
        Backwards-compatible method name used elsewhere in the codebase.
        Delegates to add_transaction.
        """
        return self.add_transaction(trans_data)


# Now you test the DataManager class directly
if __name__ == "__main__":
    minti_data = DataManager()

    # Now let's define a new transaction (columns aligned with this class)
    new_expense = {
        "Date": datetime.now(),
        "Type": "Expense",
        "Category": "Clothing",
        "Amount": 200,
        "Description": "New Ballet Flats, Pauline bag, Scarf",
        "Is_debt": False
    }

    # Record the transaction
    minti_data.record_transaction(new_expense)

    # View the result (last few rows)
    print("\n--- Current Transactions ---")
    print(minti_data.df.tail())



