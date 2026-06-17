import io
import fitz
import pytest
from app.services.pdf_extractor import extract_pages, is_scanned_pdf


def make_simple_pdf(texts: list[str]) -> bytes:
    """Create a minimal in-memory PDF with one text span per page."""
    doc = fitz.open()
    for text in texts:
        page = doc.new_page()
        if text:
            page.insert_text((72, 100), text, fontsize=12)
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


def test_extract_pages_count():
    pdf = make_simple_pdf(["Page one content", "Page two content", "Page three content"])
    pages = extract_pages(pdf)
    assert len(pages) == 3


def test_extract_pages_text_content():
    pdf = make_simple_pdf(["Hello world this is a test"])
    pages = extract_pages(pdf)
    assert "Hello" in pages[0].text


def test_extract_pages_page_numbers_are_1_based():
    pdf = make_simple_pdf(["A", "B"])
    pages = extract_pages(pdf)
    assert pages[0].page_num == 1
    assert pages[1].page_num == 2


def test_extract_pages_blocks_populated():
    pdf = make_simple_pdf(["Some block text here"])
    pages = extract_pages(pdf)
    assert len(pages[0].blocks) > 0
    assert pages[0].blocks[0].text != ""


def test_is_scanned_pdf_false_for_text_pdf():
    pdf = make_simple_pdf(["Normal page with plenty of text content"] * 5)
    pages = extract_pages(pdf)
    assert not is_scanned_pdf(pages)


def test_is_scanned_pdf_true_for_empty_pages():
    pdf = make_simple_pdf([""] * 10)
    pages = extract_pages(pdf)
    assert is_scanned_pdf(pages)
