"""
DB_CONNECTION MODULE
CBSE Class 12 Computer Science Project

This module holds things that are shared by every other module:
  - get_connection() : opens a connection to the MySQL database
  - get_valid_int()   : safely reads a whole number from the user
  - check_database_ready() : FAILSAFE - confirms the database and all
                              required tables exist before the menu
                              in main.py is shown
  - offer_setup()          : helper used by check_database_ready() to
                              run the one-time setup from db_config.py
                              if something is missing
"""

import mysql.connector
from db_config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE
from db_config import setup_database

def get_connection():
    """
    Creates and returns a connection object to the MySQL database.
    Change the host/user/password values in db_config to match your own MySQL setup.
    """
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,   
        database=DB_DATABASE
    )
    return conn


def get_valid_int(prompt):
    """
    Keeps asking the user for input until a valid whole number
    is entered. This prevents the program from crashing if the
    user types letters or leaves the field blank by mistake.
    """
    while True:
        value = input(prompt)
        try:
            return int(value)
        except ValueError:
            print("Invalid input. Please enter numbers only.")


def check_database_ready():
    """
    FAILSAFE: called once by main.py, right when the program starts,
    BEFORE the menu is shown.
 
    Without this check, if the database or a table was missing, the
    program would only find out in the middle of some menu option
    (e.g. after the user has already typed in guest details), which
    is confusing and wastes their time. This checks everything up
    front instead, so the problem is caught immediately with a clear
    message.
 
    It does two things:
      1. Tries to connect to MySQL using get_connection(). If this
         fails, the database itself (or the MySQL server) is not
         reachable.
      2. If the connection works, tries a harmless SELECT on each of
         the three required tables (guests, rooms, reservations) to
         make sure they actually exist.
 
    If either check fails, the user is offered a chance to run the
    setup from db_config.py immediately, without leaving the program.
 
    Returns True if the program is safe to continue, False otherwise.
    """
    try:
        conn = get_connection()
    except mysql.connector.Error as e:
        print("\nCould not connect to the database 'hotel_db'.")
        print("(Technical detail:", e, ")")
        return offer_setup()
 
    # connection worked, now check that every required table exists
    cursor = conn.cursor()
    tables_ok = True
    for table_name in ("guests", "rooms", "reservations"):
        try:
            cursor.execute("SELECT 1 FROM " + table_name + " LIMIT 1")
            cursor.fetchall()
        except mysql.connector.Error:
            tables_ok = False
            break
 
    cursor.close()
    conn.close()
 
    if not tables_ok:
        print("\nThe database exists, but one or more required tables")
        print("(guests, rooms, reservations) are missing.")
        return offer_setup()
 
    # everything checked out fine
    return True
 
 
def offer_setup():
    """
    Called by check_database_ready() only when something was found
    to be missing (database or a table). Offers to run
    db_config.setup_database() immediately, then checks once more
    to confirm the fix worked, instead of forcing the user to quit
    and separately run "python db_config.py".
    """
    choice = input("Do you want to set up the database now? (Y/N): ")
    if choice.upper() != "Y":
        print("Cannot continue without the database. Exiting program.")
        return False
 
    setup_database()
 
    # after setup, try connecting and checking the tables one more
    # time to confirm the database is genuinely ready now
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM guests LIMIT 1")
        cursor.fetchall()
        cursor.close()
        conn.close()
        print("Database is ready.")
        return True
    except mysql.connector.Error as e:
        print("\nSetup did not fully succeed. Please check your MySQL")
        print("server and connection details, then try again.")
        print("(Technical detail:", e, ")")
        return False