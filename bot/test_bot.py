import asyncio
import requests
from app.models import init_db, get_users_by_difficulty_and_subject

async def test_database():
    await init_db()
    print("Database initialized successfully")

def test_webhook():
    url = "http://localhost:8000/webhook/"
    payload = {
        "id": 1,
        "title": "Test Course",
        "description": "Test Description",
        "start_date": "2024-01-01",
        "url": "https://example.com",
        "image_url": "https://example.com/image.jpg",
        "grades": [1, 2, 3],
        "difficulty": "beginner",
        "subjects": ["math", "physics"],
        "organization": "Test Org"
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Webhook test response: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Webhook test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_database())
    test_webhook() 