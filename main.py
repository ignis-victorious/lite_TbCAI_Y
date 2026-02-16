#
#  Import LIBRARIES
import sqlite3
from sqlite3 import Connection, Cursor

#  Import FILES
#  ______________________
#


DB_NAME: str = "employees. db"


def get_connection() -> Connection:
    conn: Connection = sqlite3.connect(database=DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_table() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS employees(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL, 
                department TEXT NOT NULL,
                salary REAL NOT NULL, 
                active INTEGER DEFAULT 1
                )
        """)
        conn.commit()
    print("Table ready.")


def add_employee(name, department, salary) -> int | None:
    with get_connection() as conn:
        cursor: Cursor = conn.execute(
            "INSERT INTO employees (name, department, salary) VALUES (?, ?,?)", (name, department, salary)
        )
        conn.commit()
        return cursor.lastrowid


def list_employees() -> list[float | int | str]:
    with get_connection() as conn:
        rows: list[int | str | float] = conn.execute(
            "SELECT * FROM employees WHERE active = 1 ORDER BY name"
        ).fetchall()
        return rows


def update_salary(name, new_salary) -> int:
    with get_connection() as conn:
        cursor: Cursor = conn.execute(
            "UPDATE employees SET salary = ? WHERE name = ? AND active = 1", (new_salary, name)
        )
        conn.commit()
        return cursor.rowcount


def delete_employee(name) -> int:
    with get_connection() as conn:
        cursor: Cursor = conn.execute("UPDATE employees SET active = 0 WHERE name = ? AND active = 1", (name,))
        conn.commit()
        return cursor.rowcount


def search_by_department(department) -> list[float | str]:
    with get_connection() as conn:
        rows: list[str | float] = conn.execute(
            "SELECT name, salary FROM employees WHERE department = ? AND active = 1 ORDER BY salary DESC", (department,)
        ).fetchall()
        return rows


def get_department_stats() -> list[float | str]:
    with get_connection() as conn:
        rows: list[str | float] = conn.execute("""
            SELECT department, COUNT (*) as count,
            AVG (salary) as avg_salary, 
            MIN (salary) as min_salary, 
            MAX (salary) as max_salary
            FROM empLoyees WHERE active = 1
            GROUP BY department ORDER BY avg_salary DESC
        """).fetchall()
        return rows


if __name__ == "__main__":
    import os

    if os.path.exists(path=DB_NAME):
        os.remove(path=DB_NAME)

    create_table()

    # Seed empLoyees
    print("\n=== Adding Employees ===")
    employees: list[tuple[str, str, int]] = [
        ("Tony Stark", "Engineering", 250000),
        ("Pepper Potts", "Management", 180000),
        ("Happy Hogan", "Security", 95000),
        ("James Rhodes", "Engineering", 160000),
        ("Peter Parker", "Engineering", 85000),
        ("Natasha Romanoff", "Security", 145000),
    ]
    for name, dept, salary in employees:
        emp_id: int | None = add_employee(name=name, department=dept, salary=salary)
        print(f" Added {name} (id: {emp_id})")

    # List all
    print("\n=== All Employees ===")
    for emp in list_employees():
        print(f"l{emp['name']:20s} | {emp['department']:12s} | ${emp['salary']:>10,.2f}")

    # Update salary
    print("\n=== Salary Update ===")
    updated: int = update_salary(name="Peter Parker", new_salary=110000)
    print(f" Updated {updated} row(s): Peter Parker - $110, 000")

    # Search by department
    print("\n=== Engineering Team ===")
    for emp in search_by_department("Engineering"):
        print(f" {emp['name']:20s} | ${emp['salary']:>10,.2f}")

    # Delete employee
    print("\n=== Remove Employee ===")
    removed = delete_employee("Happy Hogan")
    print(f" Removed {removed} row(s): Happy Hogan")

    # Department stats
    print("\n=== Department Stats ===")
    for dept in get_department_stats():
        print(
            f"    {dept['department']:12s} |    {dept['count']} employees | avg ${dept['avg_salary']:>10,.2f} | range ${dept['min_salary']:>10,.2f} - ${dept['max_salary']:>10,.2f}"
        )

    # Final count
    print(f"\n=== Active Employees: {len(list_employees())} ===")


#
#  Import FILES LIBRARIES
#  ______________________
#
