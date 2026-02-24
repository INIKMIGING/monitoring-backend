from fastapi import FastAPI

app = FastAPI(
    title="Monitoring Backend API",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "API is running"}