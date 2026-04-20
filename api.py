from fastapi import FastAPI

app = FastAPI()

db = []

def analyze(text: str):
    t = text.lower()

    score = 60
    advice = []

    # 📌 расплод
    if "расплод" in t:
        score += 20
    else:
        score -= 15
        advice.append("⚠️ мало расплода — проверь развитие семьи")

    # 📌 мёд
    if "мёд" in t:
        score += 15
    else:
        score -= 10
        advice.append("🍯 запасы мёда слабые")

    # 📌 матка
    if "матка" in t:
        if "нет" in t:
            score -= 40
            advice.append("🚨 нет матки — критично")
        else:
            score += 15

    # 📌 агрессия / риск
    if "злая" in t or "агрессив" in t:
        score -= 10
        advice.append("🐝 повышенная агрессия — возможен стресс")

    # 📊 финальная оценка
    if score >= 80:
        advice.append("🟢 сильная и стабильная семья")
    elif score >= 60:
        advice.append("🟡 нормальное состояние, но нужен контроль")
    elif score >= 40:
        advice.append("🟠 ослабление семьи")
    else:
        advice.append("🔴 критическое состояние — срочное вмешательство")

    return max(0, min(100, score)), advice


@app.get("/")
def root():
    return {"status": "bee-api running"}

@app.post("/add")
def add(hive: int, text: str):
    score, advice = analyze(text)

    db.append({
        "hive": hive,
        "text": text,
        "score": score
    })

    return {
        "hive": hive,
        "score": score,
        "advice": advice
    }

@app.get("/hives")
def hives():
    return db
