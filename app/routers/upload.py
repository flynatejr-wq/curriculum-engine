import os
import tempfile
from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Textbook, Chunk, Lesson
from app.schemas import UploadResponse, CurriculumEntry, LessonSchema
from app.services.pdf_parser import extract_text_from_pdf
from app.services.chunker import chunk_text
from app.services.scheduler import build_schedule
from app.services.lesson_generator import generate_lesson

router = APIRouter()

LESSON_LIMIT = 20

@router.post("/upload", response_model=UploadResponse)
async def upload_textbook(
    file: UploadFile = File(...),
    title: str = Form(...),
    semester_weeks: int = Form(16),
    db: AsyncSession = Depends(get_db),
):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        raw_text = extract_text_from_pdf(tmp_path)
    finally:
        os.unlink(tmp_path)

    textbook = Textbook(title=title, content=raw_text)
    db.add(textbook)
    await db.commit()
    await db.refresh(textbook)

    chunks = chunk_text(raw_text)
    db_chunks = []
    for chunk_text_content in chunks:
        chunk = Chunk(textbook_id=textbook.id, text=chunk_text_content)
        db.add(chunk)
        db_chunks.append(chunk)
    await db.commit()
    for c in db_chunks:
        await db.refresh(c)

    schedule = build_schedule(chunk_count=len(chunks), semester_weeks=semester_weeks)

    preview = []
    lessons_generated = 0

    for entry in schedule:
        if lessons_generated >= LESSON_LIMIT:
            break
        chunk = db_chunks[entry["chunk_index"]]
        lesson_data = generate_lesson(chunk.text)
        lesson = Lesson(chunk_id=chunk.id, lesson_json=lesson_data)
        db.add(lesson)
        lessons_generated += 1
        preview.append(
            CurriculumEntry(
                week=entry["week"],
                day=entry["day"],
                chunk_id=chunk.id,
                lesson=LessonSchema(**lesson_data),
            )
        )

    await db.commit()

    return UploadResponse(
        textbook_id=textbook.id,
        title=textbook.title,
        total_chunks=len(chunks),
        lessons_generated=lessons_generated,
        preview=preview,
    )
