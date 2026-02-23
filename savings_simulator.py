from analytics import get_monthly_totals
from crud import get_goal, get_current_salary, get_latest_month_expense

def simulate_savings_growth(
    months=12,
    annual_interest_rate=0.05,
    expense_growth_rate=0.0
):
    monthly_income = get_current_salary()

    if not monthly_income:
        return {"error": "No salary set. Please update salary first."}

    data = get_monthly_totals()
    
    if not data:
        return {"error": "No expense data available"}
    
    # baseline expense (average of last 3 months)
    totals = [row[1] for row in data]
    
    baseline_expense = (
        sum(totals[-3:]) / min(len(totals), 3)
    )
    
    monthly_interest = annual_interest_rate / 12
    
    results = []
    savings_balance = 0
    current_expense = baseline_expense
    
    for month in range(1, months + 1):
        monthly_savings = max(0, monthly_income - current_expense)
        
        savings_balance = (
            savings_balance * (1 + monthly_interest)
            + monthly_savings
        )
        
        results.append({
            "month": month,
            "income": monthly_income,
            "expense": round(current_expense, 2),
            "monthly_savings": round(monthly_savings, 2),
            "total_savings": round(savings_balance, 2), 
            "savings_rate": round((monthly_income - baseline_expense) / monthly_income * 100, 2)
        })
        
        current_expense *= (1 + expense_growth_rate)
    
    return {
        "monthly_income": monthly_income,
        "baseline_expense": round(baseline_expense, 2),
        "projection": results,
        "final_savings": round(savings_balance, 2)
    }