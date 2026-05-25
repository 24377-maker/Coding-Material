import sqlite3 # loads sqlite3 library

DATABASE = "task7country.db"  #saves database filename

conn = sqlite3.connect(DATABASE) # opens a connection to your database
cursor = conn.cursor() # creates a cursor , a pointe than runs ur sql queries

FIELDS = {
    "1": ("hdi", "HDI"),
    "2": ("gdp", "GDP"),
    "3": ("gdp_per_cap", "GDP per Capita"),
    "4": ("population", "Population"),
}

def show_menu():
    print("\n--- Country Query Tool ---")
    print("Choose a field:")
    for key, (_, label) in FIELDS.items():
        print(f"  {key}. {label}")
    print("  q. Quit")

def get_filter():
    print("Filter:")
    print("  1. Minimum value")
    print("  2. Maximum value")
    print("  3. Top N countries (highest)")
    print("  4. Bottom N countries (lowest)")
    choice = input("Choose filter: ").strip()
    return choice

def run_query(field, filter_choice):
    label = FIELDS[field][1]
    col = FIELDS[field][0]

    if filter_choice == "1":
        val = input(f"Enter minimum {label}: ").strip()
        cursor.execute(
            f"SELECT country, {col} FROM countries WHERE {col} >= ? ORDER BY {col} DESC",
            (val,)
        )
    elif filter_choice == "2":
        val = input(f"Enter maximum {label}: ").strip()
        cursor.execute(
            f"SELECT country, {col} FROM countries WHERE {col} <= ? ORDER BY {col} ASC",
            (val,)
        )
    elif filter_choice == "3":
        n = input("How many top countries? ").strip()
        cursor.execute(
            f"SELECT country, {col} FROM countries ORDER BY {col} DESC LIMIT ?",
            (n,)
        )
    elif filter_choice == "4":
        n = input("How many bottom countries? ").strip()
        cursor.execute(
            f"SELECT country, {col} FROM countries ORDER BY {col} ASC LIMIT ?",
            (n,)
        )
    else:
        print("Invalid filter choice.")
        return

    rows = cursor.fetchall()
    if not rows:
        print("No results found.")
        return

    print(f"\n{'Country':<25} {label}")
    print("-" * 45)
    for country, value in rows:
        print(f"{country:<25} {value:,}")

while True:
    show_menu()
    field_choice = input("Your choice: ").strip()

    if field_choice == "q":
        print("Goodbye!")
        break
    if field_choice not in FIELDS:
        print("Invalid choice, try again.")
        continue

    filter_choice = get_filter()
    run_query(field_choice, filter_choice)

conn.close()
