from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import auth, results

app = FastAPI(title="Telegram Test API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(test.router, prefix="/api/test", tags=["test"])
app.include_router(results.router, prefix="/api/results", tags=["results"])


@app.get("/")
async def root():
    return {"status": "ok", "message": "Telegram Test API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)