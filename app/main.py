from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.core.config import settings

APP_NAME = settings.APP_NAME
app = FastAPI(title=APP_NAME, version=settings.APP_VERSION)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": f"{APP_NAME} is running"}


@app.get("/health_check")
async def health_check():
    return {"status": "ok"}
