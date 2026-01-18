from fastapi import FastAPI
from app.routers import chats

app = FastAPI(
    title="Chat Service API",
    description="Тестовое задание для вакансии Python Developer",
    version="1.0.0"
)

# Подключаем роутер чатов
app.include_router(chats.router)

# Оставляем простой корневой эндпоинт для проверки здоровья сервиса
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Service is running"}