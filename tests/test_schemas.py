from app.schemas import LessonSchema, ChunkPreview, CurriculumEntry, UploadResponse


def test_lesson_schema_validates_correct_data():
    data = {
        "objective": "Understand photosynthesis",
        "key_points": ["Chlorophyll absorbs light", "Water is split"],
        "activity": "Label a plant cell diagram",
        "exit_ticket": "What is the role of chlorophyll?"
    }
    lesson = LessonSchema(**data)
    assert lesson.objective == "Understand photosynthesis"
    assert len(lesson.key_points) == 2


def test_curriculum_entry_has_week_day_lesson():
    entry = CurriculumEntry(
        week=1,
        day=2,
        chunk_id=5,
        lesson=LessonSchema(
            objective="obj",
            key_points=["p1"],
            activity="act",
            exit_ticket="q?"
        )
    )
    assert entry.week == 1
    assert entry.day == 2


def test_upload_response_structure():
    resp = UploadResponse(
        textbook_id=1,
        title="Biology",
        total_chunks=30,
        lessons_generated=20,
        preview=[
            CurriculumEntry(
                week=1,
                day=1,
                chunk_id=1,
                lesson=LessonSchema(
                    objective="obj",
                    key_points=["p1"],
                    activity="act",
                    exit_ticket="q?"
                )
            )
        ]
    )
    assert resp.textbook_id == 1
    assert resp.lessons_generated == 20
    assert len(resp.preview) == 1
