from database import get_connection


def get_category_rolling_average(current_month):
    with get_connection() as conn:
        curr = conn.execute("""
            SELECT category, AVG(amount)
            FROM expenses
            WHERE amount > 0
            AND strftime('%Y-%m', date) < ?
            GROUP BY category
        """, (current_month,))
        return dict(curr.fetchall())
    
    
# monthly totals(expenses only)
def get_monthly_totals(): 
    with get_connection() as c: 
        curr = c.execute("""
                        SELECT strftime('%Y-%m', date) AS month, 
                        SUM(amount) AS total
                        FROM expenses 
                        WHERE amount > 0
                        GROUP BY month
                        ORDER BY month ASC""")
        return curr.fetchall() 
    

# category monthly totals 
def get_category_monthly_totals(): 
    with get_connection() as c: 
        curr = c.execute("""
                        SELECT strftime('%Y-%m', date) AS month, category, SUM(amount) AS total 
                        FROM expenses 
                        WHERE amount > 0
                        GROUP BY month, category
                        ORDER BY month ASC, category ASC""")
        return curr.fetchall() 
    
# daily totals 
def get_daily_totals(): 
    with get_connection() as c: 
        curr = c.execute(""" 
                        SELECT date, SUM(amount) AS total
                        FROM expenses 
                        WHERE amount > 0 
                        GROUP BY date 
                        ORDER BY date 
                        """)
        return curr.fetchall() 
    
    
# category average transaction amount 
def get_category_average(): 
    with get_connection() as conn: 
        curr = conn.execute("""
                            SELECT category, AVG(amount) AS avg_amount
                            FROM expenses 
                            WHERE amount > 0 
                            GROUP BY category""")
        return dict(curr.fetchall())
    
    
def get_average_monthly_expense():
    with get_connection() as c:
        curr = c.execute("""
            SELECT AVG(month_total)
            FROM (
                SELECT SUM(amount) as month_total
                FROM expenses
                WHERE amount > 0
                GROUP BY strftime('%Y-%m', date)
            )
        """)
        row = curr.fetchone()
        return row[0] if row[0] else 0