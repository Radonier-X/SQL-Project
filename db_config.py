"""
DB_CONFIGURATION FILE
CBSE Class 12 Computer Science Project

Stores the MySQL connector values used by every other module
(db_connection.py, guest_operations.py, room_operations.py,
reservation_operations.py), and can also SET UP the database
for the very first time by running hotel_db_schema.sql.

HOW TO USE THIS FILE:
  1. Run this file directly:      python db_config.py
     - It will ask if you want to enter your own MySQL host /
       username / password / database name.
     - Whatever you enter is saved to a text file called
       "db_settings.txt" in the same folder, so the next time
       ANY file in this project runs, it automatically picks up
       your saved values (no need to type them again).
     - It then runs hotel_db_schema.sql to create the database
       and tables.
  2. After that, just run main.py as usual (python main.py).
     Running main.py does NOT run the setup again -- setup only
     happens when db_config.py itself is run directly.
"""

import mysql.connector
import os

# Name of the text file where connection details are stored.
# This file is created automatically the first time someone
# saves their settings -- it is NOT part of the project when
# you first download/copy it.
SETTINGS_FILE = "db_settings.txt"

# ---- default values, used only if db_settings.txt does not exist yet ----
# Values used when testing
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "sandship@119002"
DB_DATABASE = "hotel_db"


def load_settings():
    """
    Reads db_settings.txt (if it exists) and overwrites the
    DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE values above with
    whatever was saved earlier. Because every other module does
    "from db_config import DB_HOST, DB_USER, ..." they automatically
    receive the saved values too, without any change needed on
    their part.
    """
    global DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE

    if os.path.exists(SETTINGS_FILE):
        file = open(SETTINGS_FILE, "r")
        lines = file.readlines()
        file.close()

        settings = {}
        for line in lines:
            line = line.strip()
            if line == "":
                continue
            key, value = line.split("=", 1)
            settings[key] = value

        if "DB_HOST" in settings:
            DB_HOST = settings["DB_HOST"]
        if "DB_USER" in settings:
            DB_USER = settings["DB_USER"]
        if "DB_PASSWORD" in settings:
            DB_PASSWORD = settings["DB_PASSWORD"]
        if "DB_DATABASE" in settings:
            DB_DATABASE = settings["DB_DATABASE"]


def save_settings():
    """
    Writes the current DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE
    values to db_settings.txt so they are remembered the next time
    the program is run -- even by a different person using this
    same folder on their own computer.
    """
    file = open(SETTINGS_FILE, "w")
    file.write("DB_HOST=" + DB_HOST + "\n")
    file.write("DB_USER=" + DB_USER + "\n")
    file.write("DB_PASSWORD=" + DB_PASSWORD + "\n")
    file.write("DB_DATABASE=" + DB_DATABASE + "\n")
    file.close()


def ask_and_save_settings():
    """
    Asks the user for their own MySQL host, username, password and
    database name, and saves them using save_settings(). Pressing
    Enter without typing anything keeps the current value (shown
    in square brackets).
    """
    global DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE

    print("\nEnter your MySQL connection details.")
    print("(Press Enter to keep the current value shown in brackets.)\n")

    new_host = input("MySQL host : ")
    new_user = input("MySQL username : ")
    new_password = input("MySQL password : ")
    new_database = input("Database name : ")

    if new_host != "":
        DB_HOST = new_host
    if new_user != "":
        DB_USER = new_user
    if new_password != "":
        DB_PASSWORD = new_password
    if new_database != "":
        DB_DATABASE = new_database

    save_settings()
    print("Connection details saved to", SETTINGS_FILE)


