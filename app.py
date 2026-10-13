from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# 1. FastAPI ka instance create karein
app = FastAPI(title="Demo App", version="1.0.0")

# 2. Data model define karein (Request body validation ke liye)
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

# In-memory temporary database
fake_db = []

# 3. Root Endpoint (GET request)
@app.get("/")
def read_root():
    return {"message": "FastAPI Demo App running successfully!"}

# 4. Item fetch karne ka endpoint (Path parameter & Query parameter)
@app.get("/items/{item_id}")
def get_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "query": q}

# 5. New item create karne ka endpoint (POST request)
@app.post("/items/")
def create_item(item: Item):
    fake_db.append(item.dict())
    return {"status": "success", "data": item, "total_items": len(fake_db)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)