# Gaming Lounge Database Schema

This document describes the four tables in the provided schema diagram: `Spaces`, `Computers`, `Equipment`, and `Reservations`.

Primary keys use integer IDs. The diagram marks non-key fields with `?`, which appears to indicate that they are nullable; confirm this in the database definition before implementation. No defaults, status enums, or automatic ID generation are specified in the diagram.

## Spaces

Stores the physical spaces available in the gaming lounge, such as gaming stations or console areas.

| Column        | Type shown     | Key         | Purpose                                                                                 |
| ------------- | -------------- | ----------- | --------------------------------------------------------------------------------------- |
| `space_id`    | `INTEGER`      | Primary key | Unique identifier for a space.                                                          |
| `space_name`  | `VARCHAR(255)` | —           | Display name, such as Station 01 - Cyberhound Rig.                                      |
| `description` | `TEXT(65535)`  | —           | Description of the space and its features.                                              |
| `is_active`   | `BOOLEAN`      | —           | Whether the space is active. This is separate from time-based reservation availability. |

`Spaces.space_id` is referenced by `Computers.space_id`.

## Computers

Stores computers and associates each computer with a space.

| Column        | Type shown     | Key / relationship          | Purpose                                 |
| ------------- | -------------- | --------------------------- | --------------------------------------- |
| `computer_id` | `INTEGER`      | Primary key                 | Unique identifier for a computer.       |
| `space_id`    | `INTEGER`      | Linked to `Spaces.space_id` | Space assigned to the computer.         |
| `hostname`    | `VARCHAR(255)` | —                           | Computer name, such as CH-RIG-01.       |
| `specs`       | `TEXT(65535)`  | —                           | Hardware specifications stored as text. |
| `status`      | `VARCHAR(255)` | —                           | Operational status of the computer.     |

Example status values could include `AVAILABLE`, `IN_USE`, `MAINTENANCE`, and `OFFLINE`. These are application conventions, not constraints defined in the diagram.

## Equipment

Stores individual accessories, such as headsets and controllers.

| Column          | Type shown     | Key         | Purpose                                            |
| --------------- | -------------- | ----------- | -------------------------------------------------- |
| `equipment_id`  | `INTEGER`      | Primary key | Unique identifier for an equipment item.           |
| `item_name`     | `VARCHAR(255)` | —           | Display name of the item.                          |
| `category`      | `VARCHAR(255)` | —           | Equipment category, such as HEADSET or CONTROLLER. |
| `serial_number` | `VARCHAR(255)` | —           | Serial number associated with the item.            |
| `status`        | `VARCHAR(255)` | —           | Item status, such as AVAILABLE or MAINTENANCE.     |

## Reservations

Stores bookings for a space, including the user, scheduled interval, and reservation status.

| Column           | Type shown     | Key / relationship | Purpose                                            |
| ---------------- | -------------- | ------------------ | -------------------------------------------------- |
| `reservation_id` | `INTEGER`      | Primary key        | Unique identifier for a reservation.               |
| `user_name`      | `VARCHAR(255)` |                    | Identifier for the user making the reservation.    |
| `space_id`       | `INTEGER`      |                    | Space associated with the reservation.             |
| `start_time`     | `TIMESTAMP`    | —                  | Scheduled start of the reservation.                |
| `end_time`       | `TIMESTAMP`    | —                  | Scheduled end of the reservation.                  |
| `status`         | `VARCHAR(255)` | —                  | Reservation state, such as CONFIRMED or CANCELLED. |
| `created_at`     | `TIMESTAMP`    | —                  | Time the reservation record was created.           |

For JSON payloads, represent timestamps using ISO 8601, such as `2026-09-23T14:00:00Z`. The diagram does not specify database timezone handling or a default for `created_at`.
