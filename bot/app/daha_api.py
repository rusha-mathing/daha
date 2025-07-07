import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("BOT_DB_URL") or "postgresql://daha_user:SWP2025@localhost/daha_db"

async def fetch_subjects():
    """Получить все предметы из PostgreSQL"""
    conn = await asyncpg.connect(DB_URL)
    query = '''
        SELECT json_agg(json_build_object(
            'id', s.id,
            'type', s.type,
            'label', s.label,
            'icon', s.icon,
            'color', s.color,
            'additional_description', s.additional_description
        )) AS subjects
        FROM subject s
    '''
    result = await conn.fetchval(query)
    await conn.close()
    return result or []

async def fetch_difficulties():
    """Получить все уровни сложности из PostgreSQL"""
    conn = await asyncpg.connect(DB_URL)
    query = '''
        SELECT json_agg(json_build_object(
            'id', d.id,
            'type', d.type,
            'label', d.label,
            'icon', d.icon,
            'color', d.color
        )) AS difficulties
        FROM difficulty d
    '''
    result = await conn.fetchval(query)
    await conn.close()
    return result or []

async def fetch_courses():
    """Получить все курсы из PostgreSQL"""
    conn = await asyncpg.connect(DB_URL)
    query = '''
        SELECT json_agg(json_build_object(
            'id', c.id,
            'title', c.title,
            'description', c.description,
            'start_date', c.start_date,
            'end_date', c.end_date,
            'url', c.url,
            'image_url', c.image_url
        )) AS courses
        FROM course c
    '''
    result = await conn.fetchval(query)
    await conn.close()
    return result or []

# Замена старой функции fetch_endpoint
async def fetch_endpoint(endpoint):
    """Совместимость со старым кодом - теперь получает данные напрямую из PostgreSQL"""
    if endpoint == "subjects":
        return await fetch_subjects()
    elif endpoint == "difficulties":
        return await fetch_difficulties()
    elif endpoint == "courses":
        return await fetch_courses()
    else:
        return []

# Пример использования:
# courses = await fetch_courses()
