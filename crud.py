from database import get_connection

# -----------------------------
# ADD EXPENSE
# -----------------------------
def add_expense(date, amount, category, subcategory, note=""):
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        return {"status": "ok", "id": cur.lastrowid}


# -----------------------------
# LIST EXPENSES
# -----------------------------
def list_expenses(start_date, end_date):
    with get_connection() as conn:
        cur = conn.execute("""
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
        """, (start_date, end_date))

        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


# -----------------------------
# EDIT EXPENSE
# -----------------------------
def edit_expense(id, date=None, amount=None, category=None, subcategory=None, note=None):
    with get_connection() as conn:
        curr = conn.execute("SELECT * FROM expenses WHERE id = ?", (id,))
        row = curr.fetchone()

        if not row:
            return {"status": "error", "message": "Expense entry not found."}

        fields = []
        values = []

        if date is not None:
            fields.append("date = ?")
            values.append(date)
        if amount is not None:
            fields.append("amount = ?")
            values.append(amount)
        if category is not None:
            fields.append("category = ?")
            values.append(category)
        if subcategory is not None:
            fields.append("subcategory = ?")
            values.append(subcategory)
        if note is not None:
            fields.append("note = ?")
            values.append(note)

        if not fields:
            return {"status": "error", "message": "No fields to update."}

        query = f"UPDATE expenses SET {', '.join(fields)} WHERE id = ?"
        values.append(id)

        conn.execute(query, values)

        return {"status": "ok", "message": f"Expense entry with ID {id} updated successfully."}


# -----------------------------
# DELETE EXPENSE
# -----------------------------
def delete_expense(id):
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM expenses WHERE id = ?", (id,))

        if cur.rowcount == 0:
            return {"status": "error", "message": f"Expense entry with ID {id} not found."}

        return {"status": "ok", "message": f"Expense entry with ID {id} deleted successfully."}


# -----------------------------
# ADD CREDIT
# -----------------------------
def add_credit(date, amount, category="Credit", subcategory="", note=""):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO expenses (date, amount, category, subcategory, note)
            VALUES (?, ?, ?, ?, ?)
        """, (date, -abs(amount), category, subcategory, note))

        return {"status": "ok", "message": "Credit entry added successfully."}
    
    
def update_salary(new_salary):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO income_profile (monthly_salary) VALUES (?)",
            (new_salary,)
        )
def get_current_salary():
    with get_connection() as conn:
        cur = conn.execute("""
            SELECT monthly_salary
            FROM income_profile
            ORDER BY updated_at DESC
            LIMIT 1
        """)
        row = cur.fetchone()
        return row[0] if row else None     
        
def get_latest_month_expense():
    with get_connection() as conn:
        cur = conn.execute("""
            SELECT SUM(amount)
            FROM expenses
            WHERE amount > 0
            AND strftime('%Y-%m', date) = (
                SELECT strftime('%Y-%m', MAX(date))
                FROM expenses
            )
        """)
        row = cur.fetchone()
        return row[0] if row[0] else 0
    
    
def create_goal(goal_name, target_amount):
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO goals (goal_name, target_amount)
            VALUES (?, ?)
        """, (goal_name, target_amount))

        conn.commit()
        return {"goal_id": cursor.lastrowid, "goal_name": goal_name}
    
    
def get_goal(goal_id):
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT id, goal_name, target_amount
            FROM goals
            WHERE id = ?
        """, (goal_id,))
        row = cursor.fetchone()

        if not row:
            return None

        return {
            "id": row[0],
            "goal_name": row[1],
            "target_amount": row[2]
        }