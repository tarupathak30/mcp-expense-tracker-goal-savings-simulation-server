import math
from crud import get_goal, get_current_salary, get_latest_month_expense
from analytics import get_average_monthly_expense

def simulate_goal(goal_id, annual_interest_rate):
    goal = get_goal(goal_id)

    if not goal:
        return {"error": "Goal not found"}

    monthly_salary = get_current_salary()
    monthly_expenses = max(
        get_latest_month_expense(),
        get_average_monthly_expense()
    )

    if monthly_salary is None:
        return {"error": "No salary set"}

    monthly_savings = monthly_salary - monthly_expenses

    if monthly_savings <= 0:
        return {"error": "No positive monthly savings available"}

    target_amount = goal["target_amount"]
    monthly_rate = annual_interest_rate / 12

    numerator = math.log(1 + (target_amount * monthly_rate) / monthly_savings)
    denominator = math.log(1 + monthly_rate)

    months_required = math.ceil(numerator / denominator)

    total_invested = monthly_savings * months_required
    final_amount = monthly_savings * ((1 + monthly_rate) ** months_required - 1) / monthly_rate
    interest_earned = final_amount - total_invested

    return {
        "goal_name": goal["goal_name"],
        "target_amount": target_amount,
        "monthly_salary": monthly_salary,
        "monthly_expenses": monthly_expenses,
        "monthly_savings": monthly_savings,
        "months_required": months_required,
        "years_required": round(months_required / 12, 2),
        "total_invested": round(total_invested, 2),
        "interest_earned": round(interest_earned, 2),
        "final_amount": round(final_amount, 2)
    }