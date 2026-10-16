from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_items(item: Item):
    return item


@app.get("/items/")
async def read_items():
    return {"message": "List of items"}
