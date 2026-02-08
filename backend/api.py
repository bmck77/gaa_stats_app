"""GAA Stats backend service.

This FastAPI application stores match events in a local SQLite database,
provides endpoints to POST/GET events, and serves a CSV export.

Files:
- `data.db` (created at runtime) — SQLite storage for events.
Endpoints:
- `POST /events` accepts a JSON array of events to store.
- `GET /events` returns stored events as JSON.
- `GET /events.csv` returns a CSV download of events.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
import os
from fastapi.responses import StreamingResponse, JSONResponse
import csv
import io

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'data.db')

app = FastAPI(title="GAA Stats Backend")


class Event(BaseModel):
    """Pydantic model describing a single match event.

    Fields:
    - team: 'Home' or 'Away'
    - minute: minute in match
    - player: player name
    - assistor: optional assistor name
    - type: 'Point' or 'Goal'
    """
    team: str
    minute: int
    player: str
    assistor: str = ""
    type: str


def init_db():
    """Initialize the SQLite database and create the `events` table if missing."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team TEXT,
            minute INTEGER,
            player TEXT,
            assistor TEXT,
            type TEXT
        )
        """
    )
    conn.commit()
    conn.close()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health():
    """Simple health check endpoint."""
    return {"status": "ok"}


@app.post("/events")
def post_events(events: List[Event]):
    """Accept and store a list of events.

    Returns the number of inserted rows.
    """
    if not events:
        raise HTTPException(status_code=400, detail="No events provided")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for e in events:
        cur.execute(
            "INSERT INTO events (team, minute, player, assistor, type) VALUES (?, ?, ?, ?, ?)",
            (e.team, e.minute, e.player, e.assistor, e.type),
        )
    conn.commit()
    conn.close()
    return {"inserted": len(events)}


@app.get("/events")
def get_events():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, team, minute, player, assistor, type FROM events ORDER BY minute")
    rows = cur.fetchall()
    conn.close()
    events = [
        {"id": r[0], "team": r[1], "minute": r[2], "player": r[3], "assistor": r[4], "type": r[5]}
        for r in rows
    ]
    return JSONResponse(content=events)


@app.get("/events.csv")
def get_events_csv():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT team, minute, player, assistor, type FROM events ORDER BY minute")
    rows = cur.fetchall()
    conn.close()

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["team", "minute", "player", "assistor", "type"])
    for r in rows:
        writer.writerow(r)
    buffer.seek(0)
    return StreamingResponse(buffer, media_type='text/csv', headers={"Content-Disposition": "attachment; filename=events.csv"})
