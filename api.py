from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()


class Item(BaseModel):
    hive: int
    text: str


def analyze(text: str):
    t = text.lower()

    score = 50
    advice = []

    # --- здоровье семьи ---
    if "расплод" in t:
        score += 20
    if "мёд" in t or "мед" in t:
        score += 10
    if "сильный" in t:
        score += 10

    if "агресс" in t or "злые" in t:
        score -= 25
        advice.append("⚠️ Пчёлы агрессивны — не тревожить часто")

    if "пусто" in t:
        score -= 15
        advice.append("🍂 Мало ресурсов — нужен контроль кормовой базы")

    # --- границы ---
    score = max(0, min(100, score))

    # --- интерпретация ---
    if score >= 80:
        advice.append("🟢 Сильная семья — можно расширять улей")
    elif score >= 50:
        advice.append("🟡 Среднее состояние — наблюдать")
    else:
        advice.append("🔴 Ослабленная семья — нужна помощь")

    return score, advice


@app.get("/")
def root():
    return {"status": "ok", "service": "bee-api 🐝"}


@app.post("/add")
def add(item: Item):
    score, advice = analyze(item.text)

    return {
        "ok": True,
        "hive": item.hive,
        "text": item.text,
        "score": score,
        "advice": advice,
        "time": datetime.now().isoformat()
    }
