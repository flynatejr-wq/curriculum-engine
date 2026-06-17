import pytest
from app.schemas import PageContent, Block
from app.services.structure_detector import (
    _toc_to_structure,
    _font_heuristic,
    _regex_detect,
    _flat_fallback,
)


def make_pages_with_headings(headings: list[tuple[int, str, float]]) -> list[PageContent]:
    """headings: [(page_num, heading_text, font_size)]"""
    pages = []
    for page_num, text, size in headings:
        pages.append(PageContent(
            page_num=page_num,
            text=text + " body text here " * 20,
            blocks=[
                Block(text=text, font_size=size, is_bold=True),
                Block(text="body text here " * 5, font_size=12.0, is_bold=False),
            ],
        ))
    return pages


def test_toc_to_structure_returns_none_for_empty_toc():
    result = _toc_to_structure([], total_pages=100)
    assert result is None


def test_toc_to_structure_parses_chapters():
    toc = [[1, "Introduction", 1], [1, "Chapter 1", 10], [1, "Chapter 2", 30]]
    result = _toc_to_structure(toc, total_pages=50)
    assert result is not None
    assert result.detection_method == "toc"
    assert len(result.chapters) == 3
    assert result.chapters[0].title == "Introduction"


def test_toc_to_structure_sets_end_pages():
    toc = [[1, "Ch 1", 1], [1, "Ch 2", 20], [1, "Ch 3", 40]]
    result = _toc_to_structure(toc, total_pages=60)
    assert result.chapters[0].end_page == 19
    assert result.chapters[1].end_page == 39
    assert result.chapters[2].end_page == 60


def test_font_heuristic_detects_large_headings():
    # Build pages: 3 heading pages + 47 body-only pages to establish body_size median
    pages = make_pages_with_headings([
        (1, "Chapter One Introduction", 24.0),
        (15, "Chapter Two Methods", 24.0),
        (30, "Chapter Three Results", 24.0),
    ])
    for i in range(4, 51):
        if not any(p.page_num == i for p in pages):
            pages.append(PageContent(
                page_num=i,
                text="body text " * 30,
                blocks=[Block(text="body text", font_size=12.0, is_bold=False)] * 10,
            ))
    pages.sort(key=lambda p: p.page_num)
    result = _font_heuristic(pages, total_pages=50)
    assert result is not None
    assert result.detection_method == "font_heuristic"
    assert len(result.chapters) >= 2


def test_regex_detect_finds_chapter_headings():
    pages = [
        PageContent(page_num=1, text="Chapter 1: Introduction to the subject", blocks=[
            Block(text="Chapter 1: Introduction to the subject", font_size=14.0),
        ]),
        PageContent(page_num=2, text="Some body text here on page 2", blocks=[
            Block(text="Some body text", font_size=12.0),
        ]),
        PageContent(page_num=10, text="Chapter 2: Methods and approaches", blocks=[
            Block(text="Chapter 2: Methods and approaches", font_size=14.0),
        ]),
    ]
    result = _regex_detect(pages, total_pages=20)
    assert result is not None
    assert result.detection_method == "regex"
    assert len(result.chapters) == 2


def test_flat_fallback_returns_single_chapter():
    result = _flat_fallback(total_pages=100, warning="test warning")
    assert result.detection_method == "flat"
    assert len(result.chapters) == 1
    assert result.chapters[0].start_page == 1
    assert result.chapters[0].end_page == 100
    assert "test warning" in result.warnings[0]
