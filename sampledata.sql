-- Sample data for the tables described in db.md.
-- Timestamps are in the lounge's local time.
-- Space 2 is inactive; reservation 8802 was booked before it was turned off and is kept.

INSERT INTO Spaces (space_id, space_name, description, is_active) VALUES
  (1, 'Station 01 - Cyberhound Rig', 'PC gaming station with a 240Hz monitor.', TRUE),
  (2, 'Station 02 - Cyberhound Rig', 'PC gaming station with a 165Hz monitor.', FALSE);

INSERT INTO Computers (computer_id, space_id, hostname, specs, status) VALUES
  (1, 1, 'CH-RIG-01', 'Intel Core i7-13700K, RTX 4080, 32GB DDR5 RAM, 1TB NVMe SSD, 240Hz Monitor', 'AVAILABLE'),
  (2, 2, 'CH-RIG-02', 'AMD Ryzen 7 7800X3D, RTX 4070 Ti, 32GB DDR5 RAM, 2TB NVMe SSD, 165Hz Monitor', 'AVAILABLE');

INSERT INTO Equipment (equipment_id, item_name, category, serial_number, status) VALUES
  (1, 'Logitech G Pro X Wireless Headset #1', 'HEADSET', 'MOCK-HEADSET-001', 'AVAILABLE'),
  (2, 'Xbox Elite Wireless Controller #1', 'CONTROLLER', 'MOCK-CONTROLLER-001', 'AVAILABLE');

INSERT INTO Reservations (reservation_id, user_name, space_id, start_time, end_time, status, created_at) VALUES
  (8801, 'usr_001', 1, '2026-09-23 14:00:00', '2026-09-23 16:00:00', 'CONFIRMED', '2026-09-22 18:30:00'),
  (8802, 'usr_002', 2, '2026-09-23 18:00:00', '2026-09-23 20:00:00', 'CONFIRMED', '2026-09-22 20:15:00');

INSERT INTO ReservationEquipment (reservation_id, equipment_id) VALUES
  (8801, 1),
  (8801, 2),
  (8802, 2);
