import sqlite3
# sqlite3 is a built-in Python tool that lets us save information to a file on the computer.
# At Grok/Level 1 you stored things in lists - but lists disappear when the program closes.
# A database is like a spreadsheet saved in a file, so the data stays there forever.

# This is the name of the file where all our data gets saved
DB_NAME = "task8rocket.db"

# NOTE: The rockets table has a space at the end of its name ("rockets ")
# so every SQL command has to put quotes around it - that is why you see "rockets " everywhere.


# ------------------------------------------------------------------
# HELPER FUNCTIONS
# These two small functions make getting input from the user easier.
# ------------------------------------------------------------------

def get_int(prompt):
    # Asks the user a question and only accepts a whole number as the answer.
    # If the user types "abc" or leaves it blank it just asks again.
    # "prompt" is the question we pass in when we call this function.

    while True:   # keep looping forever until we get a valid answer

        user_answer = input(prompt)        # ask the user the question
        user_answer = user_answer.strip()  # remove any accidental spaces at the start or end

        try:
            # try to turn the answer into a whole number
            # if the user typed letters this line will fail and jump down to "except"
            number = int(user_answer)
            return number   # it worked - send the number back to whoever called this function

        except ValueError:
            # this runs when int() failed, meaning the user didn't type a valid number
            print("That's not a valid number, try again.")


def get_text(prompt):
    # Asks the user a question and only accepts a non-empty answer.
    # If the user just hits Enter without typing anything it asks again.

    while True:   # keep looping forever until we get a real answer

        user_answer = input(prompt)        # ask the user the question
        user_answer = user_answer.strip()  # remove any accidental spaces

        if user_answer != "":    # if they actually typed something (not just hit Enter)
            return user_answer   # send it back to whoever called this function

        print("This field can't be empty, try again.")


# ------------------------------------------------------------------
# VIEW FUNCTIONS
# These functions read data from the database and print it on screen.
# ------------------------------------------------------------------

def view_all_rockets():
    # Reads every rocket from the database and prints them out.

    try:
        # Step 1 - open the database file
        conn = sqlite3.connect(DB_NAME)

        # Step 2 - get a "cursor"
        # A cursor is like a pen that lets us send commands to the database.
        cursor = conn.cursor()

        # Step 3 - run a SQL command
        # SELECT means "get me these columns"
        # FROM "rockets " means "from the rockets table"
        # This asks the database to give us every row in the rockets table.
        cursor.execute('SELECT rocket_id, name, manufacturer, payload_kg, status FROM "rockets "')

        # Step 4 - collect all the results
        # fetchall() returns a list where each item is one rocket row.
        # Each row is a tuple, for example: (1, "Falcon 9", "SpaceX", 22800, "Active")
        rockets = cursor.fetchall()

        # Step 5 - close the database file when we are done with it
        conn.close()

        # If the list is empty there are no rockets saved yet
        if len(rockets) == 0:
            print("No rockets found.")
            return   # stop the function here, nothing left to do

        print("\n--- ALL ROCKETS ---")
        for r in rockets:
            # r is one rocket row (a tuple)
            # r[0] = id,  r[1] = name,  r[2] = manufacturer,  r[3] = payload,  r[4] = status
            print(f"  ID: {r[0]}  |  {r[1]}  |  {r[2]}  |  {r[3]} kg  |  {r[4]}")

    except sqlite3.Error as e:
        # If something goes wrong with the database, print the error instead of crashing
        print(f"Database error: {e}")


def view_all_missions():
    # Reads every mission from the database and prints them out.
    # Also shows the rocket NAME instead of just a number,
    # by linking the missions table to the rockets table (called a JOIN).

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # This SQL command uses a JOIN - it connects two tables together in one query.
        # The missions table stores a rocket_id number, but we want to show the real rocket name.
        # JOIN "rockets " r ON m.rocket_id = r.rocket_id means:
        #   "link each mission to the rocket that has the matching ID"
        # m. means columns from the missions table
        # r. means columns from the rockets table
        cursor.execute("""
            SELECT m.mission_id, m.mission_name, m.destination,
                   m.launch_date, m.outcome, r.name
            FROM missions m
            JOIN "rockets " r ON m.rocket_id = r.rocket_id
        """)

        missions = cursor.fetchall()   # get all the results as a list
        conn.close()

        if len(missions) == 0:
            print("No missions found.")
            return

        print("\n--- ALL MISSIONS ---")
        for m in missions:
            # m[0]=id,  m[1]=mission name,  m[2]=destination,  m[3]=date,  m[4]=outcome,  m[5]=rocket name
            print(f"  ID: {m[0]}  |  {m[1]}  |  Dest: {m[2]}  |  {m[3]}  |  {m[4]}  |  Rocket: {m[5]}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")


