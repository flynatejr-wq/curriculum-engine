from typing import List

def chunk_text(text: str, min_words: int = 800, max_words: int = 1500) -> List[str]:
    if not text.strip():
        return []

    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    chunks: List[str] = []
    current: List[str] = []
    current_word_count = 0

    for para in paragraphs:
        para_words = len(para.split())

        if current_word_count + para_words > max_words and current_word_count >= min_words:
            chunks.append('\n\n'.join(current))
            current = [para]
            current_word_count = para_words
        else:
            current.append(para)
            current_word_count += para_words

    if current:
        chunks.append('\n\n'.join(current))

    return chunks
