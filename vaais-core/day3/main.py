
from fastapi import FastAPI
from pydantic import BaseModel

class Items(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

name ="apple"
prices = 4

app = FastAPI()

@app.post("/Items/", response_model=Items)
async def create_item(item: Items):
    return item

@app.get("/Items/",response_model=Items)
async def read_items(name: str = "apple", max_price: float | None = None):
    return [
        Items(name="apple",price=4),
    ]
