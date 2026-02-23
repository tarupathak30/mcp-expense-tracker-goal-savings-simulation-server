from fastmcp import FastMCP
import mcp
from database import init_db
from crud import (
    add_expense,
    list_expenses,
    edit_expense,
    delete_expense,
    add_credit, 
    update_salary, 
    create_goal
)
import os
from insights import generate_financial_report
from savings_simulator import simulate_savings_growth
from goals_simulation import simulate_goal 

# Initialize DB
init_db()

mcp = FastMCP("ExpenseTracker")

CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")


# TOOL WRAPPERS


@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    # Read fresh each time so you can edit the file without restarting
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()



@mcp.tool()
def add_expense_tool(date: str, amount: float, category: str, subcategory: str, note: str = ""):
    return add_expense(date, amount, category, subcategory, note)


@mcp.tool()
def list_expenses_tool(start_date: str, end_date: str):
    return list_expenses(start_date, end_date)


@mcp.tool()
def edit_expense_tool(id: int, date=None, amount=None, category=None, subcategory=None, note=None):
    return edit_expense(id, date, amount, category, subcategory, note)


@mcp.tool()
def delete_expense_tool(id: int):
    return delete_expense(id)


@mcp.tool()
def add_credit_tool(date: str, amount: float, category: str = "Credit", subcategory: str = "", note: str = ""):
    return add_credit(date, amount, category, subcategory, note)

@mcp.tool()
def financial_insights_tool():
    return generate_financial_report()

@mcp.tool()
def set_salary(amount: float):
    update_salary(amount)
    return {"message": f"Salary updated to ₹{amount}"}

@mcp.tool()
def simulate_savings_tool(
    months: int = 12,
    annual_interest_rate: float = 0.05,
    expense_growth_rate: float = 0.0
):
    return simulate_savings_growth(
        months,
        annual_interest_rate,
        expense_growth_rate
    )
    
@mcp.tool()
def api_create_goal(goal_name: str, target_amount: float):
    return create_goal(goal_name, target_amount)


@mcp.tool()
def api_simulate_goal(goal_id: int, annual_interest_rate: float):
    return simulate_goal(goal_id, annual_interest_rate)

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    mcp.run()