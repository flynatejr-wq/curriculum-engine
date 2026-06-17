from typing import List, Dict

def build_schedule(
    chunk_count: int,
    semester_weeks: int = 16,
    days_per_week: int = 5
) -> List[Dict]:
    total_days = semester_weeks * days_per_week
    schedule = []

    for i in range(chunk_count):
        day_index = int(i * total_days / chunk_count)
        week = (day_index // days_per_week) + 1
        day = (day_index % days_per_week) + 1
        schedule.append({
            "chunk_index": i,
            "week": week,
            "day": day,
        })

    return schedule
