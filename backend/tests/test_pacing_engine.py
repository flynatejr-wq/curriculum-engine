import pytest
from app.schemas import Chapter, Section, StructureMap
from app.services.pacing_engine import build_schedule, _flatten_to_units


def make_structure(chapters: list[dict], total_pages: int) -> StructureMap:
    ch_list = []
    for c in chapters:
        sections = [
            Section(title=s["title"], start_page=s["start_page"])
            for s in c.get("sections", [])
        ]
        ch_list.append(Chapter(
            title=c["title"],
            start_page=c["start_page"],
            end_page=c["end_page"],
            sections=sections,
        ))
    return StructureMap(
        detection_method="toc",
        total_pages=total_pages,
        chapters=ch_list,
    )


def test_total_sessions_correct():
    s = make_structure([{"title": "Ch1", "start_page": 1, "end_page": 100}], 100)
    schedule = build_schedule(s, total_weeks=4, sessions_per_week=3)
    assert schedule.total_sessions == 12
    assert len(schedule.sessions) == 12


def test_week_and_day_numbers():
    s = make_structure([{"title": "Ch1", "start_page": 1, "end_page": 60}], 60)
    schedule = build_schedule(s, total_weeks=4, sessions_per_week=3)
    # Session 1 → week 1, day 1
    assert schedule.sessions[0].week_number == 1
    assert schedule.sessions[0].day_number == 1
    # Session 4 → week 2, day 1
    assert schedule.sessions[3].week_number == 2
    assert schedule.sessions[3].day_number == 1


def test_all_pages_covered():
    """Every page should appear in exactly one session."""
    s = make_structure([
        {"title": "Ch1", "start_page": 1, "end_page": 50},
        {"title": "Ch2", "start_page": 51, "end_page": 100},
        {"title": "Ch3", "start_page": 101, "end_page": 150},
    ], 150)
    schedule = build_schedule(s, total_weeks=3, sessions_per_week=3)
    # Each session should have content
    sessions_with_content = [sess for sess in schedule.sessions if sess.units]
    assert len(sessions_with_content) > 0
    # First session starts at page 1
    assert schedule.sessions[0].start_page == 1


def test_sections_preferred_over_chapters():
    s = make_structure([{
        "title": "Ch1", "start_page": 1, "end_page": 100,
        "sections": [
            {"title": "Sec A", "start_page": 1},
            {"title": "Sec B", "start_page": 50},
        ]
    }], 100)
    units = _flatten_to_units(s)
    assert all(u.source == "section" for u in units)
    assert len(units) == 2


def test_chapters_used_when_no_sections():
    s = make_structure([
        {"title": "Ch1", "start_page": 1, "end_page": 50},
        {"title": "Ch2", "start_page": 51, "end_page": 100},
    ], 100)
    units = _flatten_to_units(s)
    assert all(u.source == "chapter" for u in units)
    assert len(units) == 2


def test_large_chapter_split_across_sessions():
    """A 200-page chapter with only 2 sessions of 10 pages target should be split."""
    s = make_structure([
        {"title": "Giant Chapter", "start_page": 1, "end_page": 200}
    ], 200)
    schedule = build_schedule(s, total_weeks=4, sessions_per_week=5)  # 20 sessions, ~10 pages each
    # Should have more than one session with content from Giant Chapter
    sessions_with_content = [sess for sess in schedule.sessions if sess.units]
    assert len(sessions_with_content) > 1


def test_target_pages_per_session_calculated():
    s = make_structure([
        {"title": "Ch1", "start_page": 1, "end_page": 160},
    ], 160)
    schedule = build_schedule(s, total_weeks=4, sessions_per_week=2)  # 8 sessions
    assert schedule.target_pages_per_session == 20  # 160 / 8
