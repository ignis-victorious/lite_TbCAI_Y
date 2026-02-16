#
#  Import LIBRARIES
import sqlite3
import sys
from sqlite3 import Connection

#  Import FILES
#  ______________________
#
# QUERIES - Terminal
# uv run main.py setup
# sqlite3 -header -column shopping.db "SELECT * FROM products;"
# uv run main.py add
# sqlite3 -header -column shopping.db "SELECT * FROM products;"
# uv run main.py update
# sqlite3 -header -column shopping.db "SELECT * FROM products;"
# uv run main.py delete
# sqlite3 -header -column shopping.db "SELECT * FROM products;"


DB_NAME: str = "shopping.db"


def setup() -> None:
    conn: Connection = sqlite3.connect(database=DB_NAME)
    conn.execute("""CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL, 
        price REAL NOT NULL
        ) 
    """)
    conn.executemany(
        "INSERT INTO products (name, price) VALUES (?, ?)",
        [("Laptop", 999.99), ("Coffee Mug", 12.99), ("Python Book", 39.99), ("Keyboard", 79.99)],
    )
    conn.commit()
    conn.close()
    print("Created 4 products.")


def add() -> None:
    conn: Connection = sqlite3.connect(database=DB_NAME)
    conn.execute("INSERT INTO products (name, price) VALUES (?, ?)", ("Headphones", 59.99))
    conn.commit()
    conn.close()
    print("Added Headphones ($59.99) ")


def update() -> None:
    conn: Connection = sqlite3.connect(database=DB_NAME)
    conn.execute("UPDATE products SET price = ? WHERE name = ?", (899.99, "Laptop"))
    conn.commit()
    conn.close()
    print("Updated Laptop to $899.99")


def delete() -> None:
    conn: Connection = sqlite3.connect(database=DB_NAME)
    conn.execute("DELETE FROM products WHERE name = ?", ("Coffee Mug",))
    conn.commit()
    conn.close()
    print("Deleted Coffee Mug")


if __name__ == "__main__":
    actions = {"setup": setup, "add": add, "update": update, "delete": delete}
    action: str = sys.argv[1] if len(sys.argv) > 1 else "setup"
    if action in actions:
        actions[action]()
    else:
        print("Usage: python3 shopping_crud.py [setup |add|update|deletel")


#
#  Import FILES LIBRARIES
#  ______________________
#
