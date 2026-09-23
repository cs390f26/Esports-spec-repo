# Esports Reservation System Specs

This repo contains the specification for an esports reservation system. Users browse gaming spaces, choose a game, optionally add equipment, and reserve a session. Users can also view and cancel reservations. Station settings include computer specifications and availability. The prototype has no sign-in.

- [Use cases](use_cases.md) — Describes the booking experience, happy path, and error cases. These cases form the basis for acceptance tests.
- [API](openapi.yaml) — Describes the HTTP contract between the web browser (client) and the backend (server).
- [Data model](db.md) — Describes the SQL database tables, fields, and relationships.

## Screen Mockups

- [Overview](ui/01-overview.html) — Browse stations and view ongoing and upcoming sessions.
- [Reservation](ui/02-reservation.html) — Choose a space, time, game, and optional equipment, then confirm the booking.
- [Space details](ui/03-space-details.html) — View computer specifications and the station schedule.
- [Settings](ui/04-settings.html) — Update station details and active status, and view shared equipment.
- [My reservations](ui/05-my-reservations.html) — View and cancel bookings.
