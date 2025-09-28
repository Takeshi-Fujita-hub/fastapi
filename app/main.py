from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI (read-only) 20250928"}

@app.get("/healthz")
def health_check():
    return {"status": "ok"}

@app.get("/items/")
def read_items():
    return [
        {"name": "apple"},
        {"name": "banana"},
        {"name": "cherry"}
    ]
