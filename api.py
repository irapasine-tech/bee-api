from fastapi import FastAPI

app = FastAPI()

db = []

def analyze(text: str):
    score = 50
    advice = []

    t = text.lower()

    if "расплод" in t:
        score += 20
    else:
        advice.append("⚠️ мало расплода")

    if "мёд" in t:
        score += 15
    else:
        advice.append("⚠️ мало запасов мёда")

    if "нет матки" in t:
        score -= 50
        advice.append("🚨 срочно проверить матку")

    if score >= 80:
        advice.append("🟢 семья сильная")
    elif score >= 60:
        advice.append("🟡 нормальное развитие")
    else:
        advice.append("🔴 риск ослабления")

    return score, advice


@app.get("/")
def root():
    return {"status": "ok"}


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
