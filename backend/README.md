# GAA Stats Backend

This is a minimal FastAPI backend used for syncing events and serving CSV exports.

Run locally (recommended during development):

```bash
python -m venv .venv
. .venv/bin/activate   # or .\.venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Docker:

```bash
docker build -t gaa-stats-backend .
docker run -p 8000:8000 gaa-stats-backend
```

Endpoints:
- `POST /events` — accept a JSON array of events to store
- `GET /events` — return stored events as JSON
- `GET /events.csv` — download CSV of stored events