# ------------------------------------------------------------------
# SEARCH AND DELETE FUNCTIONS
# ------------------------------------------------------------------

def search_missions():
    # Lets the user search for missions by destination and prints any matches.

    print("\n--- SEARCH BY DESTINATION ---")
    term = get_text("Enter destination to search for: ")

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # LIKE is used in SQL for partial text matching.
        # The % symbols are wildcards that mean "any characters here".
        # So %Mars% means "anything that contains the word Mars anywhere in it".
        # For example: "Near Mars", "Mars Orbit", and "To Mars and Back" would all match.
        cursor.execute("""
            SELECT m.mission_id, m.mission_name, m.destination,
                   m.launch_date, m.outcome, r.name
            FROM missions m
            JOIN "rockets " r ON m.rocket_id = r.rocket_id
            WHERE m.destination LIKE ?
        """, (f"%{term}%",))

        results = cursor.fetchall()
        conn.close()

        if len(results) == 0:
            print(f"No missions found matching '{term}'.")
            return

        print(f"\nResults for '{term}':")
        for m in results:
            print(f"  ID: {m[0]}  |  {m[1]}  |  Dest: {m[2]}  |  {m[3]}  |  {m[4]}  |  Rocket: {m[5]}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")


def search_rockets_by_manufacturer():
    # Lets the user search for rockets by manufacturer and prints any matches.

    print("\n--- SEARCH BY MANUFACTURER ---")
    term = get_text("Enter manufacturer to search for: ")

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # LIKE with % wildcards matches any rocket whose manufacturer contains the search term.
        cursor.execute(
            'SELECT rocket_id, name, manufacturer, payload_kg, status FROM "rockets " WHERE manufacturer LIKE ?',
            (f"%{term}%",)
        )

        results = cursor.fetchall()
        conn.close()

        if len(results) == 0:
            print(f"No rockets found matching manufacturer '{term}'.")
            return

        print(f"\nResults for '{term}':")
        for r in results:
            print(f"  ID: {r[0]}  |  {r[1]}  |  {r[2]}  |  {r[3]} kg  |  {r[4]}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")


# ------------------------------------------------------------------
# MENU AND MAIN
# ------------------------------------------------------------------

def show_menu():
    # Prints the menu options for the user to choose from.
    print("\n===== ROCKET DATABASE =====")
    print("1. View all rockets")
    print("2. View all missions")
    print("3. Search missions by destination")
    print("4. Search rockets by manufacturer")
    print("5. Exit")
    print("===========================")


def main():
    # This is the main function - it shows the menu in a loop and calls the right
    # function depending on what the user picks.
    # The loop keeps going until the user chooses option 5 (Exit).

    print("Welcome to the Rocket Mission Database!")

    while True:   # keep showing the menu over and over until the user exits

        show_menu()

        try:
            user_input = input("Enter your choice (1-5): ")
            choice = int(user_input.strip())   # convert to a number
        except ValueError:
            # the user typed something that isn't a number
            print("Please enter a number between 1 and 5.")
            continue   # go back to the top of the while loop and show the menu again

        # check the number is in the valid range
        if choice < 1 or choice > 5:
            print("Please enter a number between 1 and 5.")
            continue

        # call the matching function based on what the user chose
        if choice == 1:
            view_all_rockets()
        elif choice == 2:
            view_all_missions()
        elif choice == 3:
            search_missions()
        elif choice == 4:
            search_rockets_by_manufacturer()
        elif choice == 5:
            print("Goodbye!")
            break   # break exits the while True loop so the program ends


# This line means: only run main() if someone runs THIS file directly.
# If another file imports this file, main() won't start automatically.
# At Level 1 you can just treat this as the "start button" for the program.
if __name__ == "__main__":
    main()
