from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import upload, curriculum

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Curriculum Engine", lifespan=lifespan)

app.include_router(upload.router)
app.include_router(curriculum.router)
