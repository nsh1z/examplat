from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Any
import json
from database import get_db
from services.adaptive_engine import get_next_adaptive_question, update_spaced_repetition, calculate_mastery
from services.ai_grader import grade_objective_question, grade_semantic_open_question
from services.tutor_service import explain_differently

router = APIRouter(prefix="/api/practice", tags=["practice"])

class SubmitAnswerRequest(BaseModel):
    user_id: str = "default_user"
    question_id: str
    user_answer: str
    time_seconds: int = 0
    attempt_type: str = "practice" # practice, exam, review

@router.get("/next")
def get_next_question(
    user_id: str = "default_user",
    topic_id: Optional[str] = None,
    difficulty: Optional[str] = None,
    q_type: Optional[str] = None
):
    with get_db() as conn:
        q = get_next_adaptive_question(conn, user_id, topic_id, difficulty, q_type)
        if not q:
            # Fallback if filters are too restrictive: relax difficulty and type
            q = get_next_adaptive_question(conn, user_id, topic_id=topic_id)
            if not q:
                raise HTTPException(status_code=404, detail="No hay más preguntas disponibles para este criterio.")

        # Fetch concept info for context
        cursor = conn.cursor()
        cursor.execute("SELECT name, difficulty FROM concepts WHERE id = ?;", (q["concept_id"],))
        c_row = cursor.fetchone()
        concept_name = c_row["name"] if c_row else ""

        # Parse options if JSON
        options = None
        if q.get("options"):
            try:
                options = json.loads(q["options"])
            except Exception:
                options = q["options"]

        # Safe client response (WITHOUT revealing correct_answer or internal notes)
        return {
            "id": q["id"],
            "topic_id": q["topic_id"],
            "concept_id": q["concept_id"],
            "concept_name": concept_name,
            "type": q["type"],
            "difficulty": q["difficulty"],
            "question": q["question"],
            "options": options,
            "has_hint1": bool(q.get("hint1")),
            "has_hint2": bool(q.get("hint2")),
            "source_document": q["source_document"],
            "source_page": q["source_page"]
        }

