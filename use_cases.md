# Reservation Page Use Cases

## Happy Path: Reserve a Space

**Goal:** A user books an available space, selects a game, and optionally adds equipment.

**Preconditions:** The system has spaces and a game catalog available. The selected space and any requested equipment are available for the requested time period.

### 1. Browse the Home Page

1. The user lands on the home page.
2. The system displays available spaces and reservations currently in progress.
3. The user reviews the spaces and their details, then opens the reservation page.

**Expected result:** The user can identify a suitable space and begin booking it. Current availability is distinct from availability for a future booking period.

### 2. Choose Reservation Details

1. The user selects a space.
2. The user selects a date, start time, and end time.
3. The system checks that the start time is not in the past and that the duration is between 30 minutes and 12 hours, inclusive.
4. The system verifies that the space is available for the entire selected period.
5. The user optionally selects equipment. The system shows which items are available for the selected period.
6. The user selects a game from the catalog of games supported by the selected system.
7. The user proceeds to review the reservation.

**Expected result:** The user has selected a valid space, time period, and game, with or without optional equipment.

### 3. Review and Confirm

1. The system displays a summary containing the space, date, start and end times, duration, selected game, and any equipment.
2. The system asks, “Are you sure you want to schedule this reservation?”
3. The user can return to edit the details or confirm the booking.
4. The user confirms the reservation.
5. The system rechecks availability and saves the reservation with its selected game and equipment. The availability check and booking must prevent competing users from booking the same resources for overlapping periods.

**Expected result:** A confirmed reservation is created, and the space and selected equipment are reserved for that period.

### 4. View Booking Confirmation

1. The system displays a success message and the reservation details.
2. The user can review the confirmed booking.
3. The system updates availability for the booked period. When the reservation begins, it appears among the ongoing reservations on the home page.

**Success outcome:** The user knows the booking succeeded and can clearly see where and when to arrive, what game they selected, and which equipment is included.

## Alternate Happy Path: Reserve Without Equipment

The user follows the same booking flow but skips equipment selection. The review and confirmation screens show “No additional equipment.” The reservation succeeds as long as the space, time period, and game selection are valid.

## Validation and Error Cases

For each error, the system preserves the user's selections, explains the issue, and allows the user to correct it without restarting the booking flow.

| Use case                                                                                   | Expected behavior                                                                                                      | Suggested message                                                                       |
| ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| User selects a start time in the past.                                                     | Block booking and ask the user to choose a current or future start time. Recheck at confirmation.                      | “Choose a start time that is not in the past.”                                          |
| User selects a space that is already booked for any part of the requested period.          | Block booking and let the user change the space or time period.                                                        | “This space is already booked during your selected time. Choose another space or time.” |
| User selects a duration shorter than 30 minutes.                                           | Block booking and ask the user to extend the reservation.                                                              | “Reservations must be at least 30 minutes long.”                                        |
| User selects a duration longer than 12 hours.                                              | Block booking and ask the user to shorten the reservation.                                                             | “Reservations cannot exceed 12 hours.”                                                  |
| User selects an end time at or before the start time.                                      | Block booking and ask for a later end time.                                                                            | “End time must be after start time.”                                                    |
| User selects equipment whose active use or existing booking overlaps the requested period. | Block booking with that item and allow the user to remove it, choose another item, or change the time.                 | “This equipment is unavailable during your selected time.”                              |
| A space or equipment item becomes unavailable before confirmation completes.               | Do not create a partial booking. Explain the conflict and return the user to their selections.                         | “Availability changed. Please review your space and equipment selections.”              |
| The system cannot save the reservation.                                                    | Show an error and allow a retry without creating duplicate bookings. Show success only after the booking is confirmed. | “We couldn't complete your reservation. Please try again.”                              |

Equipment being used now does not prevent a future booking when that use does not overlap the requested period.
