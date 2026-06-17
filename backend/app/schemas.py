from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel


class Block(BaseModel):
    text: str
    font_size: float | None = None
    is_bold: bool = False


class PageContent(BaseModel):
    page_num: int   # 1-based
    text: str
    blocks: list[Block] = []


class Section(BaseModel):
    title: str
    start_page: int
    end_page: int | None = None


class Chapter(BaseModel):
    title: str
    chapter_num: int | None = None
    start_page: int
    end_page: int | None = None
    sections: list[Section] = []


class StructureMap(BaseModel):
    detection_method: str   # "toc" | "font_heuristic" | "regex" | "llm_fallback" | "flat"
    total_pages: int
    chapters: list[Chapter]
    warnings: list[str] = []


class SessionData(BaseModel):
    session_id: str
    filename: str
    pages: list[PageContent]
    structure: StructureMap | None = None
    created_at: datetime


class UploadResponse(BaseModel):
    session_id: str
    filename: str
    total_pages: int
    structure: StructureMap
    message: str


class StructureResponse(BaseModel):
    session_id: str
    filename: str
    structure: StructureMap


# ── Phase 2: Pacing ──────────────────────────────────────────────────────────

class ScheduleUnit(BaseModel):
    title: str
    start_page: int
    end_page: int
    source: str  # "chapter" | "section"


class SessionSlot(BaseModel):
    session_number: int
    week_number: int
    day_number: int       # 1-based within the week
    units: list[ScheduleUnit]
    start_page: int
    end_page: int
    page_count: int


class Schedule(BaseModel):
    total_weeks: int
    sessions_per_week: int
    total_sessions: int
    target_pages_per_session: int
    sessions: list[SessionSlot]


class PaceRequest(BaseModel):
    session_id: str
    total_weeks: int
    sessions_per_week: int


class PaceResponse(BaseModel):
    session_id: str
    filename: str
    schedule: Schedule
