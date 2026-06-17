import sqlite3

DB_NAME = "database.db"

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

# Sửa dòng ID = 2 đang bị lỗi 0.0015
cur.execute("""
UPDATE transactions
SET amount = 150000
WHERE id = 2
""")

conn.commit()
conn.close()

print("Đã sửa dòng dữ liệu sai ID = 2 thành 150000 VND.")