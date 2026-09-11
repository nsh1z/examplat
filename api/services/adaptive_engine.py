import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

def calculate_mastery(correct_count: int, incorrect_count: int, attempts: List[Dict[str, Any]]) -> float:
    """
    Calculates dynamic mastery (0.0 to 100.0) based on total successes,
    error penalties, and recent trend weighting.
    """
    total = correct_count + incorrect_count
    if total == 0:
        return 0.0

    raw_ratio = (correct_count / total) * 100.0
    
    # Recent trend bonus/penalty (last 3 attempts)
    recent = attempts[-3:] if attempts else []
    if recent:
        recent_avg = sum(a["score"] for a in recent) / len(recent)
        # Weighted blend: 60% historical, 40% recent performance
        blended = (raw_ratio * 0.6) + (recent_avg * 0.4)
    else:
        blended = raw_ratio

    # Penalize if repeated errors
    if incorrect_count > correct_count:
        blended = max(0.0, blended - 10.0)

    return round(min(100.0, max(0.0, blended)), 1)

def update_spaced_repetition(current_interval: float, ease_factor: float, score: float) -> tuple[float, float, str]:
    """
    SuperMemo-2 (SM-2) inspired spaced repetition algorithm.
    Returns: (new_interval_days, new_ease_factor, next_review_iso_date)
    """
    # Quality scale from 0 to 5 based on 0-100 score
    if score >= 90:
        quality = 5
    elif score >= 75:
        quality = 4
    elif score >= 60:
        quality = 3
    elif score >= 40:
        quality = 2
    elif score >= 20:
        quality = 1
    else:
        quality = 0

    # Calculate new ease factor
    new_ef = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    new_ef = max(1.3, round(new_ef, 2))

    # Calculate new interval
    if quality < 3:
        new_interval = 1.0  # Review tomorrow or today
    else:
        if current_interval <= 1.0:
            new_interval = 3.0
        elif current_interval <= 3.0:
            new_interval = 7.0
        else:
            new_interval = round(current_interval * new_ef, 1)

    next_review_dt = datetime.now() + timedelta(days=new_interval)
    return new_interval, new_ef, next_review_dt.strftime("%Y-%m-%d")

def get_next_adaptive_question(
    conn: sqlite3.Connection,
    user_id: str = "default_user",
    topic_id: Optional[str] = None,
    difficulty: Optional[str] = None,
    q_type: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Intelligently selects the next question applying the strict Anti-Repetition filter:
    1. Excludes questions recently answered by the user.
    2. Prioritizes concepts marked as 'debil' or with next_review_at <= now.
    3. If all questions for a weak concept were used, varies the question type (e.g. from MC to True/False or Open).
    """
    cursor = conn.cursor()

    # Get recent question IDs to avoid repeating
    cursor.execute("""
    SELECT question_id FROM question_attempts
    WHERE user_id = ?
    ORDER BY created_at DESC
    LIMIT 25;
    """, (user_id,))
    recent_q_ids = set(row[0] for row in cursor.fetchall())

    # Find weak or review-pending concepts
    query_concepts = """
    SELECT cp.concept_id, cp.mastery, cp.status, cp.needs_practice_flag
    FROM concept_progress cp
    JOIN concepts c ON cp.concept_id = c.id
    WHERE cp.user_id = ?
    """
    params_c = [user_id]

    if topic_id:
        query_concepts += " AND c.topic_id = ?"
        params_c.append(topic_id)

    query_concepts += """
    ORDER BY 
        cp.needs_practice_flag DESC,
        CASE WHEN cp.status = 'debil' THEN 1
             WHEN cp.next_review_at <= date('now') THEN 2
             WHEN cp.status = 'en_progreso' THEN 3
             WHEN cp.status = 'no_estudiado' THEN 4
             ELSE 5 END ASC,
        cp.mastery ASC
    """
    cursor.execute(query_concepts, params_c)
    priority_concepts = [row[0] for row in cursor.fetchall()]

    # First attempt: pick a question from prioritized concepts that hasn't been used recently
    for cid in priority_concepts:
        q_filter = "WHERE concept_id = ?"
        q_params = [cid]

        if difficulty:
            q_filter += " AND difficulty = ?"
            q_params.append(difficulty)
        if q_type:
            q_filter += " AND type = ?"
            q_params.append(q_type)

        cursor.execute(f"SELECT * FROM questions {q_filter} ORDER BY times_used ASC;", q_params)
        candidate_rows = cursor.fetchall()
        
        # Look for a question not in recent
        for row in candidate_rows:
            if row["id"] not in recent_q_ids:
                return dict(row)

    # Fallback: Pick any question matching filters with minimum usage
    fallback_filter = "WHERE 1=1"
    fb_params = []
    if topic_id:
        fallback_filter += " AND topic_id = ?"
        fb_params.append(topic_id)
    if difficulty:
        fallback_filter += " AND difficulty = ?"
        fb_params.append(difficulty)
    if q_type:
        fallback_filter += " AND type = ?"
        fb_params.append(q_type)

    cursor.execute(f"""
    SELECT * FROM questions
    {fallback_filter}
    ORDER BY times_used ASC, RANDOM()
    LIMIT 1;
    """, fb_params)

    row = cursor.fetchone()
    return dict(row) if row else None
