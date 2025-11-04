from fastapi import FastAPI
from .routers import health

app = FastAPI(
    title="AI Resume Parser API",
    version="1.0.0",
    openapi_version="3.1.1"
)
app.include_router(health.router)

@app.get("/")
def root():
    return {"message": "Welcome to the AI Resume Parser API"}
