"""
Nova OS
Author: Tanju Aksit
Copyright (c) 2026 Tanju Aksit

This source code is licensed under the Nova OS Author Credit License.
"""

import sqlite3
from datetime import datetime
from config.paths import DB_PATH
from config.loader import config


class EventMemory:  # <--- Sınıf adı EventMemory olarak güncellendi!

    def __init__(self, brain=None):
        self.brain = brain
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            action TEXT,
            target TEXT,
            timestamp TEXT
        )
        """)

        self.conn.commit()

    def add_event(self, subject, action, target=None):
        ts = datetime.now().isoformat()
        self.cursor.execute(
            "INSERT INTO events (subject, action, target, timestamp) VALUES (?, ?, ?, ?)",
            (subject, action, target, ts)
        )
        self.conn.commit()

    def get_recent_events(self, subject=None, limit=5):
        if subject is None:
            subject = config.get("name", "User")

        self.cursor.execute("""
        SELECT subject, action, target, timestamp
        FROM events
        WHERE subject=?
        ORDER BY id DESC
        LIMIT ?
        """, (subject, limit))

        return self.cursor.fetchall()

    def search_events(self, keyword):
        self.cursor.execute("""
        SELECT subject, action, target, timestamp
        FROM events
        WHERE action LIKE ?
        ORDER BY id DESC
        LIMIT 5
        """, (f"%{keyword}%",))

        return self.cursor.fetchall()