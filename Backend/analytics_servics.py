from datetime import date, timedelta
from typing import List, Dict, Any

def calculate_practice_streaks(session_dates: List[date]) -> Dict[str, int]:
    if not session_dates:
        return {"current_streak": 0, "longest_streak": 0}

    unique_dates = sorted(set(session_dates), reverse=True)
    today = date.today()
    yesterday = today - timedelta(days=1)

    # Current streak calculation
    current_streak = 0
    if unique_dates[0] in (today, yesterday):
        anchor = unique_dates[0]
        for d in unique_dates:
            if d == anchor:
                current_streak += 1
                anchor -= timedelta(days=1)
            else:
                break

    # Longest streak calculation
    dates_asc = sorted(unique_dates)
    longest_streak = 0
    current_run = 0
    prev = None

    for d in dates_asc:
        if prev is None or d == prev + timedelta(days=1):
            current_run += 1
        else:
            current_run = 1
        prev = d
        if current_run > longest_streak:
            longest_streak = current_run

    return {
        "current_streak": current_streak,
        "longest_streak": max(longest_streak, current_streak)
    }

def calculate_goal_progress(target_hours: float, current_hours: float) -> Dict[str, Any]:
    if target_hours <= 0:
        return {"progress_percentage": 0.0, "status": "IN_PROGRESS"}
    pct = min(100.0, round((current_hours / target_hours) * 100.0, 1))
    return {
        "progress_percentage": pct,
        "status": "COMPLETED" if current_hours >= target_hours else "IN_PROGRESS"
    }
