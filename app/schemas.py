from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# --- Базовые схемы ---

class MessageBase(BaseModel):
    # text: не пустой, до 5000 символов
    text: str = Field(..., min_length=1, max_length=5000)

class ChatBase(BaseModel):
    # title: не пустой, до 200 символов
    title: str = Field(..., min_length=1, max_length=200)

# --- Схемы для создания ---

class MessageCreate(MessageBase):
    pass

class ChatCreate(ChatBase):
    pass

# --- Схемы для чтения ---

class Message(MessageBase):
    id: int
    chat_id: int
    created_at: datetime

    # Эта настройка нужна, чтобы Pydantic умел читать данные прямо из объектов ORM
    model_config = ConfigDict(from_attributes=True)

class Chat(ChatBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Специальная схема для GET /chats/{id}, где возвращается чат вместе со списком сообщений
class ChatWithMessages(Chat):
    messages: list[Message] = []