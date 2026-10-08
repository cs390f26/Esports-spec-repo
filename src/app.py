import os
import sqlite3
from datetime import date, datetime, timedelta

from flask import Flask, g, jsonify, redirect, request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, "esports.db")
START_HOURS = (10, 12, 14, 16, 18, 20)

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, "ui"), static_url_path="")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE, isolation_level=None)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def error(status, code, message):
    return jsonify(code=code, message=message), status


def parse_date(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def block_times(day, start_hour):
    start = datetime(day.year, day.month, day.day, start_hour)
    return start, start + timedelta(hours=2)


def db_time(value):
    return value.strftime("%Y-%m-%d %H:%M:%S")


def iso_time(value):
    return value.replace(" ", "T")


def reservation_json(db, row):
    equipment_ids = [
        r["equipment_id"]
        for r in db.execute(
            "SELECT equipment_id FROM ReservationEquipment WHERE reservation_id = ? ORDER BY equipment_id",
            (row["reservation_id"],),
        )
    ]
    return {
        "reservation_id": row["reservation_id"],
        "user_id": row["user_name"],
        "space_id": row["space_id"],
        "equipment_ids": equipment_ids,
        "start_time": iso_time(row["start_time"]),
        "end_time": iso_time(row["end_time"]),
        "status": row["status"],
        "created_at": iso_time(row["created_at"]),
    }


@app.get("/")
def index():
    return redirect("/01-overview.html")


@app.get("/spaces")
def list_spaces():
    rows = get_db().execute("SELECT * FROM Spaces ORDER BY space_id")
    return jsonify([{**dict(r), "is_active": bool(r["is_active"])} for r in rows])


@app.get("/computers")
def list_computers():
    rows = get_db().execute("SELECT * FROM Computers ORDER BY computer_id")
    return jsonify([dict(r) for r in rows])


@app.get("/equipment")
def list_equipment():
    rows = get_db().execute("SELECT * FROM Equipment ORDER BY equipment_id")
    return jsonify([dict(r) for r in rows])


@app.get("/time-blocks")
def list_time_blocks():
    day = parse_date(request.args.get("date"))
    if day is None:
        return error(400, "INVALID_DATE", "Choose a valid date.")
    blocks = []
    for hour in START_HOURS:
        start, end = block_times(day, hour)
        blocks.append(
            {
                "date": day.isoformat(),
                "start_hour": hour,
                "end_hour": hour + 2,
                "start_time": start.isoformat(),
                "end_time": end.isoformat(),
            }
        )
    return jsonify(blocks)


@app.get("/availability")
def availability():
    day = parse_date(request.args.get("date"))
    if day is None:
        return error(400, "INVALID_DATE", "Choose a valid date.")
    hour = request.args.get("start_hour", type=int)
    if hour not in START_HOURS:
        return error(400, "INVALID_BLOCK", "Choose one of the available time blocks.")
    start, _ = block_times(day, hour)
    db = get_db()
    space_ids = [
        r["space_id"]
        for r in db.execute(
            """SELECT space_id FROM Spaces
               WHERE is_active = 1 AND space_id NOT IN (
                 SELECT space_id FROM Reservations
                 WHERE status = 'CONFIRMED' AND start_time = ?)
               ORDER BY space_id""",
            (db_time(start),),
        )
    ]
    equipment_ids = [
        r["equipment_id"]
        for r in db.execute(
            """SELECT equipment_id FROM Equipment
               WHERE status != 'MAINTENANCE' AND status != 'OFFLINE' AND equipment_id NOT IN (
                 SELECT re.equipment_id FROM ReservationEquipment re
                 JOIN Reservations r ON r.reservation_id = re.reservation_id
                 WHERE r.status = 'CONFIRMED' AND r.start_time = ?)
               ORDER BY equipment_id""",
            (db_time(start),),
        )
    ]
    return jsonify(space_ids=space_ids, equipment_ids=equipment_ids)


@app.get("/reservations")
def list_reservations():
    sql = "SELECT * FROM Reservations WHERE 1 = 1"
    params = []
    if "user_id" in request.args:
        sql += " AND user_name = ?"
        params.append(request.args["user_id"])
    if "space_id" in request.args:
        space_id = request.args.get("space_id", type=int)
        if space_id is None or space_id < 1:
            return error(400, "INVALID_FILTER", "Check the reservation filters and try again.")
        sql += " AND space_id = ?"
        params.append(space_id)
    sql += " ORDER BY created_at DESC"
    db = get_db()
    return jsonify([reservation_json(db, r) for r in db.execute(sql, params).fetchall()])


@app.post("/reservations")
def create_reservation():
    body = request.get_json(silent=True) or {}
    user_id = body.get("user_id")
    space_id = body.get("space_id")
    equipment_ids = body.get("equipment_ids", [])
    day = parse_date(body.get("date"))
    hour = body.get("start_hour")

    if not isinstance(user_id, str) or not user_id or not isinstance(space_id, int) or day is None:
        return error(400, "INVALID_REQUEST", "Check the reservation details and try again.")
    if hour not in START_HOURS:
        return error(400, "INVALID_BLOCK", "Choose one of the available time blocks.")
    if not isinstance(equipment_ids, list) or len(set(equipment_ids)) != len(equipment_ids):
        return error(400, "INVALID_REQUEST", "Check the reservation details and try again.")

    start, end = block_times(day, hour)
    if start <= datetime.now():
        return error(400, "BLOCK_STARTED", "Choose a time block that has not started yet.")

    db = get_db()
    # BEGIN IMMEDIATE takes the write lock before checking, so two requests
    # cannot both pass the availability checks for the same block.
    db.execute("BEGIN IMMEDIATE")
    try:
        space = db.execute("SELECT is_active FROM Spaces WHERE space_id = ?", (space_id,)).fetchone()
        if space is None:
            db.execute("ROLLBACK")
            return error(404, "SPACE_NOT_FOUND", "That space could not be found.")
        if not space["is_active"]:
            db.execute("ROLLBACK")
            return error(409, "SPACE_INACTIVE", "This space is not available for new bookings.")

        for equipment_id in equipment_ids:
            if db.execute("SELECT 1 FROM Equipment WHERE equipment_id = ?", (equipment_id,)).fetchone() is None:
                db.execute("ROLLBACK")
                return error(404, "EQUIPMENT_NOT_FOUND", "That equipment item could not be found.")

        booked_space = db.execute(
            "SELECT 1 FROM Reservations WHERE space_id = ? AND start_time = ? AND status = 'CONFIRMED'",
            (space_id, db_time(start)),
        ).fetchone()
        if booked_space:
            db.execute("ROLLBACK")
            return error(
                409,
                "SPACE_BOOKED",
                "This space is already booked during your selected time. Choose another space or time.",
            )

        if equipment_ids:
            placeholders = ",".join("?" * len(equipment_ids))
            booked_item = db.execute(
                f"""SELECT 1 FROM ReservationEquipment re
                    JOIN Reservations r ON r.reservation_id = re.reservation_id
                    WHERE r.status = 'CONFIRMED' AND r.start_time = ?
                      AND re.equipment_id IN ({placeholders})""",
                (db_time(start), *equipment_ids),
            ).fetchone()
            if booked_item:
                db.execute("ROLLBACK")
                return error(409, "EQUIPMENT_UNAVAILABLE", "This equipment is unavailable during your selected time.")

        cursor = db.execute(
            """INSERT INTO Reservations (user_name, space_id, start_time, end_time, status, created_at)
               VALUES (?, ?, ?, ?, 'CONFIRMED', ?)""",
            (user_id, space_id, db_time(start), db_time(end), db_time(datetime.now())),
        )
        reservation_id = cursor.lastrowid
        db.executemany(
            "INSERT INTO ReservationEquipment (reservation_id, equipment_id) VALUES (?, ?)",
            [(reservation_id, e) for e in equipment_ids],
        )
        db.execute("COMMIT")
    except sqlite3.Error:
        db.execute("ROLLBACK")
        return error(500, "SAVE_FAILED", "We couldn't complete your reservation. Please try again.")

    row = db.execute("SELECT * FROM Reservations WHERE reservation_id = ?", (reservation_id,)).fetchone()
    return jsonify(reservation_json(db, row)), 201


@app.get("/reservations/<int:reservation_id>")
def get_reservation(reservation_id):
    db = get_db()
    row = db.execute("SELECT * FROM Reservations WHERE reservation_id = ?", (reservation_id,)).fetchone()
    if row is None:
        return error(404, "RESERVATION_NOT_FOUND", "That reservation could not be found.")
    return jsonify(reservation_json(db, row))


@app.post("/reservations/<int:reservation_id>/cancel")
def cancel_reservation(reservation_id):
    db = get_db()
    row = db.execute("SELECT * FROM Reservations WHERE reservation_id = ?", (reservation_id,)).fetchone()
    if row is None:
        return error(404, "RESERVATION_NOT_FOUND", "That reservation could not be found.")
    if row["status"] != "CANCELLED":
        if datetime.fromisoformat(row["end_time"]) <= datetime.now():
            return error(409, "BOOKING_ENDED", "This reservation has already ended.")
        db.execute("UPDATE Reservations SET status = 'CANCELLED' WHERE reservation_id = ?", (reservation_id,))
        row = db.execute("SELECT * FROM Reservations WHERE reservation_id = ?", (reservation_id,)).fetchone()
    return jsonify(reservation_json(db, row))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
