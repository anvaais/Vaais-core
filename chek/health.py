from fastapi import FastAPI

# FastAPI instance initialize kar rahe hain
app = FastAPI(title="Health Check Demo")

# 1. Root endpoint (just for welcome)
@app.get("/")
def home():
    return {"message": "Welcome to my API!"}

# 2. GET /health endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FastAPI Dummy App",
        "version": "1.0.0"
    }