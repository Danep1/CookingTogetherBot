import sqlite3 as sql

conn = sql.connect("db/CookingBook.sqlite")
cursor = conn.cursor()
cursor.execute("select cooking from Book where id_1='1'")

for row in cursor.fetchall():
    print(row)
