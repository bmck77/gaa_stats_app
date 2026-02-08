[app]
title = GAA Stats
package.name = gaa_stats
package.domain = org.example
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
# Buildozer requires a comma-separated `requirements` listing for Android.
# Keep this in sync with `requirements.txt` above (kivy and plyer are required
# for the mobile build). The top-level `requirements.txt` may also be used
# for local development installs: `pip install -r requirements.txt`.
requirements = python3,kivy,plyer
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
