from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI()

# 📦 DB
conn = sqlite3.connect("hives.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS records (
    hive INTEGER,
    text TEXT,
    score INTEGER,
    time TEXT
)
""")
conn.commit()


# 🧠 оценка улья
def score(text: str):
    t = text.lower()
    s = 50

    if "расплод" in t:
        s += 15
    if "мёд" in t or "мед" in t:
        s += 10
    if "агресс" in t:
        s -= 25

    return max(0, min(100, s))


# 📩 модель входа (ВАЖНО)
class Item(BaseModel):
    hive: int
    text: str


@app.get("/")
def root():
    return {"status": "ok", "service": "bee-api 🐝"}


@app.post("/add")
def add(item: Item):
    s = score(item.text)

    cur.execute(
        "INSERT INTO records VALUES (?, ?, ?, ?)",
        (item.hive, item.text, s, datetime.now().isoformat())
    )
    conn.commit()

    return {
        "hive": item.hive,
        "score": s,
        "text": item.text,
        "advice": [
            "📊 оценка рассчитана",
            "🐝 состояние зафиксировано"
        ]
    }


@app.get("/hives")
def get_hives():
    cur.execute("SELECT hive, score FROM records ORDER BY rowid DESC")
    return cur.fetchall()
