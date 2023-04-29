from fastapi import FastAPI

from core.config import settings
from api.router import router
from db.sessions import create_db_and_tables, bulk_create_profiles


app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    openapi_prefix=settings.openapi_prefix,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url
)

app.include_router(router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    return {"Say": "Hello!"}



@app.get("/create_tables")
async def create_tables():
    await create_db_and_tables()

    return {"Say": "Tables created!"}


@app.get("/create_profiles/{number}")
async def create_profiles(
    number: int,
):
    await bulk_create_profiles(number)

    return {"Say": "Profiles created!"}