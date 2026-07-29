"""
ROOM_OPERATIONS MODULE
CBSE Class 12 Computer Science Project

Contains every function related to room records:
  - add_room()            -> Create
  - view_available_rooms()-> Read
  - modify_room()         -> Update
  - delete_room()         -> Delete
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


def modify_room():
    """
    Updates the type and price of an existing room.
      - asks for room_no
      - checks the room exists
      - asks for new type and price and overwrites the old row
    (status is not changed here on purpose -- status is only
    ever changed by booking/cancel/checkout, never by this menu
    option, so that room availability always stays consistent
    with the reservations table.)
    """
    print("\n--- Modify Room Details ---")
    room_no = get_valid_int("Enter room number to modify: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT room_no FROM rooms WHERE room_no = %s", (room_no,))
    if cursor.fetchone() is None:
        print("No room found with this number.")
        cursor.close()
        conn.close()
        return

    print("Enter the new details below (this will replace the old details):")
    room_type = input("Enter new room type: ")
    price = get_valid_int("Enter new price per day: ")

    query = "UPDATE rooms SET room_type = %s, price_per_day = %s WHERE room_no = %s"
    values = (room_type, price, room_no)

    try:
        cursor.execute(query, values)
        conn.commit()
        print("Room details updated successfully.")
    except mysql.connector.Error as e:
        print("Error while updating room:", e)

    cursor.close()
    conn.close()


def delete_room():
    """
    Deletes a room record.
      - checks the room exists
      - tries to delete; if the room has reservations linked to
        it (foreign key), MySQL will refuse the delete, so this
        is caught and explained instead of crashing the program
    """
    print("\n--- Delete Room ---")
    room_no = get_valid_int("Enter room number to delete: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT room_type, status FROM rooms WHERE room_no = %s", (room_no,))
    result = cursor.fetchone()

    if result is None:
        print("No room found with this number.")
    else:
        confirm = input("Are you sure you want to delete room " + str(room_no) + " (" + result[0] + ")? (Y/N): ")
        if confirm.upper() == "Y":
            try:
                cursor.execute("DELETE FROM rooms WHERE room_no = %s", (room_no,))
                conn.commit()
                print("Room deleted successfully.")
            except mysql.connector.Error as e:
                print("Cannot delete this room. It likely has one or more")
                print("reservations linked to it (past or present). Those")
                print("reservations must be removed first.")
                print("(Technical detail:", e, ")")
        else:
            print("Delete cancelled.")

    cursor.close()
    conn.close()
