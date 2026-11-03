# RoomService Developer Guide

## 1. Overview

`RoomService` provides atomic operations for managing room occupancy in the Hostel Management System.

It supports:
- Reserving one bed in a room.
- Releasing one occupied bed.
- Preventing occupancy from exceeding room capacity.
- Preventing occupancy from becoming negative.

## 2. Service Imports

Import the service and its exceptions from `rooms.services`:

```python
from rooms.services import (
    RoomService,
    RoomServiceError,
    RoomNotFoundError,
    RoomFullError,
    RoomNotOccupiedError,
)
```

## 3. Method Contract

### 3.1 reserve_bed(room_id)

- **Purpose:** Reserve one bed if the room has available capacity.
- **Parameter:** `room_id`, the room's primary key.
- **Behavior:** Atomically increments `occupied_count` by one.
- **Return value:** Updated `Room` model instance.
- **Exceptions:**
  - `RoomNotFoundError`: Room does not exist.
  - `RoomFullError`: Room has no available beds.

### 3.2 release_bed(room_id)

- **Purpose:** Release one occupied bed.
- **Parameter:** `room_id`, the room's primary key.
- **Behavior:** Atomically decrements `occupied_count` by one.
- **Return value:** Updated `Room` model instance.
- **Exceptions:**
  - `RoomNotFoundError`: Room does not exist.
  - `RoomNotOccupiedError`: Room has no occupied beds.

## 4. Exception Contract

All service exceptions inherit from `RoomServiceError`.

| Exception | Meaning |
|---|---|
| `RoomServiceError` | Base exception |
| `RoomNotFoundError` | Room does not exist |
| `RoomFullError` | No available beds |
| `RoomNotOccupiedError` | No occupied beds to release |

## 5. Allocation Developer Usage Example

The following example demonstrates how an allocation developer can reserve a bed and handle service exceptions.

```python
from rooms.services import (
    RoomService,
    RoomServiceError,
    RoomNotFoundError,
    RoomFullError,
)

def allocate_student_to_room(room_id):
    try:
        room = RoomService.reserve_bed(room_id)

        return {
            "success": True,
            "room_id": room.id,
            "occupied_count": room.occupied_count,
            "available_beds": room.available_beds,
        }

    except RoomNotFoundError:
        return {"success": False, "message": "Room not found."}

    except RoomFullError:
        return {"success": False, "message": "Room is full."}

    except RoomServiceError:
        return {"success": False, "message": "Allocation failed."}
```

### Releasing a bed

```python
from rooms.services import (
    RoomService,
    RoomNotFoundError,
    RoomNotOccupiedError,
)

def release_student_room(room_id):
    try:
        room = RoomService.release_bed(room_id)

        return {
            "success": True,
            "room_id": room.id,
            "occupied_count": room.occupied_count,
            "available_beds": room.available_beds,
        }

    except RoomNotFoundError:
        return {"success": False, "message": "Room not found."}

    except RoomNotOccupiedError:
        return {"success": False, "message": "No occupied beds."}
```

## 6. Transaction and Concurrency

Both `reserve_bed()` and `release_bed()` use Django's `transaction.atomic`.

- Database-side `F()` expressions update occupancy.
- Conditional updates prevent occupancy from exceeding room capacity.
- Conditional updates prevent occupancy from falling below zero.
- Successful operations return the updated room instance.
- Failed operations raise the documented exceptions.

## 7. Developer Guidelines

1. Use `RoomService.reserve_bed(room_id)` for bed allocation.
2. Use `RoomService.release_bed(room_id)` for bed release.
3. Do not directly modify `occupied_count` in allocation logic.
4. Handle the documented service exceptions.
5. Use the returned room instance to access updated occupancy and available beds.

## 8. Source Implementation

The service implementation is maintained in `rooms/services.py`.

This guide documents the existing RoomService contract for developers integrating room allocation and occupancy management.