from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Textbook, Chunk
from app.schemas import CurriculumResponse, CurriculumEntry, LessonSchema
from app.services.scheduler import build_schedule

router = APIRouter()

@router.get("/curriculum/{textbook_id}", response_model=CurriculumResponse)
async def get_curriculum(textbook_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Textbook).where(Textbook.id == textbook_id))
    textbook = result.scalar_one_or_none()
    if not textbook:
        raise HTTPException(status_code=404, detail="Textbook not found")

    chunk_result = await db.execute(
        select(Chunk)
        .where(Chunk.textbook_id == textbook_id)
        .options(selectinload(Chunk.lesson))
        .order_by(Chunk.id)
    )
    chunks = chunk_result.scalars().all()

    schedule = build_schedule(chunk_count=len(chunks))
    curriculum = []
    for entry in schedule:
        chunk = chunks[entry["chunk_index"]]
        if chunk.lesson:
            curriculum.append(
                CurriculumEntry(
                    week=entry["week"],
                    day=entry["day"],
                    chunk_id=chunk.id,
                    lesson=LessonSchema(**chunk.lesson.lesson_json),
                )
            )

    return CurriculumResponse(
        textbook_id=textbook.id,
        title=textbook.title,
        curriculum=curriculum,
    )
