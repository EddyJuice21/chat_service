from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, crud, database

# Создаем роутер с префиксом /chats
router = APIRouter(
    prefix="/chats",
    tags=["chats"]
)


# 1. Создать чат
@router.post("/", response_model=schemas.Chat, status_code=status.HTTP_201_CREATED)
async def create_chat(
        chat: schemas.ChatCreate,
        db: AsyncSession = Depends(database.get_db)
):
    return await crud.create_chat(db=db, chat=chat)


# 2. Отправить сообщение в чат
@router.post("/{chat_id}/messages/", response_model=schemas.Message, status_code=status.HTTP_201_CREATED)
async def create_message(
        chat_id: int,
        message: schemas.MessageCreate,
        db: AsyncSession = Depends(database.get_db)
):
    db_message = await crud.create_message(db=db, chat_id=chat_id, message=message)

    if db_message is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    return db_message


# 3. Получить чат и последние сообщения
@router.get("/{chat_id}", response_model=schemas.ChatWithMessages)
async def get_chat(
        chat_id: int,
        # Валидация limit: по умолчанию 20, максимум 100
        limit: int = Query(default=20, le=100, ge=1),
        db: AsyncSession = Depends(database.get_db)
):
    chat = await crud.get_chat_with_messages(db=db, chat_id=chat_id, limit=limit)

    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    return chat


# 4. Удалить чат
@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
        chat_id: int,
        db: AsyncSession = Depends(database.get_db)
):
    success = await crud.delete_chat(db=db, chat_id=chat_id)

    if not success:
        raise HTTPException(status_code=404, detail="Chat not found")

    return None