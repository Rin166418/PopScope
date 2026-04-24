import asyncio
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import Municipality, MunicipalityData

SEEDS_DIR = Path(__file__).parent


async def seed_municipalities(session):
    result = await session.execute(select(Municipality).limit(1))
    if result.scalar():
        print("✅ Муниципалитеты уже загружены, пропускаем")
        return

    with open(SEEDS_DIR / "municipality.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        objects = [
            Municipality(
                id=int(row["id"]),
                name=row["name"],
                region=row["region"],
                type=row["type"],
                area=float(row["area"]) if row["area"] else None,
            )
            for row in reader
        ]

    session.add_all(objects)
    await session.commit()
    print(f"🌱 Загружено {len(objects)} муниципалитетов")


async def seed_municipality_data(session):
    result = await session.execute(select(MunicipalityData).limit(1))
    if result.scalar():
        print("✅ Данные муниципалитетов уже загружены, пропускаем")
        return

    with open(SEEDS_DIR / "municipality_data.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        objects = [
            MunicipalityData(
                id=int(row["id"]),
                municipality_id=int(row["municipality_id"]),
                year=int(row["year"]),
                population=int(row["population"]) if row["population"] else None,
                birth_rate=float(row["birth_rate"]) if row["birth_rate"] else None,
                death_rate=float(row["death_rate"]) if row["death_rate"] else None,
                migration=int(row["migration"]) if row["migration"] else None,
            )
            for row in reader
        ]

    session.add_all(objects)
    await session.commit()
    print(f"🌱 Загружено {len(objects)} записей данных муниципалитетов")


async def main():
    async with AsyncSessionLocal() as session:
        await seed_municipalities(session)
        await seed_municipality_data(session)


if __name__ == "__main__":
    asyncio.run(main())