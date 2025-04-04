from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.config import settings
from app.routers import phrases, users

app = FastAPI(title="QR Code Wars API")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для продакшена лучше указать конкретный домен фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(phrases.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "QR Code Wars API is running"}

# Инициализация базы данных при запуске
@app.on_event("startup")
async def startup_event():
    from sqlalchemy.orm import Session
    from app.db.base import SessionLocal
    from app.db.init_db import init_db
    
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

# Подключение роутеров будет здесь
# from app.routers import qrcodes, users, phrases

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True) 