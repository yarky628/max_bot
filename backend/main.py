import os
from fastapi import FastAPI, Header, HTTPException, Request, Depends, Query
from dotenv import load_dotenv
from typing import List, Optional, Dict, Any

load_dotenv()

from .database import database
from .schemas import CreateRequest, RequestOut, PartnerIn, WebhookPayload
from . import crud
from . import max_api

ADMIN_SECRET = os.getenv("ADMIN_SECRET", "admin_secret_example")

app = FastAPI(title="Право выбора — Backend")

def require_admin(secret: str = Header(..., alias="X-Admin-Secret")):
    if secret != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/webhook")
async def webhook_handler(payload: WebhookPayload):
    try:
        print(f"Webhook received: {payload.model_dump()}")
        
        event_type = payload.type
        user_id = payload.user_id
        
        if not user_id:
            return {"ok": False, "error": "user_id is required"}
        
        if event_type == "message":
            text = (payload.text or "").strip().lower()
            
            if any(word in text for word in ["привет", "здравствуй", "начать", "start", "hello"]):
                await max_api.send_message(
                    user_id=user_id,
                    text="Здравствуйте! Я — помощник «Право выбора». Я помогу шаг за шагом восстановить документы, найти поддержку и работу. Это займёт 1–3 минуты. Продолжить?",
                    buttons=["Продолжить", "Подробнее о проекте"]
                )
            
            elif any(word in text for word in ["документы", "паспорт", "восстановить"]):
                await max_api.send_message(
                    user_id=user_id,
                    text="Понял, вам нужно восстановить документы. В каком регионе вы находитесь?",
                    buttons=["Москва", "Санкт-Петербург", "Другой регион"]
                )
            
            elif any(word in text for word in ["работа", "трудоустройство", "вакансия"]):
                await max_api.send_message(
                    user_id=user_id,
                    text="Помогу с трудоустройством. Какой у вас опыт работы?",
                    buttons=["Есть опыт", "Без опыта", "Нужна помощь с резюме"]
                )
            
            elif any(word in text for word in ["психолог", "поддержка", "помощь психологическая"]):
                await max_api.send_message(
                    user_id=user_id,
                    text="Психологическая поддержка доступна. Вы можете получить консультацию анонимно. Продолжить?",
                    buttons=["Да, получить помощь", "Позже"]
                )
            
            else:
                await max_api.send_message(
                    user_id=user_id,
                    text="Что вам нужно прямо сейчас?",
                    buttons=["SOS — угроза", "Восстановить документы", "Трудоустройство", "Психологическая поддержка", "Другое"]
                )
        
        elif event_type == "button_click":
            button_id = payload.button_id
            if button_id == "Продолжить":
                await max_api.send_message(
                    user_id=user_id,
                    text="Чтобы помочь, нам нужно ваше согласие на передачу минимальной информации профильным центрам и волонтёрам. Всё конфиденциально. Даёте согласие?",
                    buttons=["Даю согласие", "Анонимно (без передачи)"]
                )
            elif button_id in ["Даю согласие", "Анонимно (без передачи)"]:
                await max_api.send_message(
                    user_id=user_id,
                    text="Что вам нужно прямо сейчас?",
                    buttons=["SOS — угроза", "Восстановить документы", "Трудоустройство", "Психологическая поддержка", "Другое"]
                )
        
        return {"ok": True}
    
    except Exception as e:
        error_msg = str(e)
        print(f"Ошибка обработки webhook: {error_msg}")
        
        if "401" in error_msg or "Unauthorized" in error_msg:
            return {
                "ok": False, 
                "error": "Ошибка авторизации MAX API. Проверьте MAX_TOKEN в .env",
                "details": "Для тестирования без реальной отправки установите TEST_MODE=true в .env"
            }
        
        return {"ok": False, "error": error_msg}

@app.post("/api/requests", response_model=RequestOut)
async def create_request_endpoint(req: CreateRequest):
    out = await crud.create_request(req)
    return out

@app.get("/api/requests", response_model=List[RequestOut])
async def list_requests_endpoint(status: Optional[str] = None, region: Optional[str] = None, admin: bool = Depends(require_admin)):
    rows = await crud.list_requests(status=status, region=region)
    return rows

@app.post("/api/requests/{request_id}/assign")
async def assign_request_endpoint(request_id: str, assignee: str = Query(..., description="ID волонтёра или партнёра"), admin: bool = Depends(require_admin)):
    ok = await crud.assign_request(request_id, assignee)
    return {"ok": ok, "id": request_id}

@app.post("/api/partners")
async def add_partner_endpoint(p: PartnerIn, admin: bool = Depends(require_admin)):
    pid = await crud.add_partner(p)
    return {"ok": True, "id": pid}

