"""
GUEST_OPERATIONS MODULE
CBSE Class 12 Computer Science Project

Contains every function related to guest records:
  - add_guest()
  - display_all_guests()
"""

import mysql.connector
from db_connection import get_connection, get_valid_int


def add_guest():
    """
    Takes guest details from the user and inserts a new row
    into the guests table.
    """
    print("\n--- Register New Guest ---")
    name = input("Enter guest name: ")
    phone = input("Enter phone number: ")
    address = input("Enter address: ")
    id_proof = input("Enter ID proof number: ")

    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO guests (name, phone, address, id_proof) VALUES (%s, %s, %s, %s)"
    values = (name, phone, address, id_proof)

    try:
        cursor.execute(query, values)
        conn.commit()
        print("Guest registered successfully. Guest ID:", cursor.lastrowid)
    except mysql.connector.Error as e:
        print("Error while adding guest:", e)

    cursor.close()
    conn.close()

def modify_guest():
    """
    Updates the details of an existing guest.
      - asks for guest_id
      - checks the guest exists
      - asks for new details and overwrites the old row
    """
    print("\n--- Modify Guest Details ---")
    guest_id = get_valid_int("Enter guest ID to modify: ")
 
    conn = get_connection()
    cursor = conn.cursor()
 
    cursor.execute("SELECT guest_id FROM guests WHERE guest_id = %s", (guest_id,))
    if cursor.fetchone() is None:
        print("No guest found with this ID.")
        cursor.close()
        conn.close()
        return
 
    print("Enter the new details below (this will replace the old details):")
    name = input("Enter new name: ")
    phone = input("Enter new phone number: ")
    address = input("Enter new address: ")
    id_proof = input("Enter new ID proof number: ")
 
    query = """UPDATE guests
               SET name = %s, phone = %s, address = %s, id_proof = %s
               WHERE guest_id = %s"""
    values = (name, phone, address, id_proof, guest_id)
 
    try:
        cursor.execute(query, values)
        conn.commit()
        print("Guest details updated successfully.")
    except mysql.connector.Error as e:
        print("Error while updating guest:", e)
 
    cursor.close()
    conn.close()
 
 
def delete_guest():
    """
    Deletes a guest record.
      - checks the guest exists
      - tries to delete; if the guest has reservations linked to
        them (foreign key), MySQL will refuse the delete, so this
        is caught and explained instead of crashing the program
    """
    print("\n--- Delete Guest ---")
    guest_id = get_valid_int("Enter guest ID to delete: ")
 
    conn = get_connection()
    cursor = conn.cursor()
 
    cursor.execute("SELECT name FROM guests WHERE guest_id = %s", (guest_id,))
    result = cursor.fetchone()
 
    if result is None:
        print("No guest found with this ID.")
    else:
        confirm = input("Are you sure you want to delete guest '" + result[0] + "'? (Y/N): ")
        if confirm.upper() == "Y":
            try:
                cursor.execute("DELETE FROM guests WHERE guest_id = %s", (guest_id,))
                conn.commit()
                print("Guest deleted successfully.")
            except mysql.connector.Error as e:
                print("Cannot delete this guest. They likely have one or more")
                print("reservations linked to their record. Cancel/remove those")
                print("reservations first.")
                print("(Technical detail:", e, ")")
        else:
            print("Delete cancelled.")
 
    cursor.close()
    conn.close()


def display_all_guests():
    """
    Displays every guest currently registered in the system.
    """
    print("\n--- All Registered Guests ---")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT guest_id, name, phone, address FROM guests")
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No guests registered yet.")
    else:
        for row in rows:
            print("ID:", row[0], "| Name:", row[1], "| Phone:", row[2], "| Address:", row[3])

    cursor.close()
    conn.close()
