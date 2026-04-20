from fastapi import FastAPI

app = FastAPI()

db = []


def analyze(text: str):
    t = text.lower()

    score = 60
    advice = []

    if "расплод" in t:
        score += 20
    else:
        score -= 15
        advice.append("⚠️ мало расплода")

    if "мёд" in t:
        score += 15
    else:
        score -= 10
        advice.append("🍯 мало запасов мёда")

    if "матка" in t:
        if "нет" in t:
            score -= 40
            advice.append("🚨 нет матки — срочно проверить")
        else:
            score += 15

    if score >= 80:
        advice.append("🟢 сильная семья")
    elif score >= 60:
        advice.append("🟡 нормальное состояние")
    elif score >= 40:
        advice.append("🟠 ослабленная семья")
    else:
        advice.append("🔴 критическое состояние")

    return max(0, min(100, score)), advice


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
