from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 📦 модель входных данных
class Item(BaseModel):
    hive: int
    text: str


# 🟢 проверка что сервер жив
@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "bee-api 🐝"
    }


# 📊 основной endpoint для бота
@app.post("/add")
def add(item: Item):
    return {
        "ok": True,
        "hive": item.hive,
        "text": item.text,
        "analysis": f"Улей {item.hive}: данные приняты"
    }
