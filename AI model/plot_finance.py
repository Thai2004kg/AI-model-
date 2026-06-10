import sqlite3
import matplotlib.pyplot as plt

DB_PATH = r"C:\AI model\database.db"

def get_financial_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE type = 'income'
    """)
    total_income = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE type = 'expense'
    """)
    total_expense = cursor.fetchone()[0]

    cursor.execute("""
        SELECT category, COALESCE(SUM(amount), 0) AS total
        FROM transactions
        WHERE type = 'expense'
        GROUP BY category
        ORDER BY total DESC
    """)
    category_stats = cursor.fetchall()

    conn.close()
    return total_income, total_expense, category_stats

def plot_pie_chart(category_stats):
    if not category_stats:
        print("Không có dữ liệu chi tiêu để vẽ biểu đồ tròn.")
        return

    labels = [row[0] for row in category_stats]
    values = [row[1] for row in category_stats]

    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title("Tỷ lệ chi tiêu theo danh mục")
    plt.axis("equal")
    plt.show()

def plot_income_expense_bar(total_income, total_expense):
    labels = ["Thu nhập", "Chi tiêu"]
    values = [total_income, total_expense]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.title("So sánh tổng thu nhập và tổng chi tiêu")
    plt.ylabel("Số tiền (VND)")
    plt.show()

def plot_category_bar(category_stats):
    if not category_stats:
        print("Không có dữ liệu chi tiêu để vẽ biểu đồ danh mục.")
        return

    labels = [row[0] for row in category_stats]
    values = [row[1] for row in category_stats]

    plt.figure(figsize=(10, 6))
    plt.barh(labels, values)
    plt.title("Chi tiêu theo từng danh mục")
    plt.xlabel("Số tiền (VND)")
    plt.gca().invert_yaxis()
    plt.show()