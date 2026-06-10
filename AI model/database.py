# database.py

import sqlite3
import time
from config import DB_NAME


REQUIRED_COLUMNS = {
    "id",
    "trans_date",
    "trans_type",
    "amount",
    "description",
    "category",
    "created_at"
}


def get_connection():
    return sqlite3.connect(DB_NAME)


def table_exists(cursor, table_name):
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name=?
    """, (table_name,))
    return cursor.fetchone() is not None


def get_table_columns(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    rows = cursor.fetchall()
    return {row[1] for row in rows}


def create_transactions_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trans_date TEXT NOT NULL,
            trans_type TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT NOT NULL,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    if table_exists(cursor, "transactions"):
        columns = get_table_columns(cursor, "transactions")

        if not REQUIRED_COLUMNS.issubset(columns):
            backup_name = f"transactions_old_{int(time.time())}"

            cursor.execute(f"""
                ALTER TABLE transactions
                RENAME TO {backup_name}
            """)

            create_transactions_table(cursor)

    else:
        create_transactions_table(cursor)

    conn.commit()
    conn.close()


def add_transaction(trans_date, trans_type, amount, description, category):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (trans_date, trans_type, amount, description, category)
        VALUES (?, ?, ?, ?, ?)
    """, (
        trans_date,
        trans_type,
        amount,
        description,
        category
    ))

    conn.commit()
    conn.close()


def get_all_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, trans_date, trans_type, amount, description, category
        FROM transactions
        ORDER BY trans_date DESC, id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_finance_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN trans_type = 'Thu' THEN amount ELSE 0 END), 0),
            COALESCE(SUM(CASE WHEN trans_type = 'Chi' THEN amount ELSE 0 END), 0)
        FROM transactions
    """)

    total_income, total_expense = cursor.fetchone()

    cursor.execute("""
        SELECT
            COALESCE(category, 'Chưa phân loại') AS category_name,
            COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE trans_type = 'Chi'
        GROUP BY category_name
        ORDER BY SUM(amount) DESC
    """)

    expense_by_category = cursor.fetchall()

    conn.close()

    balance = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "expense_by_category": expense_by_category
    }


def get_finance_summary_text():
    summary = get_finance_summary()

    lines = []
    lines.append(f"Tổng thu: {summary['total_income']:,.0f} VND")
    lines.append(f"Tổng chi: {summary['total_expense']:,.0f} VND")
    lines.append(f"Số dư: {summary['balance']:,.0f} VND")
    lines.append("Chi theo danh mục:")

    if summary["expense_by_category"]:
        for category, amount in summary["expense_by_category"]:
            lines.append(f"- {category}: {amount:,.0f} VND")
    else:
        lines.append("- Chưa có dữ liệu chi tiêu")

    return "\n".join(lines)


def get_monthly_summary(month: int, year: int):
    conn = get_connection()
    cursor = conn.cursor()

    month_str = f"{month:02d}"
    year_str = str(year)

    cursor.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN trans_type = 'Thu' THEN amount ELSE 0 END), 0),
            COALESCE(SUM(CASE WHEN trans_type = 'Chi' THEN amount ELSE 0 END), 0)
        FROM transactions
        WHERE substr(trans_date, 1, 4) = ?
          AND substr(trans_date, 6, 2) = ?
    """, (year_str, month_str))

    total_income, total_expense = cursor.fetchone()

    conn.close()

    return {
        "month": month,
        "year": year,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    }


def get_database_debug_info():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    debug_info = {
        "database": DB_NAME,
        "tables": tables,
        "transactions_columns": []
    }

    if table_exists(cursor, "transactions"):
        cursor.execute("PRAGMA table_info(transactions)")
        debug_info["transactions_columns"] = cursor.fetchall()

    conn.close()

    return debug_info
def get_monthly_summary(month: int, year: int):
    conn = get_connection()
    cursor = conn.cursor()

    month_str = f"{month:02d}"
    year_str = str(year)

    cursor.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN trans_type = 'Thu' THEN amount ELSE 0 END), 0),
            COALESCE(SUM(CASE WHEN trans_type = 'Chi' THEN amount ELSE 0 END), 0)
        FROM transactions
        WHERE substr(trans_date, 1, 4) = ?
          AND substr(trans_date, 6, 2) = ?
    """, (year_str, month_str))

    total_income, total_expense = cursor.fetchone()

    conn.close()

    return {
        "month": month,
        "year": year,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    }