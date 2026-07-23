-- ==========================================================
-- HOTEL / RESORT RESERVATION SYSTEM - DATABASE SCHEMA
-- CBSE Class 12 Computer Science Project
-- ==========================================================

CREATE DATABASE IF NOT EXISTS hotel_db;
USE hotel_db;

-- ----------------------------------------------------------
-- Table 1: ROOMS
-- Stores information about every room in the hotel
-- ----------------------------------------------------------
CREATE TABLE IF NOT EXISTS rooms (
    room_no       INT PRIMARY KEY,
    room_type     VARCHAR(20)   NOT NULL,   -- e.g. Single, Double, Deluxe, Suite
    price_per_day INT           NOT NULL,
    status        VARCHAR(10)   DEFAULT 'Available'  -- 'Available' or 'Booked'
);

-- ----------------------------------------------------------
-- Table 2: GUESTS
-- Stores information about every guest who registers
-- ----------------------------------------------------------
CREATE TABLE IF NOT EXISTS guests (
    guest_id   INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(50)  NOT NULL,
    phone      VARCHAR(15)  NOT NULL,
    address    VARCHAR(100),
    id_proof   VARCHAR(30)              -- e.g. Aadhaar number, Passport number
);

-- ----------------------------------------------------------
-- Table 3: RESERVATIONS
-- Links a guest to a room for a certain number of days
-- ----------------------------------------------------------
CREATE TABLE IF NOT EXISTS reservations (
    res_id        INT AUTO_INCREMENT PRIMARY KEY,
    guest_id      INT          NOT NULL,
    room_no       INT          NOT NULL,
    checkin_date  VARCHAR(15)  NOT NULL,   -- stored as text, e.g. '23-07-2026'
    num_days      INT          NOT NULL,
    total_amount  INT          NOT NULL,
    res_status    VARCHAR(15)  DEFAULT 'Active',  -- 'Active' or 'Cancelled' or 'Checked Out'
    FOREIGN KEY (guest_id) REFERENCES guests(guest_id),
    FOREIGN KEY (room_no)  REFERENCES rooms(room_no)
);

-- ----------------------------------------------------------
-- SAMPLE DATA (so the program has something to work with)
-- ----------------------------------------------------------
INSERT INTO rooms (room_no, room_type, price_per_day, status) VALUES
    (101, 'Single', 1500, 'Available'),
    (102, 'Single', 1500, 'Available'),
    (201, 'Double', 2500, 'Available'),
    (202, 'Double', 2500, 'Available'),
    (301, 'Deluxe', 4000, 'Available'),
    (302, 'Suite',  6000, 'Available');

INSERT INTO guests (name, phone, address, id_proof) VALUES
    ('Ravi Kumar',   '9876543210', 'Coimbatore', 'AADHAR1234'),
    ('Anita Sharma', '9123456780', 'Chennai',    'AADHAR5678');
