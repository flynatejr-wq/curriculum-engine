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
