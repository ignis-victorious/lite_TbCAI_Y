#
#  Import LIBRARIES
import sqlite3
from sqlite3 import Connection, Cursor

#  Import FILES
#  ______________________
#


# Connect to database
print("=== Connect to Database ===")
conn: Connection = sqlite3.connect(database="contacts.db")
cursor: Cursor = conn.cursor()
print("Connected to contacts. db")

# Create table
print("\n=== Create Table ===")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL, 
    email TEXT NOT NULL, 
    phone TEXT
    """)
conn.commit()
print("Created contacts table")

# Insert single record
print("\n=== Insert Single Record ===")
cursor.execute(
    "INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)", ("Alice Smith", "alice@acme.com", "#555-0101")
)
conn.commit()
print(f"Inserted Alice, row id: {cursor.lastrowid}")

# Bulk insert
print("\n=== Bulk Insert ===")
contacts: list[tuple[str, str, str] | tuple[str, str, None]] = [
    ("Bob Jones", "bob@globex.com", "555-0102"),
    ("Charlie Brown", "charlie@initech.com", "555-0103"),
    ("Diana Prince", "diana@hooli.com", None),
]
cursor.executemany("INSERT INTO contacts (name, email, phone) VALUES (?,?,?)", contacts)
conn.commit()
print(f"Inserted {cursor.rowcount} contacts")

# Fetch all records
print("\n=== Fetch All Records ===")
cursor.execute("SELECT * FROM contacts")
rows: list[tuple[str, str, str] | tuple[str, str, None]] = cursor.fetchall()
for row in rows:
    print(f" {row[0]}: {row[1]} | {row[2]} | ")
    # print(f" {row[0]}: {row[1]} | {row[2]} | {row[3]}")

# Fetch one record
print("\n=== Fetch One Record ===")
cursor.execute("SELECT * FROM contacts WHERE name = ?", ("Alice Smith",))
result = cursor.fetchone()
print(f" Found: {result[1]} ({result[2]})")

# Close connection
conn.close()
print("\nDatabase closed.")

#
#  Import FILES LIBRARIES
#  ______________________
#


# def main():
#     print("Hello from lite-tbcai-y!")


# if __name__ == "__main__":
#     main()
