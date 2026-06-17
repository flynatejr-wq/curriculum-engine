import pytest
from app.services.chunker import chunk_text

def make_text(word_count: int) -> str:
    """Generate deterministic text of exactly word_count words, split into paragraphs."""
    words = [f"word{i}" for i in range(word_count)]
    # Group into paragraphs of ~50 words separated by double newlines
    paras = []
    for i in range(0, len(words), 50):
        paras.append(" ".join(words[i:i+50]))
    return "\n\n".join(paras)

def test_short_text_produces_one_chunk():
    text = make_text(200)
    chunks = chunk_text(text)
    assert len(chunks) == 1

def test_long_text_splits_into_multiple_chunks():
    text = make_text(4000)
    chunks = chunk_text(text)
    assert len(chunks) >= 3

def test_each_chunk_within_word_bounds():
    text = make_text(5000)
    chunks = chunk_text(text)
    for chunk in chunks:
        wc = len(chunk.split())
        assert wc <= 1600, f"Chunk has {wc} words, exceeds max"

def test_chunks_preserve_all_content():
    text = make_text(3000)
    chunks = chunk_text(text)
    combined = " ".join(chunks)
    original_words = set(text.split())
    combined_words = set(combined.split())
    assert original_words == combined_words

def test_empty_text_returns_empty_list():
    assert chunk_text("") == []

def test_chunks_are_sequential():
    words = [f"word{i}" for i in range(100)]
    paras = [" ".join(words[i:i+10]) for i in range(0, 100, 10)]
    text = "\n\n".join(paras)
    chunks = chunk_text(text, min_words=20, max_words=40)
    # word0 must appear before word99 across chunks
    first_chunk_has_word0 = "word0" in chunks[0]
    last_chunk_has_word99 = "word99" in chunks[-1]
    assert first_chunk_has_word0
    assert last_chunk_has_word99
