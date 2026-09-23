# Esports Reservation System (Sample Data)

Sample payloads for each table using the schema’s field names, integer IDs, and ISO 8601 timestamps.

---

### 1: Spaces

```json
[
  {
    "space_id": 1,
    "space_name": "Station 01 - Cyberhound Rig",
    "description": "PC gaming station with a 240Hz monitor.",
    "is_active": true
  },
  {
    "space_id": 2,
    "space_name": "Station 02 - Cyberhound Rig",
    "description": "PC gaming station with a 165Hz monitor.",
    "is_active": true
  }
]
```

---

### 2: Computers

```json
[
  {
    "computer_id": 1,
    "space_id": 1,
    "hostname": "CH-RIG-01",
    "specs": "Intel Core i7-13700K, RTX 4080, 32GB DDR5 RAM, 1TB NVMe SSD, 240Hz Monitor",
    "status": "AVAILABLE"
  },
  {
    "computer_id": 2,
    "space_id": 2,
    "hostname": "CH-RIG-02",
    "specs": "AMD Ryzen 7 7800X3D, RTX 4070 Ti, 32GB DDR5 RAM, 2TB NVMe SSD, 165Hz Monitor",
    "status": "AVAILABLE"
  }
]
```

---

### 3: Equipment

```json
[
  {
    "equipment_id": 1,
    "item_name": "Logitech G Pro X Wireless Headset #1",
    "category": "HEADSET",
    "serial_number": "MOCK-HEADSET-001",
    "status": "AVAILABLE"
  },
  {
    "equipment_id": 2,
    "item_name": "Xbox Elite Wireless Controller #1",
    "category": "CONTROLLER",
    "serial_number": "MOCK-CONTROLLER-001",
    "status": "AVAILABLE"
  }
]
```

---

### 4: Reservations

```json
[
  {
    "reservation_id": 8801,
    "user_id": "usr_001",
    "space_id": 1,
    "start_time": "2026-09-23T14:00:00Z",
    "end_time": "2026-09-23T16:00:00Z",
    "status": "CONFIRMED",
    "created_at": "2026-09-22T18:30:00Z"
  },
  {
    "reservation_id": 8802,
    "user_id": "usr_002",
    "space_id": 2,
    "start_time": "2026-09-23T17:00:00Z",
    "end_time": "2026-09-23T19:00:00Z",
    "status": "CONFIRMED",
    "created_at": "2026-09-22T20:15:00Z"
  }
]
```

---

### 5: ReservationEquipment

```json
[
  {
    "reservation_id": 8801,
    "equipment_id": 1
  },
  {
    "reservation_id": 8801,
    "equipment_id": 2
  },
  {
    "reservation_id": 8802,
    "equipment_id": 2
  }
]
```
