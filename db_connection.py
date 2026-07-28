"""
DB_CONNECTION MODULE
CBSE Class 12 Computer Science Project

This module holds things that are shared by every other module:
  - get_connection() : opens a connection to the MySQL database
  - get_valid_int()   : safely reads a whole number from the user
"""

import mysql.connector
from db_config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE

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
