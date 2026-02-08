# GAA Stats client

This is a minimal React (Vite) client intended to be wrapped with Capacitor for offline-capable Android/iOS apps.

Quick start

```bash
cd client
npm install
npm run dev   # local development (browser)
npm run build # produce static assets for Capacitor
```

Capacitor steps (high-level)

```bash
# from project root or client folder
npm install @capacitor/core @capacitor/cli
# optional native plugins: sqlite, filesystem, share
npm install @capacitor-community/sqlite @capacitor/filesystem @capacitor/share
npx cap init # follow prompts (app name and id)
# build web assets
npm run build
npx cap copy
npx cap add android
npx cap open android
# then build APK inside Android Studio or via Gradle
```

Notes
- The current `db.js` uses `localStorage` for simplicity. When running inside Capacitor with the SQLite plugin installed, replace `db.js` with a native-backed implementation that uses `@capacitor-community/sqlite`.
- `exportToCsv` writes a CSV file for sharing/downloading in the browser; on device you can write files using Capacitor Filesystem or Share plugin.
