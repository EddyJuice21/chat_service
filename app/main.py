from fastapi import FastAPI

app = FastAPI(title="Chat Service")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}