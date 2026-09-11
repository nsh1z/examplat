from fastapi import APIRouter
import json
from database import get_db

router = APIRouter(prefix="/api/errors", tags=["errors"])

@router.get("")
def get_errors(user_id: str = "default_user"):
    with get_db() as conn:
        cursor = conn.cursor()

        # 1. Fetch concepts with errors or marked as weak
        cursor.execute("""
        SELECT 
            c.id as concept_id,
            c.name as concept_name,
            c.topic_id,
            t.name as topic_name,
            t.unit_number,
            c.common_confusions,
            c.definition,
            c.simple_explanation,
            c.source_document,
            c.source_page,
            cp.mastery,
            cp.status,
            cp.correct_count,
            cp.incorrect_count,
            cp.needs_practice_flag,
            cp.last_attempt_at
        FROM concept_progress cp
        JOIN concepts c ON cp.concept_id = c.id
        JOIN topics t ON c.topic_id = t.id
        WHERE cp.user_id = ? AND (cp.incorrect_count > 0 OR cp.status = 'debil' OR cp.needs_practice_flag = 1)
        ORDER BY cp.incorrect_count DESC, cp.mastery ASC;
        """, (user_id,))
        rows = cursor.fetchall()

        errors_list = []
        for r in rows:
            cid = r["concept_id"]

            # Fetch up to 3 recent failed attempts for this concept
            cursor.execute("""
            SELECT qa.id, qa.user_answer, qa.score, qa.created_at, q.question, q.type, q.correct_answer, qa.ai_feedback
            FROM question_attempts qa
            JOIN questions q ON qa.question_id = q.id
            WHERE qa.user_id = ? AND qa.concept_id = ? AND qa.is_correct = 0
            ORDER BY qa.created_at DESC
            LIMIT 3;
            """, (user_id, cid))
            
            recent_fails = []
            for f in cursor.fetchall():
                feedback = json.loads(f["ai_feedback"]) if f["ai_feedback"] else {}
                recent_fails.append({
                    "attempt_id": f["id"],
                    "question": f["question"],
                    "type": f["type"],
                    "user_answer": f["user_answer"],
                    "correct_answer": f["correct_answer"],
                    "score": f["score"],
                    "feedback": feedback,
                    "date": f["created_at"]
                })

            errors_list.append({
                "concept_id": cid,
                "concept_name": r["concept_name"],
                "topic_id": r["topic_id"],
                "topic_name": r["topic_name"],
                "unit_number": r["unit_number"],
                "common_confusions": r["common_confusions"],
                "definition": r["definition"],
                "simple_explanation": r["simple_explanation"],
                "source_document": r["source_document"],
                "source_page": r["source_page"],
                "source": f"{r['source_document']} — {r['source_page']}",
                "mastery": round(r["mastery"] or 0.0, 1),
                "status": r["status"],
                "correct_count": r["correct_count"],
                "incorrect_count": r["incorrect_count"],
                "recent_failed_attempts": recent_fails
            })

        # 2. Fetch overall recent failed attempts for user history
        cursor.execute("""
        SELECT qa.id, qa.question_id, q.question as question_text, qa.user_answer,
               c.name as concept_name, qa.score, qa.created_at as timestamp, q.explanation
        FROM question_attempts qa
        JOIN questions q ON qa.question_id = q.id
        JOIN concepts c ON qa.concept_id = c.id
        WHERE qa.user_id = ? AND qa.is_correct = 0
        ORDER BY qa.created_at DESC
        LIMIT 20;
        """, (user_id,))
        recent_failures = []
        for f in cursor.fetchall():
            recent_failures.append({
                "id": str(f["id"]),
                "question_id": f["question_id"],
                "question_text": f["question_text"],
                "user_answer": f["user_answer"],
                "concept_name": f["concept_name"],
                "score": f["score"],
                "timestamp": f["timestamp"],
                "explanation": f["explanation"] or ""
            })

        return {
            "weak_concepts": errors_list,
            "recent_failures": recent_failures
        }
