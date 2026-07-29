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
    """
    Displays the menu in a loop and calls the correct function
    based on the user's choice, until the user chooses to exit.
    """
    while True:
        print("\n========== HOTEL RESERVATION SYSTEM ==========")
 
        print("\n============== GUEST OPERATIONS ===============")
        print("1.  Register New Guest        (Create)")
        print("2.  Display All Guests        (Read)")
        print("3.  Modify Guest Details      (Update)")
        print("4.  Delete Guest              (Delete)")
 
        print("\n=============== ROOM OPERATIONS ================")
        print("5.  Add New Room              (Create)")
        print("6.  View Available Rooms      (Read)")
        print("7.  Modify Room Details       (Update)")
        print("8.  Delete Room               (Delete)")
 
        print("\n============ RESERVATION OPERATIONS ============")
        print("9.  Book a Reservation        (Create)")
        print("10. View All Reservations     (Read)")
        print("11. Modify Reservation        (Update)")
        print("12. Cancel Reservation        (status change)")
        print("13. Delete Reservation        (Delete)")
        print("14. Check-Out / Generate Bill")
        print("15. Search Reservation by Guest Name")
 
        print("\n============== HOTEL STATISTICS ================")
        print("16. View Hotel Statistics")
        print("0.  Exit")
 
        choice = input("Enter your choice: ")
 
        if choice == "1":
            add_guest()
        elif choice == "2":
            display_all_guests()
        elif choice == "3":
            modify_guest()
        elif choice == "4":
            delete_guest()
        elif choice == "5":
            add_room()
        elif choice == "6":
            view_available_rooms()
        elif choice == "7":
            modify_room()
        elif choice == "8":
            delete_room()
        elif choice == "9":
            book_reservation()
        elif choice == "10":
            view_reservations()
        elif choice == "11":
            modify_reservation()
        elif choice == "12":
            cancel_reservation()
        elif choice == "13":
            delete_reservation()
        elif choice == "14":
            checkout_guest()
        elif choice == "15":
            search_by_guest_name()
        elif choice == "16":
            view_statistics()
        elif choice == "0":
            print("Thank you for using the Hotel Reservation System.")
            break
        else:
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    main()
