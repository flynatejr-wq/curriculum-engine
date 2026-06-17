# Curriculum Engine

Textbook PDF → full semester curriculum builder.

## Setup

1. Create a PostgreSQL database named `curriculum_engine`
2. Copy `.env.example` to `.env` and fill in your credentials
3. Install dependencies: `pip install -r requirements.txt`

## Run

```bash
uvicorn app.main:app --reload
```

## API

- `POST /upload` — Upload a PDF textbook, generate curriculum
  - Form fields: `file` (PDF), `title` (string), `semester_weeks` (int, default 16)
- `GET /curriculum/{textbook_id}` — Retrieve stored curriculum for a textbook

## Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL async URL, e.g. `postgresql+asyncpg://user:pass@localhost/curriculum_engine` |
| `OPENAI_API_KEY` | Your OpenAI API key |
