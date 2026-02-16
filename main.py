#
#  Import LIBRARIES
import sqlite3
from sqlite3 import Cursor

#  Import FILES
#  ______________________
#


# Context manager handles commit and close
with sqlite3.connect("products.db") as conn:
    # Dict-like row access
    conn.row_factory = sqlite3.Row
    cursor: Cursor = conn.cursor()

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL, 
            category TEXT NOT NULL, 
            price REAL NOT NULL, 
            in_stock INTEGER DEFAULT 1
            )
    """)

    # Clear and seed data
    cursor.execute("DELETE FROM products")
    products: list[tuple[str, str, float, int]] = [
        ("Laptop", "Electronics", 999.99, 1),
        ("Headphones", "Electronics", 79.99, 1),
        ("'USB Cable", "Electronics", 12.99, 11),
        ("Python Crash Course", "Books", 35.99, 9),
        ("Clean Code", "Books", 42.50, 0),
        ("Winter Jacket", "Clothing", 89.99, 1),
        ("Running Shoes", "Clothing", 64.99, 8),
    ]
    cursor.executemany("INSERT INTO products (name, category, price, in_stock) VALUES (?, ?, ?,?)", products)
    conn.commit()
    print("=== Seeded 7 Products ===")

    # WHERE clause
    print("\n=== Products Over $50 ===")
    cursor.execute("SELECT name, price FROM products WHERE price > ?", (50,))
    for row in cursor.fetchall():
        print(f" {row['name']}: ${row['price']:.2f}")

    # ORDER BY with LIMIT
    print("\n=== Top 3 Most Expensive ==")
    cursor.execute("SELECT name, price FROM products ORDER BY price DESC LIMIT 3")
    for row in cursor.fetchall():
        print(f" {row['name']}: ${row['price']:.2f}")

    # UPDATE
    print("\n=== Update Price ===")
    cursor.execute("UPDATE products SET price = ? WHERE name = ?", (69.99, "Headphones"))
    conn.commit()
    print(f"Updated {cursor.rowcount} row(s)")
    cursor.execute("SELECT name, price FROM products WHERE name = ?", ("Headphones",))
    row = cursor.fetchone()
    print(f" {row['name']} new price: ${row['price']:.2f}")

    # DELETE
    print("\n=== Delete Out-of-Stock ===")
    cursor.execute("DELETE FROM products WHERE in_stock = 0")
    conn.commit()
    print(f" Deleted {cursor.rowcount} row(s) ")

    # Aggregate functions
    print("\n=== Aggregate Stats ===")
    cursor.execute(
        "SELECT COUNT (*) as total, AVG(price) as avg_price, MIN (price) as cheapest, MAX (price) as priciest FROM products"
    )
    stats: dict[str, int | float] = cursor.fetchone()  # This tuple[int, float, float, float] is not valid as this is
    print(f" Total: {stats['total']} products")
    print(f"Average: ${stats['avg_price']: 2f}")
    print(f"Cheapest: ${stats['cheapest']:.2f}")
    print(f" Most expensive: ${stats['priciest']:.2f}")

    # GROUP BY
    print("\n=== Products by Category ===")
    cursor.execute("SELECT category, COUNT (*) as count, AVG(price) as avg_price FROM products GROUP BY category")
    for row in cursor.fetchall():
        print(f"  {row['category']}: {row['count']} items, avg ${row['avg_price']:.2f}")
        print("\nDone. ")

    # Close connection
    # conn.close()
    # print("\nDatabase closed.")

#
#  Import FILES LIBRARIES
#  ______________________
#


# def main():
#     print("Hello from lite-tbcai-y!")


# if __name__ == "__main__":
#     main()
