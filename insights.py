from analytics import (
    get_category_rolling_average, 
    get_category_monthly_totals, 
    get_monthly_totals
)
from database import get_connection



    
# spending spike detection 
def detect_spending_spikes(threshold = 0.5): 
    data = get_monthly_totals() 
    
    if len(data) < 2: 
        return {"spike_detected" : False}
    
    months = [row[0] for row in data]
    totals = [row[1] for row in data]
    
    current_month = months[-1]
    current_total = totals[-1]
    
    # determine baseline window (last 3 months before current)
    if len(totals) >= 4: 
        baseline_values = totals[-4 : -1] #last 3 months before current
    else: 
        baseline_values = totals[:-1] #using whatever is available 
    
    if not baseline_values: 
        return {"spike_detected" : False}

    baseline_avg = sum(baseline_values) / len(baseline_values)
    
    change = (current_total - baseline_avg) / baseline_avg 
    
    return {
        "current_month" : current_month, 
        "baseline_avg" : round(baseline_avg, 2), 
        "current_total" : current_total, 
        "percentage_change" : round(change * 100, 2), 
        "spike_detected" : change > threshold
    }
    
    
# category growth detection 

def detect_category_growth(threshold = 0.4): 
    data = get_category_monthly_totals() 
    growth = {}
    
    for month, category, total in data: 
        if category not in growth: 
            growth[category] = []
        growth[category].append((month, total))
    
    growing_categories = []
    for category, values in growth.items():
        values.sort(key=lambda x: x[0])   # ensure chronological order
        if len(values) < 2: 
            continue
        baseline_vals = [v[1] for v in values[:-1]]
        baseline_avg = sum(baseline_vals) / len(baseline_vals)
        curr_total = values[-1][1]
        
        if baseline_avg == 0:
            return {"spike_detected": False}
        
        change = (curr_total - baseline_avg) / baseline_avg if baseline_avg > 0 else 0
        
        if change > threshold: 
            growing_categories.append({
                "category" : category, 
                "growth_percentage" : round(change * 100, 2)
            })
            
        growing_categories.sort(
            key=lambda x: x["growth_percentage"], 
            reverse=True
        )
    return growing_categories


# abnormal transaction detection 

def detect_abnormal_transactions(multiplier = 2): 
    data = get_monthly_totals()
    if not data:
        return []

    current_month = data[-1][0]
    category_average = get_category_rolling_average(current_month)
    
    abnormal = [] 
    
    with get_connection() as conn:
        curr = conn.execute("""
                            SELECT id, date, amount, category
                            FROM expenses
                            WHERE amount > 0
                            AND strftime('%Y-%m', date) = ?
                        """, (current_month,))
        rows = curr.fetchall() 
        
        
        for id_, date, amount, category in rows: 
            avg = category_average.get(category, 0)
            if avg > 0 and amount > avg * multiplier: 
                abnormal.append({
                    "id" : id_, 
                    "date" : date, 
                    "amount" : amount, 
                    "category" : category
                })
    return abnormal


# full financial report 

def generate_financial_report(): 
    spike = detect_spending_spikes()
    growth = detect_category_growth() 
    abnormal = detect_abnormal_transactions() 
    
    return {
        "spending_spike" : spike, 
        "category_growth" : growth, 
        "abnormal_transactions" : abnormal 
    }
    