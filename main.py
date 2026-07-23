# Main executing python file

"""
HOTEL / RESORT RESERVATION SYSTEM
CBSE Class 12 Computer Science Project

This program lets the hotel staff:
  0. Exit
  1. Register a new guest
  2. Add a new room
  3. Book a room for a guest
  4. View all current reservations
  5. View available rooms
  6. Cancel a reservation
  7. Generate bill / check-out a guest
  8. Search reservation by guest name
  9. Display all guests
  

The program is menu-driven and procedural 
"""

import mysql.connector

# ==========================================================
# DATABASE CONNECTION
# ==========================================================
def get_connection():
    """
    Creates and returns a connection object to the MySQL database.
    Change the host/user/password values to match your own MySQL setup.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sandship@119002",   # <-- change this to your MySQL password
        database="hotel_db"
    )
    return conn


# ==========================================================
# 1. ADD NEW GUEST
# ==========================================================
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


# ==========================================================
# 2. ADD NEW ROOM
# ==========================================================
def add_room():
    """
    Takes room details from the user and inserts a new row
    into the rooms table.
    """
    print("\n--- Add New Room ---")
    room_no = int(input("Enter room number: "))
    room_type = input("Enter room type (Single/Double/Deluxe/Suite): ")
    price = int(input("Enter price per day: "))

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


# ==========================================================
# 3. VIEW AVAILABLE ROOMS
# ==========================================================
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


# ==========================================================
# 4. BOOK A RESERVATION
# ==========================================================
def book_reservation():
    """
    Books a room for an existing guest:
      - asks for guest_id and room_no
      - checks the room is available
      - calculates total_amount = price_per_day * num_days
      - inserts a row into reservations
      - updates the room's status to 'Booked'
    """
    print("\n--- Book a Reservation ---")
    guest_id = int(input("Enter guest ID: "))
    room_no = int(input("Enter room number to book: "))
    checkin_date = input("Enter check-in date (DD-MM-YYYY): ")
    num_days = int(input("Enter number of days: "))

    conn = get_connection()
    cursor = conn.cursor()

    # Step 1: check if the room is available
    cursor.execute("SELECT price_per_day, status FROM rooms WHERE room_no = %s", (room_no,))
    result = cursor.fetchone()

    if result is None:
        print("Room number does not exist.")
    elif result[1] != "Available":
        print("Sorry, this room is already booked.")
    else:
        price_per_day = result[0]
        total_amount = price_per_day * num_days

        # Step 2: insert the reservation
        insert_query = """INSERT INTO reservations
                           (guest_id, room_no, checkin_date, num_days, total_amount, res_status)
                           VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (guest_id, room_no, checkin_date, num_days, total_amount, "Active")
        cursor.execute(insert_query, values)

        # Step 3: mark the room as booked
        cursor.execute("UPDATE rooms SET status = %s WHERE room_no = %s", ("Booked", room_no))

        conn.commit()
        print("Reservation successful! Total amount payable: Rs.", total_amount)

    cursor.close()
    conn.close()


# ==========================================================
# 5. VIEW ALL RESERVATIONS
# ==========================================================
def view_reservations():
    """
    Displays every reservation along with the guest name and room number,
    using a JOIN across the three tables.
    """
    print("\n--- All Reservations ---")
    conn = get_connection()
    cursor = conn.cursor()

    query = """SELECT reservations.res_id, guests.name, reservations.room_no,
                      reservations.checkin_date, reservations.num_days,
                      reservations.total_amount, reservations.res_status
               FROM reservations
               JOIN guests ON reservations.guest_id = guests.guest_id"""
    cursor.execute(query)
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No reservations found.")
    else:
        for row in rows:
            print("Res ID:", row[0], "| Guest:", row[1], "| Room:", row[2],
                  "| Check-in:", row[3], "| Days:", row[4],
                  "| Amount: Rs.", row[5], "| Status:", row[6])

    cursor.close()
    conn.close()


