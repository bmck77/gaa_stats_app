# gaa_stats_app
This is a repository to store the code and dependencies of a GAA stats-taking app.

The app records the following in a Gaelic Football match:

1. Score
2. Scorers
3. Assistors
4. Timeline

**Scaffold:** Python with a Streamlit frontend.

**Prerequisites**
- Python 3.10+ installed
- PowerShell (Windows) or a POSIX shell

**Quick setup (Windows PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

**Quick setup (cmd.exe)**

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
streamlit run app.py
```

**Notes**
- The main Streamlit app is `app.py`.
- Edit `requirements.txt` to add more dependencies.

If you want, I can also create a `.gitignore`, add CI, or expand the app features (persistence, authentication, UI improvements).

**Client (React + Capacitor-ready)**

I scaffolded a minimal React client in `client/` that provides the same features as the Streamlit prototype but is Capacitor-ready for building an offline-capable APK using on-device SQLite and file export.

- See `client/README.md` for development and Capacitor instructions.
- `client/src/db.js` currently uses `localStorage`. Swap to `@capacitor-community/sqlite` when packaging the native app.

