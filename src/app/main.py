from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import Request

from .routers import auth, health, resumes  # ✅ auth comes first
from .db import init_db


init_db()

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="AI Resume Parser API",
    version="1.0.0",
    openapi_version="3.1.1"
)

app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."}
    )


app.include_router(auth.router)
app.include_router(health.router)
app.include_router(resumes.router)


@app.get("/", tags=["Root"])
@limiter.limit("10/minute")
def root(request: Request):
    return {"message": "Welcome to the AI Resume Parser API"}