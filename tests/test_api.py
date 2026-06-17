import io
import json
import pytest
import pytest_asyncio
import fitz
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.models import Base
from app.database import get_db

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"
MOCK_LESSON = {
    "objective": "Test objective",
    "key_points": ["Point 1", "Point 2"],
    "activity": "Test activity",
    "exit_ticket": "Test question?"
}

@pytest_asyncio.fixture
async def test_app():
    engine = create_async_engine(TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_db():
        async with factory() as session:
            yield session

    from app.main import app
    app.dependency_overrides[get_db] = override_get_db
    yield app
    app.dependency_overrides.clear()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

def make_pdf_bytes(text: str) -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text, fontsize=11)
    buf = io.BytesIO()
    doc.save(buf)
    doc.close()
    return buf.getvalue()

@pytest.mark.asyncio
async def test_upload_returns_200(test_app):
    pdf_bytes = make_pdf_bytes("Chapter 1: Introduction. " * 200)
    with patch("app.services.lesson_generator.client") as mock_client:
        mock_msg = MagicMock()
        mock_msg.content = json.dumps(MOCK_LESSON)
        mock_choice = MagicMock()
        mock_choice.message = mock_msg
        mock_client.chat.completions.create.return_value = MagicMock(choices=[mock_choice])

        async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
            response = await client.post(
                "/upload",
                files={"file": ("test.pdf", pdf_bytes, "application/pdf")},
                data={"title": "Test Book"}
            )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_upload_response_has_required_fields(test_app):
    pdf_bytes = make_pdf_bytes("Introduction to Algebra. " * 300)
    with patch("app.services.lesson_generator.client") as mock_client:
        mock_msg = MagicMock()
        mock_msg.content = json.dumps(MOCK_LESSON)
        mock_choice = MagicMock()
        mock_choice.message = mock_msg
        mock_client.chat.completions.create.return_value = MagicMock(choices=[mock_choice])

        async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
            response = await client.post(
                "/upload",
                files={"file": ("book.pdf", pdf_bytes, "application/pdf")},
                data={"title": "Algebra I"}
            )
    body = response.json()
    assert "textbook_id" in body
    assert "total_chunks" in body
    assert "lessons_generated" in body
    assert "preview" in body
    assert body["title"] == "Algebra I"

@pytest.mark.asyncio
async def test_upload_limits_lessons_to_20(test_app):
    big_text = ("This is educational content about a very important topic. " * 50 + "\n\n") * 30
    pdf_bytes = make_pdf_bytes(big_text[:3000])
    with patch("app.services.lesson_generator.client") as mock_client:
        mock_msg = MagicMock()
        mock_msg.content = json.dumps(MOCK_LESSON)
        mock_choice = MagicMock()
        mock_choice.message = mock_msg
        mock_client.chat.completions.create.return_value = MagicMock(choices=[mock_choice])

        async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
            response = await client.post(
                "/upload",
                files={"file": ("big.pdf", pdf_bytes, "application/pdf")},
                data={"title": "Big Book"}
            )
    body = response.json()
    assert body["lessons_generated"] <= 20

@pytest.mark.asyncio
async def test_get_curriculum_returns_404_for_unknown_id(test_app):
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
        response = await client.get("/curriculum/9999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_curriculum_returns_200_after_upload(test_app):
    pdf_bytes = make_pdf_bytes("Introduction to Algebra. " * 300)
    with patch("app.services.lesson_generator.client") as mock_client:
        mock_msg = MagicMock()
        mock_msg.content = json.dumps(MOCK_LESSON)
        mock_choice = MagicMock()
        mock_choice.message = mock_msg
        mock_client.chat.completions.create.return_value = MagicMock(choices=[mock_choice])

        async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
            upload_response = await client.post(
                "/upload",
                files={"file": ("book.pdf", pdf_bytes, "application/pdf")},
                data={"title": "Algebra I"}
            )
            textbook_id = upload_response.json()["textbook_id"]
            curriculum_response = await client.get(f"/curriculum/{textbook_id}")

    assert curriculum_response.status_code == 200
    body = curriculum_response.json()
    assert "textbook_id" in body
    assert "curriculum" in body
    assert body["textbook_id"] == textbook_id
