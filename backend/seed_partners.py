import csv
import asyncio
import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import database
from backend.crud import add_partner
from backend.schemas import PartnerIn

default_csv = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend", "data", "partners.csv")
CSV_PATH = os.getenv("PARTNERS_CSV", default_csv)

async def load():
    await database.connect()
    if not os.path.exists(CSV_PATH):
        print("CSV not found:", CSV_PATH)
        await database.disconnect()
        return
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            partner = {
                "name": row.get("name"),
                "region": row.get("region"),
                "contact": row.get("contact"),
                "type": row.get("type"),
                "notes": row.get("notes", "")
            }
            try:
                partner_obj = PartnerIn(**partner)
                await add_partner(partner_obj)
            except Exception as e:
                print("Error adding partner:", e)
    await database.disconnect()
    print("Seeding complete.")

if __name__ == "__main__":
    asyncio.run(load())

