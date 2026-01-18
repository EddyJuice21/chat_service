from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models, schemas


# --- Chat Operations ---

async def create_chat(db: AsyncSession, chat: schemas.ChatCreate):
    # Триммим пробелы по краям
    clean_title = chat.title.strip()
    db_chat = models.Chat(title=clean_title)
    db.add(db_chat)
    await db.commit()
    await db.refresh(db_chat)
    return db_chat


async def get_chat_with_messages(db: AsyncSession, chat_id: int, limit: int = 20):
    """
    Получает чат и последние N сообщений.
    """
    # 1. Сначала ищем сам чат
    result = await db.execute(select(models.Chat).where(models.Chat.id == chat_id))
    chat = result.scalar_one_or_none()

    if not chat:
        return None

    # 2. Получаем сообщения для этого чата
    # Сортируем по убыванию даты, ограничиваем limit
    msgs_stmt = (
        select(models.Message)
        .where(models.Message.chat_id == chat_id)
        .order_by(models.Message.created_at.desc())
        .limit(limit)
    )
    msgs_result = await db.execute(msgs_stmt)
    messages = msgs_result.scalars().all()

    # Разворачиваем список, чтобы при выводе они шли в хронологическом порядке
    chat.messages = list(reversed(messages))

    return chat


async def delete_chat(db: AsyncSession, chat_id: int):
    # Ищем чат
    result = await db.execute(select(models.Chat).where(models.Chat.id == chat_id))
    chat = result.scalar_one_or_none()

    if chat:
        await db.delete(chat)  # Каскадное удаление сообщений произойдет на уровне БД
        await db.commit()
        return True
    return False


# --- Message Operations ---

async def create_message(db: AsyncSession, chat_id: int, message: schemas.MessageCreate):
    # Сначала проверяем, существует ли чат
    result = await db.execute(select(models.Chat).where(models.Chat.id == chat_id))
    chat = result.scalar_one_or_none()

    if not chat:
        return None  # Вернем None, чтобы роутер выдал 404

    # Создаем сообщение
    db_message = models.Message(chat_id=chat_id, text=message.text)
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message