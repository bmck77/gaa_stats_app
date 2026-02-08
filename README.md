# gaa_stats_app
This repository now contains a Python-only mobile app scaffold using Kivy.

Features:
- Record match events (team, minute, player, assistor, type)
- On-device persistence with SQLite
- Export events to CSV
- Built-in match timer (start/stop/reset)

Layout:
- `app/` — Kivy app source and `requirements.txt`
- `buildozer.spec` — configuration to build an Android APK using Buildozer

Run locally (desktop) for testing:

```bash
python -m venv .venv
source .venv/bin/activate   # on Windows use .\.venv\Scripts\Activate.ps1
pip install -r app/requirements.txt
python app/main.py
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

If you want, I can:
- replace the simple CSV export with `plyer` sharing to put the CSV into Downloads or invoke the Android share sheet,
- add a nicer Kivy layout with `.kv` language and icons,
- add CI instructions for building with Docker.

**Client (React + Capacitor-ready)**

I scaffolded a minimal React client in `client/` that provides the same features as the Streamlit prototype but is Capacitor-ready for building an offline-capable APK using on-device SQLite and file export.

- See `client/README.md` for development and Capacitor instructions.
- `client/src/db.js` currently uses `localStorage`. Swap to `@capacitor-community/sqlite` when packaging the native app.

