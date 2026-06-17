import json
from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.openai_api_key)

REQUIRED_KEYS = {"objective", "key_points", "activity", "exit_ticket"}

SYSTEM_PROMPT = (
    "You are an expert curriculum designer. "
    "You generate structured lesson plans ONLY from the provided textbook content. "
    "Never add information not present in the source text."
)

USER_TEMPLATE = """Given the following textbook section, generate a JSON lesson plan.

TEXTBOOK SECTION:
{chunk_text}

Respond with ONLY valid JSON matching this exact structure:
{{
  "objective": "A single measurable learning objective based ONLY on the content above",
  "key_points": ["3 to 5 key points extracted ONLY from the content above"],
  "activity": "One student activity grounded in the content above",
  "exit_ticket": "One formative assessment question based ONLY on the content above"
}}"""


def generate_lesson(chunk_text: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_TEMPLATE.format(chunk_text=chunk_text)},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )
    raw = response.choices[0].message.content
    lesson = json.loads(raw)
    missing = REQUIRED_KEYS - lesson.keys()
    if missing:
        raise ValueError(f"LLM response missing required keys: {missing}")
    return lesson
