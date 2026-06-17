import pytest
from app.services.scheduler import build_schedule

def test_schedule_returns_one_entry_per_chunk():
    schedule = build_schedule(chunk_count=10)
    assert len(schedule) == 10

def test_schedule_entries_have_required_keys():
    schedule = build_schedule(chunk_count=5)
    for entry in schedule:
        assert "chunk_index" in entry
        assert "week" in entry
        assert "day" in entry

def test_schedule_is_sequential_by_chunk_index():
    schedule = build_schedule(chunk_count=20)
    indices = [entry["chunk_index"] for entry in schedule]
    assert indices == list(range(20))

def test_schedule_week_numbers_within_semester():
    schedule = build_schedule(chunk_count=80, semester_weeks=16, days_per_week=5)
    for entry in schedule:
        assert 1 <= entry["week"] <= 16

def test_schedule_day_numbers_within_week():
    schedule = build_schedule(chunk_count=80, semester_weeks=16, days_per_week=5)
    for entry in schedule:
        assert 1 <= entry["day"] <= 5

def test_single_chunk_assigned_to_week_1_day_1():
    schedule = build_schedule(chunk_count=1)
    assert schedule[0]["week"] == 1
    assert schedule[0]["day"] == 1

def test_exactly_80_chunks_cover_full_semester():
    schedule = build_schedule(chunk_count=80, semester_weeks=16, days_per_week=5)
    covered = {(e["week"], e["day"]) for e in schedule}
    assert len(covered) == 80

def test_no_skipping_weeks():
    schedule = build_schedule(chunk_count=48, semester_weeks=16)
    weeks_used = sorted({e["week"] for e in schedule})
    assert weeks_used[0] == 1
    for i in range(len(weeks_used) - 1):
        assert weeks_used[i+1] - weeks_used[i] <= 1
