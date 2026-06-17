import io
import pytest
import fitz
from app.services.pdf_parser import extract_text_from_pdf, clean_text

def make_temp_pdf(tmp_path, content: str) -> str:
    """Helper: write content into a real single-page PDF."""
    pdf_path = tmp_path / "test.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), content, fontsize=11)
    doc.save(str(pdf_path))
    doc.close()
    return str(pdf_path)

def test_extract_text_returns_string(tmp_path):
    path = make_temp_pdf(tmp_path, "Hello World")
    result = extract_text_from_pdf(path)
    assert isinstance(result, str)
    assert len(result) > 0

def test_extract_text_contains_content(tmp_path):
    path = make_temp_pdf(tmp_path, "Variables are the foundation of algebra.")
    result = extract_text_from_pdf(path)
    assert "Variables" in result

def test_clean_text_removes_triple_newlines():
    raw = "Line one\n\n\n\nLine two\n\n\n\nLine three"
    result = clean_text(raw)
    assert "\n\n\n" not in result

def test_clean_text_collapses_multiple_spaces():
    raw = "Word    with    spaces"
    result = clean_text(raw)
    assert "    " not in result

def test_extract_multipage_pdf(tmp_path):
    pdf_path = tmp_path / "multi.pdf"
    doc = fitz.open()
    for i in range(3):
        page = doc.new_page()
        page.insert_text((72, 72), f"Page {i+1} content here.", fontsize=11)
    doc.save(str(pdf_path))
    doc.close()
    result = extract_text_from_pdf(str(pdf_path))
    assert "Page 1" in result
    assert "Page 3" in result
