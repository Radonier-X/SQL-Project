"""
ROOM_OPERATIONS MODULE
CBSE Class 12 Computer Science Project

Contains every function related to room records:
  - add_room()
  - view_available_rooms()
"""

import mysql.connector
from db_connection import get_connection, get_valid_int


def add_room():
    """
    Takes room details from the user and inserts a new row
    into the rooms table.
    """
    print("\n--- Add New Room ---")
    room_no = get_valid_int("Enter room number: ")
    room_type = input("Enter room type (Single/Double/Deluxe/Suite): ")
    price = get_valid_int("Enter price per day: ")

    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO rooms (room_no, room_type, price_per_day, status) VALUES (%s, %s, %s, %s)"
    values = (room_no, room_type, price, "Available")

    try:
        cursor.execute(query, values)
        conn.commit()
        print("Room added successfully.")
    except mysql.connector.Error as e:
        print("Error while adding room:", e)

    cursor.close()
    conn.close()


def view_available_rooms():
    """
    Displays all rooms whose status is 'Available'.
    """
    print("\n--- Available Rooms ---")
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT room_no, room_type, price_per_day FROM rooms WHERE status = %s"
    cursor.execute(query, ("Available",))
    rooms = cursor.fetchall()

    if len(rooms) == 0:
        print("No rooms available right now.")
    else:
        print("Room No | Type    | Price/Day")
        for room in rooms:
            print(room[0], "|", room[1], "|", room[2])

    cursor.close()
    conn.close()


