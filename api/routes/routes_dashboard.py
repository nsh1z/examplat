from fastapi import APIRouter
import json
from database import get_db

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("")
def get_dashboard(user_id: str = "default_user"):
    with get_db() as conn:
        cursor = conn.cursor()

        # 1. User info
        cursor.execute("SELECT * FROM users WHERE id = ?;", (user_id,))
        user = dict(cursor.fetchone() or {})

        # 2. Concept mastery statistics
        cursor.execute("""
        SELECT 
            COUNT(*) as total_concepts,
            SUM(CASE WHEN cp.status = 'dominado' OR cp.mastery >= 85 THEN 1 ELSE 0 END) as dominados,
            SUM(CASE WHEN (cp.status = 'en_progreso' OR (cp.mastery >= 40 AND cp.mastery < 85)) AND cp.status != 'debil' THEN 1 ELSE 0 END) as en_progreso,
            SUM(CASE WHEN cp.status = 'debil' OR (cp.incorrect_count > cp.correct_count AND cp.incorrect_count > 0) OR cp.needs_practice_flag = 1 THEN 1 ELSE 0 END) as debiles,
            SUM(CASE WHEN cp.status = 'no_estudiado' AND cp.correct_count = 0 AND cp.incorrect_count = 0 THEN 1 ELSE 0 END) as no_estudiados,
            AVG(cp.mastery) as avg_mastery
        FROM concept_progress cp
        WHERE cp.user_id = ?;
        """, (user_id,))
        stats = dict(cursor.fetchone() or {})
        
        total_concepts = stats.get("total_concepts") or 1
        dominados = stats.get("dominados") or 0
        en_progreso = stats.get("en_progreso") or 0
        debiles = stats.get("debiles") or 0
        no_estudiados = stats.get("no_estudiados") or 0
        avg_mastery = round(stats.get("avg_mastery") or 0.0, 1)

        # 3. Questions statistics
        cursor.execute("""
        SELECT 
            COUNT(*) as total_attempts,
            SUM(is_correct) as total_correct,
            AVG(score) as avg_score
        FROM question_attempts
        WHERE user_id = ?;
        """, (user_id,))
        q_stats = dict(cursor.fetchone() or {})
        total_attempts = q_stats.get("total_attempts") or 0
        total_correct = q_stats.get("total_correct") or 0
        accuracy = round((total_correct / total_attempts * 100.0), 1) if total_attempts > 0 else 0.0

        # 4. Mastery by Unit (Radar / Bar Chart)
        cursor.execute("""
        SELECT 
            t.unit_number,
            AVG(cp.mastery) as unit_mastery,
            COUNT(c.id) as concept_count
        FROM topics t
        JOIN concepts c ON c.topic_id = t.id
        LEFT JOIN concept_progress cp ON cp.concept_id = c.id AND cp.user_id = ?
        GROUP BY t.unit_number
        ORDER BY t.unit_number ASC;
        """, (user_id,))
        unit_progress = []
        for row in cursor.fetchall():
            unit_progress.append({
                "unit": row["unit_number"],
                "mastery": round(row["unit_mastery"] or 0.0, 1),
                "concept_count": row["concept_count"]
            })

        # 5. Continue Studying pointer (Find next recommended concept)
        cursor.execute("""
        SELECT c.id, c.name, t.name as topic_name, t.unit_number
        FROM concepts c
        JOIN topics t ON c.topic_id = t.id
        LEFT JOIN concept_progress cp ON cp.concept_id = c.id AND cp.user_id = ?
        ORDER BY 
            cp.needs_practice_flag DESC,
            CASE WHEN cp.status = 'debil' THEN 1
                 WHEN cp.status = 'en_progreso' THEN 2
                 WHEN cp.status = 'no_estudiado' THEN 3
                 ELSE 4 END ASC,
            cp.mastery ASC
        LIMIT 1;
        """, (user_id,))
        continue_rec = dict(cursor.fetchone() or {})

        # 6. Weak topics list
        cursor.execute("""
        SELECT t.name as topic_name, COUNT(cp.concept_id) as weak_count
        FROM concept_progress cp
        JOIN concepts c ON cp.concept_id = c.id
        JOIN topics t ON c.topic_id = t.id
        WHERE cp.user_id = ? AND (cp.status = 'debil' OR cp.needs_practice_flag = 1)
        GROUP BY t.id
        ORDER BY weak_count DESC
        LIMIT 4;
        """, (user_id,))
        weak_topics = [dict(r) for r in cursor.fetchall()]

        return {
            "user": user,
            "overall_progress_percent": avg_mastery,
            "stats": {
                "total_concepts": total_concepts,
                "dominados": dominados,
                "en_progreso": en_progreso,
                "debiles": debiles,
                "no_estudiados": no_estudiados,
                "total_attempts": total_attempts,
                "total_correct": total_correct,
                "accuracy_percent": accuracy
            },
            "unit_progress": unit_progress,
            "continue_studying": continue_rec,
            "weak_topics": weak_topics
        }
