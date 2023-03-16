from datetime import datetime
from flask import abort, make_response,jsonify

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

EVENT = {
    "1000": {
        "title": "New Light",
        "event_id": "1000",
        "body": "Introduction quest",
        "timestamp": get_timestamp(),
        "active": False
    },
    "2000": {
        "title": "Old Light",
        "event_id": "2000",
        "body": "Raid Quest",
        "timestamp": get_timestamp(),
        "active": False
    },
    "3000": {
        "title": "Faded Light",
        "event_id": "3000",
        "body": "Endgame grinding",
        "timestamp": get_timestamp(),
        "active": True
    }
}

def read_all():
    return jsonify(list(EVENT.values()))


def create(event):
    event_id = event.get("event_id")
    event_title = event.get("event_title", "") 
    event_body = event.get("event_body", "")


    if  event_id and event_id  not in EVENT :
        EVENT[event_id] = {
            "event_id": event_id,
            "title": event_title,
            "body": event_body,
            "timestamp": get_timestamp(),
            "active": False
        }
        return EVENT[event_id], 201
    else:
        abort(
            406,
            f"Event with id {event_id} already exists",
        )


def read_one(event_id):
    if event_id in EVENT:
        return EVENT[event_id]
    else:
        abort(
            404, f"Event with ID {event_id} not found"
        )


def update(event_id, event):
    if event_id in EVENT:
        EVENT[event_id]["title"] = event.get("event_title", EVENT[event_id]["title"])
        EVENT[event_id]["body"] = event.get("event_body", EVENT[event_id]["body"])

        EVENT[event_id]["timestamp"] = get_timestamp()
        return EVENT[event_id]
    else:
        abort(
            404,
            f"Event with ID {event_id} not found"
        )


def delete(event_id):
    if event_id in EVENT:
        del EVENT[event_id]
        return make_response(
            f"{event_id} successfully deleted", 200
        )
    else:
        abort(
            404,
            f"Event with ID {event_id} not found"
        )