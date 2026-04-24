import asyncio
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import Municipality, MunicipalityData

SEEDS_DIR = Path(__file__).parent


def parse_int(val):
    if not val or val.strip().lower() == 'null':
        return None
    return int(float(val))


def parse_float(val):
    if not val or val.strip().lower() == 'null':
        return None
    return float(val)


async def seed_municipalities(session):
    result = await session.execute(select(Municipality).limit(1))
    if result.scalar():
        print("✅ Муниципалитеты уже загружены, пропускаем")
        return

    with open(SEEDS_DIR / "municipalities.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        objects = [
            Municipality(
                id=int(row["id"]),
                name=row["name"],
                region=row["region"],
                type=row["type"],
                area=parse_float(row["area"].replace(',', '.')) if row["area"] else None,
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
                population=parse_int(row["population"]),
                birth_rate=parse_float(row["birth_rate"]),
                death_rate=parse_float(row["death_rate"]),
                migration=parse_int(row["migration"]),
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