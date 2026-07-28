"""
HOTEL / RESORT RESERVATION SYSTEM - MAIN PROGRAM
CBSE Class 12 Computer Science Project

This is the entry point of the program. It only holds the menu loop.
All the actual work is done by functions imported from the other
modules in this folder:

  db_connection.py          -> database connection + input validation
  guest_operations.py       -> guest-related functions
  room_operations.py        -> room-related functions
  reservation_operations.py -> booking, billing, search, statistics

Run this file (not the other ones) to start the program:
    python main.py

All four files must be kept in the SAME folder, because Python's
import statement looks for them alongside main.py.
"""

from guest_operations import *
from room_operations import *
from reservation_operations import *


def main():
    """
    Displays the menu in a loop and calls the correct function
    based on the user's choice, until the user chooses to exit.
    """
    while True:
        print("\n========== HOTEL RESERVATION SYSTEM ==========")

        print("\n============== GUEST OPERATIONS ==============")
        print("1. Register New Guest")
        print("2. Modify Guest Details")
        print("3. Delete Guest")
        print("4. Display All Guests")

        print("\n=========== RESERVATION OPERATIONS ===========")
        print("5. Add New Room")
        print("6. Book a Reservation")
        print("7. View All Reservations")
        print("8. View Available Rooms")
        print("9. Cancel Reservation")
        print("10. Check-Out / Generate Bill")
        print("11. Search Reservation by Guest Name")

        print("\n============== HOTEL STATISTICS ==============")

        print("12. View Hotel Statistics")
        print("0. Exit")
 
        choice = input("Enter your choice: ")
 
        if choice == "1":
            add_guest()
        elif choice == "2":
            modify_guest()
        elif choice == "3":
            delete_guest()
        elif choice == "4":
            add_room()
        elif choice == "5":
            display_all_guests()
        elif choice == "6":
            book_reservation()
        elif choice == "7":
            view_reservations()
        elif choice == "8":
            view_available_rooms()
        elif choice == "9":
            cancel_reservation()
        elif choice == "10":
            checkout_guest()
        elif choice == "11":
            search_by_guest_name()
        elif choice == "12":
            view_statistics()
        elif choice == "0":
            print("Thank you for using the Hotel Reservation System.")
            break
        else:
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    main()
