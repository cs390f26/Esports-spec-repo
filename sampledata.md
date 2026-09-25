# Sample Data

[sampledata.sql](sampledata.sql) inserts a small data set into the tables described in [db.md](db.md). Run [schema.sql](schema.sql) first to create the tables.

| Table                  | Rows | Notes                                                                                   |
| ---------------------- | ---- | --------------------------------------------------------------------------------------- |
| `Spaces`               | 2    | Station 01 is active. Station 02 is inactive.                                           |
| `Computers`            | 2    | One per space, both `AVAILABLE`.                                                        |
| `Equipment`            | 2    | One headset and one controller, both `AVAILABLE`.                                       |
| `Reservations`         | 2    | Both `CONFIRMED` on 2026-09-23: Station 01 at 14:00–16:00 and Station 02 at 18:00–20:00. |
| `ReservationEquipment` | 3    | Reservation 8801 has both items. Reservation 8802 has the controller.                   |

Reservation 8802 was booked before Station 02 was turned off and is kept. The controller appears in both reservations because they are in different blocks.

Timestamps are in the lounge's local time. `Reservations.user_name` holds the same identifier the API calls `user_id`.
