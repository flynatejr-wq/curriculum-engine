from pydantic import BaseModel
from typing import List, Optional


class LessonSchema(BaseModel):
    objective: str
    key_points: List[str]
    activity: str
    exit_ticket: str


class ChunkPreview(BaseModel):
    chunk_id: int
    text_preview: str
    word_count: int


class CurriculumEntry(BaseModel):
    week: int
    day: int
    chunk_id: int
    lesson: LessonSchema


class UploadResponse(BaseModel):
    textbook_id: int
    title: str
    total_chunks: int
    lessons_generated: int
    preview: List[CurriculumEntry]


class CurriculumResponse(BaseModel):
    textbook_id: int
    title: str
    curriculum: List[CurriculumEntry]