def setup_database():
    """
    Runs hotel_db_schema.sql to create the database and tables,
    using the DB_HOST / DB_USER / DB_PASSWORD values above.

    Note: this connects WITHOUT selecting a database first, because
    the database may not exist yet on a fresh MySQL install -- the
    schema file itself contains "CREATE DATABASE IF NOT EXISTS
    hotel_db" and "USE hotel_db", which create and select it.
    """
    if not os.path.exists("hotel_db_schema.sql"):
        print("Error: hotel_db_schema.sql not found in this folder.")
        print("Make sure db_config.py and hotel_db_schema.sql are in the same folder.")
        return

    # read the whole schema file as one block of text
    file = open("hotel_db_schema.sql", "r")
    sql_text = file.read()
    file.close()

    # remove /* ... */ comment blocks (this also removes the
    # commented-out sample INSERT statements at the end of the
    # file, so they are not run automatically)
    while "/*" in sql_text and "*/" in sql_text:
        start = sql_text.find("/*")
        end = sql_text.find("*/", start) + 2
        sql_text = sql_text[:start] + sql_text[end:]

    # split the remaining text into individual statements using
    # ";" as the separator, since each SQL statement ends with one
    statements = sql_text.split(";")

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    print("\nSetting up the database, please wait...")
    for statement in statements:
        statement = statement.strip()
        if statement != "":
            try:
                cursor.execute(statement)
            except mysql.connector.Error as e:
                print("Error running statement:", e)

    conn.commit()
    cursor.close()
    conn.close()
    print("Database setup complete! You can now run main.py")


def wipe_database():
    """
    DANGER -- deletes every row from all three tables (guests, rooms,
    reservations), but keeps the tables themselves, so the program
    can be used again immediately afterwards without needing to run
    setup_database() again. Useful for resetting the sample data
    before a fresh demo/viva run.
 
    Rows must be deleted in this order: reservations FIRST, then
    rooms and guests. This is because reservations has foreign keys
    pointing to both guests and rooms, so its rows have to be removed
    before the rows they point to can be removed.
 
    Asks for confirmation TWICE, since this action cannot be undone.
    """
    confirm1 = input("\nThis will PERMANENTLY DELETE all guests, rooms and "
                      "reservations. Continue? (Y/N): ")
    if confirm1.upper() != "Y":
        print("Wipe cancelled.")
        return
 
    confirm2 = input("Are you REALLY sure? Type WIPE in capital letters to confirm: ")
    if confirm2 != "WIPE":
        print("Wipe cancelled.")
        return
 
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    cursor = conn.cursor()
 
    try:
        cursor.execute("DELETE FROM reservations")
        cursor.execute("DELETE FROM rooms")
        cursor.execute("DELETE FROM guests")
 
        # reset the AUTO_INCREMENT counters so the next guest/reservation
        # added after the wipe starts again from ID 1
        cursor.execute("ALTER TABLE guests AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE reservations AUTO_INCREMENT = 1")
 
        conn.commit()
        print("\nDatabase wiped. All tables are now empty.")
    except mysql.connector.Error as e:
        print("Error while wiping database:", e)
 
    cursor.close()
    conn.close()


# Load any previously saved settings as soon as this module is
# imported by ANY file (db_connection.py, main.py, etc.), so the
# saved values are always used instead of the hardcoded defaults.
load_settings()


def admin_menu():
    """
    Small menu that ties together the three "whole database" admin
    functions in this file:
      1. Enter/change MySQL connection details (ask_and_save_settings)
      2. Set up the database from hotel_db_schema.sql (setup_database)
      3. Wipe all data from the database (wipe_database)
 
    This menu is deliberately kept OUT of main.py. main.py is meant
    for day-to-day hotel staff use (booking guests, checking rooms,
    etc.), and should not have powerful, database-wide actions like
    "delete everything" sitting in the same menu as normal use. An
    administrator who needs these tools runs db_config.py directly
    instead.
    """
    while True:
        print("\n===== Hotel Reservation System - Database Admin =====")
        print("1. Enter/change MySQL connection details")
        print("2. Set up database (run hotel_db_schema.sql)")
        print("3. Wipe database (DANGER: deletes ALL data)")
        print("0. Exit")
 
        choice = input("Enter your choice: ")
 
        if choice == "1":
            ask_and_save_settings()
        elif choice == "2":
            setup_database()
        elif choice == "3":
            wipe_database()
        elif choice == "0":
            print("Exiting database admin menu.")
            break
        else:
            print("Invalid choice. Please try again.")
 
 
# ------------------------------------------------------------------
# Everything below this line only runs when db_config.py is executed
# DIRECTLY (python db_config.py). When main.py or any other module
# does "from db_config import DB_HOST, ...", Python sets
# __name__ to "db_config" (not "__main__"), so this block is
# skipped -- the admin menu will never appear by accident, and
# main.py never gets access to these powerful functions.
# ------------------------------------------------------------------
if __name__ == "__main__":
    admin_menu()