@router.post("/submit")
def submit_answer(req: SubmitAnswerRequest):
    with get_db() as conn:
        cursor = conn.cursor()

        # 1. Fetch question and concept
        cursor.execute("SELECT * FROM questions WHERE id = ?;", (req.question_id,))
        q_row = cursor.fetchone()
        if not q_row:
            raise HTTPException(status_code=404, detail="Question not found")
        q = dict(q_row)

        cursor.execute("SELECT * FROM concepts WHERE id = ?;", (q["concept_id"],))
        c_row = cursor.fetchone()
        concept = dict(c_row) if c_row else {}

        # 2. Grade answer
        q_type = q["type"]
        if q_type in ["multiple_choice", "true_false", "fill_blank", "matching", "order_steps"]:
            grade = grade_objective_question(q_type, req.user_answer, q["correct_answer"], q.get("options"))
        else: # open_question, practical_case
            grade = grade_semantic_open_question(req.user_answer, q["correct_answer"], concept)

        score = grade["score"]
        is_correct = 1 if grade["is_correct"] else 0

        # 3. Record attempt
        cursor.execute("""
        INSERT INTO question_attempts (
            user_id, question_id, concept_id, user_answer, is_correct,
            score, ai_feedback, time_seconds, attempt_type, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'));
        """, (
            req.user_id, req.question_id, q["concept_id"], req.user_answer, is_correct,
            score, json.dumps(grade, ensure_ascii=False), req.time_seconds, req.attempt_type
        ))

        # 4. Update question stats
        cursor.execute("""
        UPDATE questions SET
            times_used = times_used + 1,
            times_correct = times_correct + ?,
            times_incorrect = times_incorrect + ?
        WHERE id = ?;
        """, (1 if is_correct else 0, 0 if is_correct else 1, req.question_id))

        # 5. Update Concept Progress & SM-2 Spaced Repetition
        cursor.execute("SELECT * FROM concept_progress WHERE user_id = ? AND concept_id = ?;", (req.user_id, q["concept_id"]))
        prog_row = cursor.fetchone()

        if prog_row:
            c_int = prog_row["interval_days"] or 1.0
            c_ef = prog_row["ease_factor"] or 2.5
            corr_cnt = prog_row["correct_count"] + (1 if is_correct else 0)
            incorr_cnt = prog_row["incorrect_count"] + (0 if is_correct else 1)
        else:
            c_int, c_ef, corr_cnt, incorr_cnt = 1.0, 2.5, (1 if is_correct else 0), (0 if is_correct else 1)

        new_int, new_ef, next_rev = update_spaced_repetition(c_int, c_ef, score)

        # Get recent attempts for trend mastery
        cursor.execute("""
        SELECT score FROM question_attempts
        WHERE user_id = ? AND concept_id = ?
        ORDER BY created_at DESC LIMIT 5;
        """, (req.user_id, q["concept_id"]))
        recent_scores = [{"score": r[0]} for r in cursor.fetchall()]
        new_mastery = calculate_mastery(corr_cnt, incorr_cnt, recent_scores)

        # Determine new status
        if new_mastery >= 85:
            new_status = "dominado"
        elif not is_correct or incorr_cnt > corr_cnt:
            new_status = "debil"
        elif new_mastery >= 40:
            new_status = "en_progreso"
        else:
            new_status = "debil"

        cursor.execute("""
        INSERT INTO concept_progress (
            user_id, concept_id, mastery, status, correct_count, incorrect_count,
            last_attempt_at, next_review_at, interval_days, ease_factor, needs_practice_flag
        ) VALUES (?, ?, ?, ?, ?, ?, datetime('now'), ?, ?, ?, ?)
        ON CONFLICT(user_id, concept_id) DO UPDATE SET
            mastery = excluded.mastery,
            status = excluded.status,
            correct_count = excluded.correct_count,
            incorrect_count = excluded.incorrect_count,
            last_attempt_at = excluded.last_attempt_at,
            next_review_at = excluded.next_review_at,
            interval_days = excluded.interval_days,
            ease_factor = excluded.ease_factor,
            needs_practice_flag = CASE WHEN excluded.status = 'debil' THEN 1 ELSE 0 END;
        """, (
            req.user_id, q["concept_id"], new_mastery, new_status, corr_cnt, incorr_cnt,
            next_rev, new_int, new_ef, 1 if new_status == 'debil' else 0
        ))

        # 6. Award User XP & update study stats
        xp_gain = 25 if is_correct else 10
        cursor.execute("""
        UPDATE users SET
            xp = xp + ?,
            study_time_seconds = study_time_seconds + ?,
            level = (xp + ?) / 150 + 1,
            last_study_date = date('now')
        WHERE id = ?;
        """, (xp_gain, req.time_seconds, xp_gain, req.user_id))

        return {
            "result": grade,
            "xp_earned": xp_gain,
            "concept_progress": {
                "concept_id": q["concept_id"],
                "new_mastery": new_mastery,
                "status": new_status,
                "next_review": next_rev
            },
            "explanation": q["explanation"],
            "source_citation": f"{q['source_document']} — {q['source_page']}"
        }

@router.get("/hint/{question_id}/{hint_num}")
def get_hint(question_id: str, hint_num: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT hint1, hint2 FROM questions WHERE id = ?;", (question_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Question not found")
        
        hint_text = row["hint1"] if hint_num == 1 else row["hint2"]
        if not hint_text:
            hint_text = "No hay pistas adicionales para esta pregunta."
        return {"hint_num": hint_num, "hint": hint_text}

@router.get("/explain-differently/{concept_id}")
def explain_concept_differently(concept_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM concepts WHERE id = ?;", (concept_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Concept not found")
        return explain_differently(dict(row))