# ==========================================================
# 6. CANCEL A RESERVATION
# ==========================================================
def cancel_reservation():
    """
    Cancels an active reservation:
      - marks the reservation's status as 'Cancelled'
      - frees up the room by setting its status back to 'Available'
    """
    print("\n--- Cancel Reservation ---")
    res_id = int(input("Enter reservation ID to cancel: "))

    conn = get_connection()
    cursor = conn.cursor()

    # find the room number linked to this reservation
    cursor.execute("SELECT room_no, res_status FROM reservations WHERE res_id = %s", (res_id,))
    result = cursor.fetchone()

    if result is None:
        print("No such reservation found.")
    elif result[1] != "Active":
        print("This reservation is not active, cannot cancel.")
    else:
        room_no = result[0]

        cursor.execute("UPDATE reservations SET res_status = %s WHERE res_id = %s",
                        ("Cancelled", res_id))
        cursor.execute("UPDATE rooms SET status = %s WHERE room_no = %s",
                        ("Available", room_no))

        conn.commit()
        print("Reservation cancelled successfully.")

    cursor.close()
    conn.close()


# ==========================================================
# 7. GENERATE BILL / CHECK-OUT
# ==========================================================
def checkout_guest():
    """
    Checks a guest out:
      - shows the final bill for that reservation
      - marks the reservation as 'Checked Out'
      - frees up the room
    """
    print("\n--- Check-Out / Generate Bill ---")
    res_id = int(input("Enter reservation ID: "))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT guests.name, reservations.room_no, reservations.num_days,
                              reservations.total_amount, reservations.res_status
                       FROM reservations
                       JOIN guests ON reservations.guest_id = guests.guest_id
                       WHERE reservations.res_id = %s""", (res_id,))
    result = cursor.fetchone()

    if result is None:
        print("No such reservation found.")
    elif result[4] != "Active":
        print("This reservation is not active.")
    else:
        name, room_no, num_days, total_amount, status = result

        print("\n---------- FINAL BILL ----------")
        print("Guest Name   :", name)
        print("Room No      :", room_no)
        print("No. of Days  :", num_days)
        print("Total Amount : Rs.", total_amount)
        print("---------------------------------")

        cursor.execute("UPDATE reservations SET res_status = %s WHERE res_id = %s",
                        ("Checked Out", res_id))
        cursor.execute("UPDATE rooms SET status = %s WHERE room_no = %s",
                        ("Available", room_no))

        conn.commit()
        print("Guest checked out successfully.")

    cursor.close()
    conn.close()


# ==========================================================
# 8. SEARCH RESERVATION BY GUEST NAME
# ==========================================================
def search_by_guest_name():
    """
    Lets staff search for reservations using the guest's name
    (uses SQL LIKE for partial matching).
    """
    print("\n--- Search Reservation by Guest Name ---")
    search_name = input("Enter guest name (or part of it): ")

    conn = get_connection()
    cursor = conn.cursor()

    query = """SELECT reservations.res_id, guests.name, reservations.room_no,
                      reservations.checkin_date, reservations.res_status
               FROM reservations
               JOIN guests ON reservations.guest_id = guests.guest_id
               WHERE guests.name LIKE %s"""
    cursor.execute(query, ("%" + search_name + "%",))
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No matching reservations found.")
    else:
        for row in rows:
            print("Res ID:", row[0], "| Guest:", row[1], "| Room:", row[2],
                  "| Check-in:", row[3], "| Status:", row[4])

    cursor.close()
    conn.close()


# ==========================================================
# 9. DISPLAY ALL GUESTS
# ==========================================================
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


# ==========================================================
# MAIN MENU
# ==========================================================
def main():
    """
    Displays the menu in a loop and calls the correct function
    based on the user's choice, until the user chooses to exit.
    """
    while True:
        print("\n========== HOTEL RESERVATION SYSTEM ==========")
        print("1. Register New Guest")
        print("2. Add New Room")
        print("3. Book a Reservation")
        print("4. View All Reservations")
        print("5. View Available Rooms")
        print("6. Cancel Reservation")
        print("7. Check-Out / Generate Bill")
        print("8. Search Reservation by Guest Name")
        print("9. Display All Guests")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_guest()
        elif choice == "2":
            add_room()
        elif choice == "3":
            book_reservation()
        elif choice == "4":
            view_reservations()
        elif choice == "5":
            view_available_rooms()
        elif choice == "6":
            cancel_reservation()
        elif choice == "7":
            checkout_guest()
        elif choice == "8":
            search_by_guest_name()
        elif choice == "9":
            display_all_guests()
        elif choice == "0":
            print("Thank you for using the Hotel Reservation System.")
            break
        else:
            print("Invalid choice. Please try again.")


# ==========================================================
# PROGRAM ENTRY POINT
# ==========================================================
if __name__ == "__main__":
    main()