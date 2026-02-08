
# gaa_stats_app

This repository contains a Python mobile app scaffold using Kivy and an optional FastAPI backend for syncing/exporting events.

Features:
- Record match events (team, minute, player, assistor, type)
- On-device persistence with SQLite
- Export events to CSV
- Built-in match timer (start/stop/reset)
- Optional FastAPI backend for syncing and CSV download

Layout:
- `app/` — Kivy app source (app/app.py)
- `backend/` — FastAPI backend (backend/api.py)
- `buildozer.spec` — configuration to build an Android APK using Buildozer
- `requirements.txt` — consolidated project dependencies

Run locally (desktop) for testing:

```bash
python -m venv .venv
# Activate the virtualenv (Linux/macOS)
. .venv/bin/activate
# Windows PowerShell:
# .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Run the Kivy app (default entrypoint)
python main.py --mode app
```

Run the backend locally:

```bash
# from repository root
pip install -r requirements.txt
# run with uvicorn
python main.py --mode backend
```

Build APK (Linux / WSL recommended)

- Install Buildozer (on Ubuntu) or use the official `kivy/buildozer` Docker image. Building on macOS/Windows directly is not recommended.

Example (WSL / Linux):

```bash
sudo apt update && sudo apt install -y buildozer python3-pip python3-virtualenv
pip install --user --upgrade buildozer
# from repository root
buildozer -v android debug
# generated apk will be in bin/ after successful build
```

Example (Docker):

```bash
docker run --rm -v "$(pwd):/home/user/hostcwd" -w /home/user/hostcwd kivy/buildozer buildozer android debug
```

Notes
- The SQLite DB is stored in the app `user_data_dir` on device. The app writes exported CSV files into the same directory. On Android you may want to move or share them with `plyer` or use the Android API.
- If you want Play Store release builds you'll need to generate a signing key and build a signed release APK (see Buildozer docs).

Backend (FastAPI)

The backend (optional) exposes the following endpoints:

- `POST /events` — accept a JSON array of events to store
- `GET /events` — return stored events as JSON
- `GET /events.csv` — download CSV of stored events

Run the backend locally with `python main.py --mode backend` or via `uvicorn backend.api:app --reload`.

Sync `buildozer.spec` requirements from `requirements.txt`

If you update the top-level `requirements.txt`, keep `buildozer.spec` in sync by running:

```bash
python scripts/sync_buildozer_requirements.py
```

This will update the `requirements = ...` line in `buildozer.spec` with a best-effort
selection of mobile-relevant packages (e.g. `kivy`, `plyer`). Review `buildozer.spec`
before building to ensure it contains the packages you need on Android.

If you'd like, I can:
- add `plyer` sharing for exported CSVs to place files into Downloads or invoke the Android share sheet,
- add a `.kv` layout and assets for a nicer UI,
- add CI scripts for Docker-based Buildozer builds.

