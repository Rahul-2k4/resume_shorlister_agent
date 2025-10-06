from fastapi import FastAPI

app = FastAPI(title="Test Server")

@app.get("/")
async def root():
    return {"message": "Server is working!"}

@app.get("/test")
async def test():
    return {"status": "ok", "test": "successful"}
