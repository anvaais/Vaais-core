from typing import Optional
from fastapi import FastAPI

app = FastAPI()

# Existing health route
@app.get("/health")
def health_check():
    return {"status": "ok"}

# New GET endpoint with query parameters
@app.get("/items")
def get_items(name: str, limit: Optional[int] = 10):
    return {
        "query": name,
        "limit": limit,
        "results": [f"Item matching {name} #{i+1}" for i in range(limit)]
    }