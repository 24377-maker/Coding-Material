import sqlite3  # lets Python talk to a database

conn = sqlite3.connect("task7country.db")  # opens the database file
cursor = conn.cursor()  # lets us run SQL commands


def show_menu():
    # prints the main menu for the user to see
    print("\n--- Country Query Tool ---")
    print("1. HDI")
    print("2. GDP")
    print("3. GDP per Capita")
    print("4. Population")
    print("q. Quit")


def get_field_info(choice):
    # returns the column name and label based on what the user picked
    if choice == "1":
        return "hdi", "HDI"
    elif choice == "2":
        return "gdp", "GDP"
    elif choice == "3":
        return "gdp_per_cap", "GDP per Capita"
    elif choice == "4":
        return "population", "Population"


def get_filter():
    # asks the user how they want to filter the results
    print("\nHow do you want to filter?")
    print("1. Minimum value")
    print("2. Maximum value")
    print("3. Top N countries")
    print("4. Bottom N countries")
    choice = input("Choose: ").strip()  # .strip() removes any extra spaces the user might type
    return choice


def run_query(field_choice, filter_choice):
    # gets the column name and label for the field the user picked
    col, label = get_field_info(field_choice)

    if filter_choice == "1":
        # user wants countries where the value is at least a certain number
        val = input(f"Enter minimum {label}: ").strip()
        cursor.execute(f"SELECT country, {col} FROM countries WHERE {col} >= ? ORDER BY {col} DESC", (val,))

    elif filter_choice == "2":
        # user wants countries where the value is at most a certain number
        val = input(f"Enter maximum {label}: ").strip()
        cursor.execute(f"SELECT country, {col} FROM countries WHERE {col} <= ? ORDER BY {col} ASC", (val,))

    elif filter_choice == "3":
        # user wants the top N countries with the highest values
        n = input("How many top countries? ").strip()
        cursor.execute(f"SELECT country, {col} FROM countries ORDER BY {col} DESC LIMIT ?", (n,))

    elif filter_choice == "4":
        # user wants the bottom N countries with the lowest values
        n = input("How many bottom countries? ").strip()
        cursor.execute(f"SELECT country, {col} FROM countries ORDER BY {col} ASC LIMIT ?", (n,))

    else:
        print("Invalid filter.")
        return  # stop the function early if the input was wrong

    # fetchall() gets all the results from the query as a list
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No results found.")
        return  # stop early if nothing was found

    # print the results in a simple table
    print(f"\nCountry                   {label}")
    print("-" * 45)
    for row in rows:
        country = row[0]   # first item in the row is the country name
        value = row[1]     # second item is the number (hdi, gdp, etc.)
        print(f"{country:<25} {value}")


# --- main program loop ---
# keeps running until the user types q
while True:
    show_menu()
    field_choice = input("Your choice: ").strip()

    if field_choice == "q":
        print("Goodbye!")
        break  # exits the loop and ends the program

    if field_choice not in ["1", "2", "3", "4"]:
        print("Invalid choice, try again.")
        continue  # goes back to the top of the loop

    filter_choice = get_filter()
    run_query(field_choice, filter_choice)

conn.close()  # closes the database when the program ends
