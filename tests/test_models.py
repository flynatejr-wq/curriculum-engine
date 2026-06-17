import pytest
from sqlalchemy import select
from app.models import Textbook, Chunk, Lesson

@pytest.mark.asyncio
async def test_create_textbook(db_session):
    book = Textbook(title="Algebra I", content="Chapter 1...")
    db_session.add(book)
    await db_session.commit()
    await db_session.refresh(book)
    assert book.id is not None
    assert book.title == "Algebra I"

@pytest.mark.asyncio
async def test_create_chunk_linked_to_textbook(db_session):
    book = Textbook(title="Algebra I", content="Chapter 1...")
    db_session.add(book)
    await db_session.commit()
    chunk = Chunk(textbook_id=book.id, text="Section 1.1 text here")
    db_session.add(chunk)
    await db_session.commit()
    result = await db_session.execute(select(Chunk).where(Chunk.textbook_id == book.id))
    chunks = result.scalars().all()
    assert len(chunks) == 1
    assert chunks[0].text == "Section 1.1 text here"

@pytest.mark.asyncio
async def test_create_lesson_linked_to_chunk(db_session):
    book = Textbook(title="Algebra I", content="Chapter 1...")
    db_session.add(book)
    await db_session.commit()
    chunk = Chunk(textbook_id=book.id, text="Section text")
    db_session.add(chunk)
    await db_session.commit()
    lesson_data = {
        "objective": "Understand variables",
        "key_points": ["Variables represent unknowns"],
        "activity": "Solve x + 2 = 5",
        "exit_ticket": "What is a variable?"
    }
    lesson = Lesson(chunk_id=chunk.id, lesson_json=lesson_data)
    db_session.add(lesson)
    await db_session.commit()
    await db_session.refresh(lesson)
    assert lesson.id is not None
    assert lesson.lesson_json["objective"] == "Understand variables"
