import os
import httpx
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

MAX_TOKEN = os.getenv("MAX_TOKEN")
MAX_API_BASE = os.getenv("MAX_API_BASE", "https://platform-api.max.ru")
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

async def send_message(
    user_id: str,
    text: str,
    buttons: Optional[list] = None,
    keyboard: Optional[list] = None
) -> Dict[str, Any]:
    if not MAX_TOKEN:
        raise ValueError("MAX_TOKEN не установлен в .env")
    
    url = f"{MAX_API_BASE}/messages"
    headers = {
        "Authorization": f"Bearer {MAX_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "user_id": user_id,
        "text": text
    }
    
    if buttons:
        payload["buttons"] = buttons
    elif keyboard:
        payload["keyboard"] = keyboard
    
    if TEST_MODE:
        print(f"[TEST MODE] Would send message to {user_id}: {text}")
        if buttons:
            print(f"[TEST MODE] Buttons: {buttons}")
        return {"ok": True, "test_mode": True, "message": "Message would be sent in production"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers, timeout=10.0)
            
            if response.status_code == 401:
                print(f"Ошибка авторизации MAX API:")
                print(f"URL: {url}")
                print(f"Response: {response.text}")
            
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"Ошибка отправки сообщения в MAX: {e}")
            print(f"Status: {e.response.status_code}")
            print(f"Response: {e.response.text}")
            raise
        except httpx.HTTPError as e:
            print(f"Ошибка сети при отправке в MAX: {e}")
            raise

async def send_typing(user_id: str) -> bool:
    if not MAX_TOKEN:
        return False
    
    url = f"{MAX_API_BASE}/messages/typing"
    headers = {
        "Authorization": f"Bearer {MAX_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {"user_id": user_id}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers, timeout=5.0)
            response.raise_for_status()
            return True
        except httpx.HTTPError:
            return False

