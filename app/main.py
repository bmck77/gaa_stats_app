"""Kivy mobile app for GAA Stats.

Features:
- Record events (team, minute, player, assistor, type)
- Persist events using on-device SQLite (stored in `user_data_dir`)
- Export stored events to CSV file
- Simple match timer with start/stop/reset

This app is intended to be packaged to Android using Buildozer.
"""

import os
import sqlite3
import csv
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window


class GAAApp(App):
    def build(self):
        self.title = "GAA Stats"
        self.db_path = os.path.join(self.user_data_dir, "events.db")
        os.makedirs(self.user_data_dir, exist_ok=True)
        self.init_db()

        root = BoxLayout(orientation="vertical", padding=8, spacing=8)

        # Top: Timer
        timer_box = BoxLayout(size_hint_y=None, height=60, spacing=8)
        self.timer_label = Label(text="00:00", font_size=32)
        timer_box.add_widget(self.timer_label)
        btn_start = Button(text="Start", on_release=self.start_timer)
        btn_stop = Button(text="Stop", on_release=self.stop_timer)
        btn_reset = Button(text="Reset", on_release=self.reset_timer)
        timer_box.add_widget(btn_start)
        timer_box.add_widget(btn_stop)
        timer_box.add_widget(btn_reset)
        root.add_widget(timer_box)

        # Middle: form to add event
        form = GridLayout(cols=2, size_hint_y=None, height=220, spacing=6)
        form.add_widget(Label(text="Team"))
        self.team_in = TextInput(text="Home")
        form.add_widget(self.team_in)
        form.add_widget(Label(text="Minute"))
        self.minute_in = TextInput(text="1", input_filter='int')
        form.add_widget(self.minute_in)
        form.add_widget(Label(text="Player"))
        self.player_in = TextInput()
        form.add_widget(self.player_in)
        form.add_widget(Label(text="Assistor"))
        self.assistor_in = TextInput()
        form.add_widget(self.assistor_in)
        form.add_widget(Label(text="Type"))
        self.type_in = TextInput(text="Point")
        form.add_widget(self.type_in)

        add_btn = Button(text="Add Event", size_hint_y=None, height=40)
        add_btn.bind(on_release=self.add_event_handler)

        root.add_widget(form)
        root.add_widget(add_btn)

        # Events list
        self.events_container = GridLayout(cols=1, size_hint_y=None, spacing=4)
        self.events_container.bind(minimum_height=self.events_container.setter('height'))
        scroll = ScrollView()
        scroll.add_widget(self.events_container)
        root.add_widget(scroll)

        # Bottom actions
        actions = BoxLayout(size_hint_y=None, height=48, spacing=8)
        btn_export = Button(text="Export CSV")
        btn_export.bind(on_release=self.export_csv)
        btn_clear = Button(text="Clear Events")
        btn_clear.bind(on_release=self.clear_events)
        actions.add_widget(btn_export)
        actions.add_widget(btn_clear)
        root.add_widget(actions)

        # Timer state
        self._timer_seconds = 0
        self._timer_ev = None

        # Load existing events
        self.reload_events()

        return root

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team TEXT,
                minute INTEGER,
                player TEXT,
                assistor TEXT,
                type TEXT,
                created_at TEXT
            )
            """
        )
        conn.commit()
        conn.close()

    def add_event_handler(self, instance):
        team = self.team_in.text.strip() or 'Home'
        minute = int(self.minute_in.text) if self.minute_in.text.isdigit() else 0
        player = self.player_in.text.strip()
        assistor = self.assistor_in.text.strip()
        typev = self.type_in.text.strip() or 'Point'
        if not player:
            return
        self.add_event(team, minute, player, assistor, typev)
        self.player_in.text = ''
        self.assistor_in.text = ''
        self.reload_events()

    def add_event(self, team, minute, player, assistor, typev):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO events (team, minute, player, assistor, type, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (team, minute, player, assistor, typev, datetime.utcnow().isoformat()),
        )
        conn.commit()
        conn.close()

    def get_events(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT id, team, minute, player, assistor, type FROM events ORDER BY minute")
        rows = cur.fetchall()
        conn.close()
        return rows

    def reload_events(self):
        self.events_container.clear_widgets()
        rows = self.get_events()
        if not rows:
            self.events_container.add_widget(Label(text="No events yet"))
            return
        for r in rows:
            id_, team, minute, player, assistor, typev = r
            txt = f"{minute}' {team} — {player} ({typev}) {('Assist: ' + assistor) if assistor else ''}"
            self.events_container.add_widget(Label(text=txt, size_hint_y=None, height=30))

    def export_csv(self, instance):
        rows = self.get_events()
        if not rows:
            return
        out_path = os.path.join(self.user_data_dir, f"events_{int(datetime.utcnow().timestamp())}.csv")
        with open(out_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['team', 'minute', 'player', 'assistor', 'type'])
            for r in rows:
                _, team, minute, player, assistor, typev = r
                writer.writerow([team, minute, player, assistor, typev])
        # On Android you may want to move this file to Downloads or use plyer to share it.
        print('Exported CSV to', out_path)

    def clear_events(self, instance):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM events")
        conn.commit()
        conn.close()
        self.reload_events()

    # Timer methods
    def _tick(self, dt):
        self._timer_seconds += 1
        mins = self._timer_seconds // 60
        secs = self._timer_seconds % 60
        self.timer_label.text = f"{mins:02d}:{secs:02d}"

    def start_timer(self, instance):
        if self._timer_ev is None:
            self._timer_ev = Clock.schedule_interval(self._tick, 1.0)

    def stop_timer(self, instance):
        if self._timer_ev is not None:
            self._timer_ev.cancel()
            self._timer_ev = None

    def reset_timer(self, instance):
        self.stop_timer(instance)
        self._timer_seconds = 0
        self.timer_label.text = "00:00"


if __name__ == '__main__':
    # Increase window size for desktop testing
    Window.size = (360, 740)
    GAAApp().run()
