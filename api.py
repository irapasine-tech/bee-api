from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    hive: int
    text: str


@app.get("/")
def root():
    return {"status": "ok", "service": "bee-api 🐝"}


@app.post("/add")
def add(item: Item):
    return {
        "ok": True,
        "hive": item.hive,
        "text": item.text,
        "message": f"Улей {item.hive}: данные приняты"
    }
