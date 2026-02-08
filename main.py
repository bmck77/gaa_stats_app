"""Unified entry point for the repository.

Usage:
  python main.py            # default: run the Kivy app (used by Buildozer)
  python main.py --mode app # run the Kivy app
  python main.py --mode backend  # run the FastAPI backend (uvicorn)
  python main.py --mode both     # start backend in subprocess, then run app

Default mode is `app` so that APK builds using Buildozer pick up the Kivy
application automatically.
"""
import argparse
import sys
import subprocess


def run_app():
    # Import and run the Kivy application
    from app.app import GAAApp

    GAAApp().run()


def run_backend():
    # Run uvicorn programmatically if available, otherwise fallback to
    # running via `python -m uvicorn` so reload and other options work.
    try:
        import uvicorn

        uvicorn.run("backend.api:app", host="0.0.0.0", port=8000)
    except Exception:
        # Fallback: spawn as module in a subprocess
        cmd = [sys.executable, "-m", "uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
        subprocess.check_call(cmd)


def run_both():
    # Start backend as subprocess, then start app in this process.
    proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"])
    try:
        run_app()
    finally:
        proc.terminate()
        proc.wait()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=("app", "backend", "both"), default="app")
    args = p.parse_args()

    if args.mode == "app":
        run_app()
    elif args.mode == "backend":
        run_backend()
    else:
        run_both()


if __name__ == "__main__":
    main()
