"""
RESERVATION_OPERATIONS MODULE
CBSE Class 12 Computer Science Project

Contains every function related to bookings, billing, search
and statistics. Grouped together because they all read/write
the reservations table (often together with rooms/guests via JOIN).
  - book_reservation()
  - view_reservations()
  - cancel_reservation()
  - checkout_guest()
  - search_by_guest_name()
  - view_statistics()
"""

from db_connection import get_connection, get_valid_int


def book_reservation():
    """
    Books a room for an existing guest:
      - checks the guest ID exists
      - checks the room is available
      - calculates total_amount = price_per_day * num_days
      - inserts a row into reservations
      - updates the room's status to 'Booked'
    """
    print("\n--- Book a Reservation ---")
    guest_id = get_valid_int("Enter guest ID: ")
    room_no = get_valid_int("Enter room number to book: ")
    checkin_date = input("Enter check-in date (DD-MM-YYYY): ")
    num_days = get_valid_int("Enter number of days: ")

    # basic format check for the date (does not use any date library,
    # just checks that the text follows the DD-MM-YYYY pattern)
    date_parts = checkin_date.split("-")
    if len(date_parts) != 3 or not (date_parts[0].isdigit() and date_parts[1].isdigit() and date_parts[2].isdigit()):
        print("Invalid date format. Please use DD-MM-YYYY. Booking cancelled.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    # Step 1: check that the guest ID actually exists
    cursor.execute("SELECT guest_id FROM guests WHERE guest_id = %s", (guest_id,))
    guest_check = cursor.fetchone()

    if guest_check is None:
        print("No guest found with this ID. Please register the guest first (Option 1).")
        cursor.close()
        conn.close()
        return

    # Step 2: check if the room is available
    cursor.execute("SELECT price_per_day, status FROM rooms WHERE room_no = %s", (room_no,))
    result = cursor.fetchone()

    if result is None:
        print("Room number does not exist.")
    elif result[1] != "Available":
        print("Sorry, this room is already booked.")
    else:
        price_per_day = result[0]
        total_amount = price_per_day * num_days

        # Step 3: insert the reservation
        insert_query = """INSERT INTO reservations
                           (guest_id, room_no, checkin_date, num_days, total_amount, res_status)
                           VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (guest_id, room_no, checkin_date, num_days, total_amount, "Active")
        cursor.execute(insert_query, values)

        # Step 4: mark the room as booked
        cursor.execute("UPDATE rooms SET status = %s WHERE room_no = %s", ("Booked", room_no))

        conn.commit()
        print("Reservation successful! Total amount payable: Rs.", total_amount)

    cursor.close()
    conn.close()


def view_reservations():
    """
    Displays every reservation along with the guest name and room number,
    using a JOIN across the guests and reservations tables.
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


def cancel_reservation():
    """
    Cancels an active reservation:
      - marks the reservation's status as 'Cancelled'
      - frees up the room by setting its status back to 'Available'
    """
    print("\n--- Cancel Reservation ---")
    res_id = get_valid_int("Enter reservation ID to cancel: ")

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


def checkout_guest():
    """
    Checks a guest out:
      - shows the final bill for that reservation
      - marks the reservation as 'Checked Out'
      - frees up the room
    """
    print("\n--- Check-Out / Generate Bill ---")
    res_id = get_valid_int("Enter reservation ID: ")

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


def view_statistics():
    """
    Displays a short summary report for the hotel using SQL
    aggregate functions:
      - COUNT() to count total and available rooms
      - SUM()   to add up revenue from checked-out guests
      - AVG()   to find the average room price
    """
    print("\n--- Hotel Statistics ---")
    conn = get_connection()
    cursor = conn.cursor()

    # total number of rooms
    cursor.execute("SELECT COUNT(*) FROM rooms")
    total_rooms = cursor.fetchone()[0]

    # number of rooms currently available
    cursor.execute("SELECT COUNT(*) FROM rooms WHERE status = %s", ("Available",))
    available_rooms = cursor.fetchone()[0]

    occupied_rooms = total_rooms - available_rooms

    # average price per day across all rooms
    cursor.execute("SELECT AVG(price_per_day) FROM rooms")
    avg_price = cursor.fetchone()[0]

    # total revenue collected from guests who have checked out
    cursor.execute("SELECT SUM(total_amount) FROM reservations WHERE res_status = %s", ("Checked Out",))
    total_revenue = cursor.fetchone()[0]

    # SUM() returns None (not 0) if there are no matching rows,
    # so this needs to be handled to avoid printing "None"
    if total_revenue is None:
        total_revenue = 0

    print("Total Rooms       :", total_rooms)
    print("Occupied Rooms    :", occupied_rooms)
    print("Available Rooms   :", available_rooms)
    if avg_price is not None:
        print("Average Room Price: Rs.", round(avg_price, 2))
    print("Total Revenue     : Rs.", total_revenue)

    cursor.close()
    conn.close()
