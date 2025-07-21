import asyncpg
import json
import logging
import httpx
from .config import settings

DB_URL = settings.BOT_DB_URL
BACKEND_URL = "http://localhost:8000" # Assuming backend runs on port 8000
logger = logging.getLogger(__name__)

async def link_telegram_account(token: str, telegram_id: int):
    """Send link request to the backend."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BACKEND_URL}/api/v1/auth/link-telegram",
                json={"token": token, "telegram_id": telegram_id},
                timeout=10.0
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error linking account: {e.response.status_code} - {e.response.text}")
            error_detail = e.response.json().get("detail", "Unknown error")
            return {"success": False, "error": error_detail}
        except httpx.RequestError as e:
            logger.error(f"Request error linking account: {e}")
            return {"success": False, "error": "Could not connect to the backend service."}

async def _fetch_json_from_db(query: str):
    """Generic function to fetch and parse JSON from PostgreSQL."""
    try:
        conn = await asyncpg.connect(DB_URL)
        json_str = await conn.fetchval(query)
        await conn.close()
        if json_str:
            return json.loads(json_str)
        return []
    except (asyncpg.PostgresError, OSError) as e:
        logger.error(f"Database error: {e}")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []

async def fetch_subjects():
    """Получить все предметы из PostgreSQL"""
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
    return await _fetch_json_from_db(query)

async def fetch_difficulties():
    """Получить все уровни сложности из PostgreSQL"""
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
    return await _fetch_json_from_db(query)

async def fetch_courses():
    """Получить все курсы из PostgreSQL"""
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
    return await _fetch_json_from_db(query)

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
