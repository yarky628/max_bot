import uuid
from .database import database
from .models import requests, partners
from .schemas import CreateRequest, PartnerIn
from datetime import datetime

async def create_request(req: CreateRequest):
    rid = str(uuid.uuid4())
    query = requests.insert().values(
        id=rid,
        category=req.category,
        region=req.region,
        short_text=req.short_text,
        phone_encrypted=req.phone,
        consent=req.consent,
        status="new",
        created_at=datetime.utcnow()
    )
    await database.execute(query)
    return {**req.model_dump(), "id": rid, "status": "new", "created_at": datetime.utcnow(), "assigned_to": None}

async def list_requests(status: str = None, region: str = None):
    query = requests.select()
    if status:
        query = query.where(requests.c.status == status)
    if region:
        query = query.where(requests.c.region == region)
    rows = await database.fetch_all(query)
    return [dict(r) for r in rows]

async def assign_request(request_id: str, assignee: str):
    query = requests.update().where(requests.c.id == request_id).values(assigned_to=assignee, status="in_progress")
    await database.execute(query)
    return True

async def add_partner(p: PartnerIn):
    pid = str(uuid.uuid4())
    query = partners.insert().values(
        id=pid,
        name=p.name,
        region=p.region,
        contact=p.contact,
        type=p.type,
        notes=getattr(p, "notes", None)
    )
    await database.execute(query)
    return pid

async def seed_partners_from_list(partner_list):
    for p in partner_list:
        if isinstance(p, dict):
            partner = PartnerIn(**p)
        else:
            partner = p
        await add_partner(partner)

