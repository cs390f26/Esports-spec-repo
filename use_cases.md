# Reservation Page Use Cases

## Happy Path: Reserve a Space

**Goal:** A user books an available space, selects a game, and optionally adds equipment.

**Preconditions:** The system has spaces and a game catalog available. The selected space and any requested equipment are available for the requested time block.

**Time blocks:** Reservations are made in fixed 2-hour blocks from 10:00 to 22:00 in the lounge's local time: 10:00–12:00, 12:00–14:00, 14:00–16:00, 16:00–18:00, 18:00–20:00, and 20:00–22:00. A block is identified by a date and an hour range. Users cannot choose custom start or end times.

### 1. Browse the Home Page

1. The user lands on the home page.
2. The system displays the current time block (for example, "Current time block · Sep 23, 2026 · 16:00–18:00"), which spaces are available in it, and reservations currently in progress. Outside lounge hours, it shows the next time block instead.
3. The user reviews the spaces and their details, then opens the reservation page.

**Expected result:** The user can identify a suitable space and begin booking it. Availability in the current block is distinct from availability for a future block.


### 2. Choose Reservation Details

1. The user selects a space.
2. The user selects a date and then one of that date's time blocks. Blocks that have already started or are booked for the selected space are shown but cannot be selected.
3. The system checks that the block has not started.
4. The system verifies that the space is available for the selected block.
5. The user optionally selects equipment. The system shows which items are available for the selected block.
6. The user selects a game from the catalog of games supported by the selected system.
7. The user proceeds to review the reservation.

**Expected result:** The user has selected a valid space, time block, and game, with or without optional equipment.

### 3. Review and Confirm

1. The system displays a summary containing the space, date, time block, selected game, and any equipment.
2. The system asks, “Are you sure you want to schedule this reservation?”
3. The user can return to edit the details or confirm the booking.
4. The user confirms the reservation.
5. The system rechecks availability and saves the reservation with its selected game and equipment. The availability check and booking must prevent competing users from booking the same resources in the same block.

**Expected result:** A confirmed reservation is created, and the space and selected equipment are reserved for that block.

### 4. View Booking Confirmation

1. The system displays a success message and the reservation details.
2. The user can review the confirmed booking.
3. The system updates availability for the booked block. When the block begins, the reservation appears among the ongoing reservations on the home page.

**Success outcome:** The user knows the booking succeeded and can clearly see where and when to arrive, what game they selected, and which equipment is included.

## Alternate Happy Path: Reserve Without Equipment

The user follows the same booking flow but skips equipment selection. The review and confirmation screens show “No additional equipment.” The reservation succeeds as long as the space, time block, and game selection are valid.

## Validation and Error Cases

For each error, the system preserves the user's selections, explains the issue, and allows the user to correct it without restarting the booking flow.

| Use case                                                                                   | Expected behavior                                                                                                      | Suggested message                                                                       |
| ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| User selects a time block that has already started.                                        | Block booking and ask the user to choose a later block. Recheck at confirmation.                                       | “Choose a time block that has not started yet.”                                         |
| The request names a time that is not one of the defined blocks.                            | Reject the request. The UI only offers defined blocks, so this applies to direct API calls.                            | “Choose one of the available time blocks.”                                              |
| User selects a space that is already booked for the selected block.                        | Block booking and let the user change the space or time block.                                                         | “This space is already booked during your selected time. Choose another space or time.” |
| User selects equipment that is in use or already booked for the selected block.            | Block booking with that item and allow the user to remove it, choose another item, or change the block.                | “This equipment is unavailable during your selected time.”                              |
| A space or equipment item becomes unavailable before confirmation completes.               | Do not create a partial booking. Explain the conflict and return the user to their selections.                         | “Availability changed. Please review your space and equipment selections.”              |
| The system cannot save the reservation.                                                    | Show an error and allow a retry without creating duplicate bookings. Show success only after the booking is confirmed. | “We couldn't complete your reservation. Please try again.”                              |

Equipment being used now does not prevent booking it for a different block.
