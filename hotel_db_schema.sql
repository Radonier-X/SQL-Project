/*
============================================================
HOTEL / RESORT RESERVATION SYSTEM - DATABASE SCHEMA
CBSE Class 12 Computer Science Project

Run this whole file in MySQL (Workbench, or `mysql -u root -p < hotel_db_schema.sql`)
before running hotel_reservation.py for the first time.
============================================================
*/

CREATE DATABASE IF NOT EXISTS hotel_db;
USE hotel_db;

/*
------------------------------------------------------------
Table 1: GUESTS
Stores details of every guest who has ever registered.
guest_id is AUTO_INCREMENT so the program does not need to generate IDs manually.
------------------------------------------------------------
*/
CREATE TABLE guests (
    guest_id   INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(50) NOT NULL,
    phone      VARCHAR(15),
    address    VARCHAR(100),
    id_proof   VARCHAR(30)
);

/*
------------------------------------------------------------
Table 2: ROOMS
room_no is chosen (not auto-generated) by the staff, so it
is the primary key directly.
Status is either 'Available' or 'Booked'.
-- ------------------------------------------------------------
*/
CREATE TABLE rooms (
    room_no        INT PRIMARY KEY,
    room_type      VARCHAR(20),
    price_per_day  INT,
    status         VARCHAR(15) DEFAULT 'Available'
);

/*
------------------------------------------------------------
Table 3: RESERVATIONS
Links guests and rooms. guest_id and room_no are foreign keys.
checkin_date is stored as VARCHAR (not DATE)
the date is kept as plain text in DD-MM-YYYY format.
res_status is one of: 'Active', 'Cancelled', 'Checked Out'.
------------------------------------------------------------
*/
CREATE TABLE reservations (
    res_id         INT AUTO_INCREMENT PRIMARY KEY,
    guest_id       INT,
    room_no        INT,
    checkin_date   VARCHAR(15),
    num_days       INT,
    total_amount   INT,
    res_status     VARCHAR(15),
    FOREIGN KEY (guest_id) REFERENCES guests(guest_id),
    FOREIGN KEY (room_no) REFERENCES rooms(room_no)
);

/*
============================================================
SAMPLE DATA (optional - insert this so the program has
something to show during your viva demo)
============================================================
*/

/*
INSERT INTO guests (name, phone, address, id_proof) VALUES
('Rohan Sharma', '9876543210', 'Delhi', 'AADHAR1234'),
('Priya Menon', '9123456780', 'Chennai', 'AADHAR5678'),
('Arjun Verma', '9988776655', 'Mumbai', 'PAN1122AB');

INSERT INTO rooms (room_no, room_type, price_per_day, status) VALUES
(101, 'Single', 1500, 'Available'),
(102, 'Double', 2500, 'Available'),
(201, 'Deluxe', 4000, 'Available'),
(301, 'Suite', 7000, 'Available');



-- A couple of sample reservations. If you insert these, remember
-- to also update the matching room's status to 'Booked' so the
-- data stays consistent with what the program itself would do.

INSERT INTO reservations (guest_id, room_no, checkin_date, num_days, total_amount, res_status) VALUES
(1, 101, '20-07-2026', 3, 4500, 'Active');

UPDATE rooms SET status = 'Booked' WHERE room_no = 101;

*/
