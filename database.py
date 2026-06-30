# database.py
import sqlite3

class Database:
    def __init__(self, db_name="love_journal.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """ডাটাবেস টেবিল তৈরি করার লজিক (ইমোশন ও সেন্টিমেন্ট স্কোর কলামসহ)"""
        query = """
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            text_entry TEXT,
            location TEXT,
            status TEXT,
            image_name TEXT,
            sentiment_score REAL DEFAULT 0.0,
            emotion TEXT DEFAULT 'Neutral',
            tags TEXT,
            weather TEXT
        );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def insert_entry(self, date, text, location, status, image_name, sentiment_score, emotion, tags, weather):
        """নতুন মেমোরি ডেটাবেসে সেভ করার ফাংশন"""
        query = """
        INSERT INTO journal (date, text_entry, location, status, image_name, sentiment_score, emotion, tags, weather)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        self.cursor.execute(query, (date, text, location, status, image_name, sentiment_score, emotion, tags, weather))
        self.conn.commit()

    def fetch_all_entries(self):
        """টাইমলাইন ও চার্টের জন্য ডাটাবেস থেকে সব মেমোরি রিড করার ফাংশন"""
        self.cursor.execute("SELECT * FROM journal")
        rows = self.cursor.fetchall()
        
        # ডাটাবেসের র ডেটাকে ডিকশনারি ফরম্যাটে কনভার্ট করা যাতে app.py সহজে বুঝতে পারে
        memories = []
        for row in rows:
            memories.append({
                "id": row[0],
                "date": row[1],
                "text_entry": row[2],
                "location": row[3],
                "status": row[4],
                "image_name": row[5],
                "sentiment_score": row[6],
                "emotion": row[7],
                "tags": row[8],
                "weather": row[9]
            })
        return memories

    def __del__(self):
        self.conn.close()