from main import DataManager
import pandas as pd
from datetime import datetime

class MintLogic:
    """"Handles budget calculations, feedback and financial motivation"""
    def __init__(self, filename="transactions.xlsx"):
        self.data_manager = DataManager(filename)
        self.monthly_budget = 1500.00  ## This is just a placeholder and will later be user set
def get_monthly_summary(self, year_month=None):      
    """Calculates the total income, expenses and category breakdown for a given month"""
    """Also if year_month is None the default is the current month"""
    df=self.data_manager.df

    if year_month is None:
        """"If there is no specified month, use the current month"""
        year_month=datetime.now().strftime("%Y-%m")

    """Filter the DataFrame for the specified month"""
    monthly_data= df[df["Date"].dt.strftime("%Y-%m")==year_month]


    """Calculate total income and total expenses"""
    total_income= monthly_data[monthly_data["Type"]=="Income"]["Amount"].sum()
    total_expenses=monthly_data[monthly_data["Type"]=="Expense"]["Amount"].sum()

    """Calculates savings total (Birthdays, events, etc)"""
    savings_total= monthly_data[monthly_data["Type"]=="Savings"]
    savings_breakdown= savings_total.groupby("Category")["Amount"].sum().to_dict()
    ##Return the monthly summary as a dictionary
    return{
    "year_month":year_month,
    "total_expenses": total_expenses,
    "total_income": total_income,
    "savings_breakdown": savings_breakdown,
    "current_spending": total_expenses,
    "net_balance": total_income- total_expenses- savings_total["Amount"].sum()
    }

def generated_feedback(self, spending):
    """"Generates motivational feedback based on monthly budget"""
    budget_used_percentage= (spending/self.MONTHLY_BUDGET)*100
    if spending> self.MONTHLY_BUDGET:
        return (
                "Jeez girl, you overspent. Let’s get it together. "
                "Sis, slow down—your wallet’s crying 😭."
         ) 

    elif budget_used_percentage>80:
        return(
            
                f"🚨 Warning: You've used {budget_used_percentage:.0f}% of your budget. "
                "One more expense and you're in trouble! Stay mindful. 🧠"
        )
    
    else:
        return(
            "Yes queen 👑, you’re killing it with those savings! "
                "You’re smashing your goals and your budget is healthy. 🎉"
        )
    
###Now test the mint logic class
if __name__ == "__main__":
    minti_app=MintLogic()

##Add a test data
minti_app.data_manager.record_transaction({
    "Date": "2025-11-06", 
    "Type": "Income",
    "Amount": 2000,
    "Category": "Salary",
    "Is_debt": False
})
minti_app.data_manager.record_transaction({
    "Date": "2025-11-06", 
    "Type": "Income",
    "Amount": 4999,
    "Description": "Monthly Paycheck",
    "Category": "Rent",
    "Is_debt": False
})

minti_app.data_manager.record_transaction({
    "Date": "2025-11-06", 
    "Type": "Expense",
    "Amount": 1000,
    "Category": "Salary",
    "Description":"Monthly contribution",
    "Is_debt": False
})

###Get the monthly summary
