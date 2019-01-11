import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")
conn.execute('DROP TABLE employee;')
print("Table Dropped")
conn.execute('CREATE TABLE employee (name TEXT, addr TEXT, city TEXT, pin TEXT)')
print("Table created successfully")
conn.close()
