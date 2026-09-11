from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import uuid
from datetime import datetime
from database import get_db
from services.ai_grader import grade_objective_question, grade_semantic_open_question

router = APIRouter(prefix="/api/exam", tags=["exam"])

class StartExamRequest(BaseModel):
    user_id: str = "default_user"
    num_questions: int = 15
    duration_minutes: int = 45
    topic_ids: Optional[List[str]] = None

class SubmitExamRequest(BaseModel):
    session_id: str
    user_id: str = "default_user"
    answers: Dict[str, str] # question_id -> user_answer
    time_spent_seconds: int = 0

@router.post("/start")
def start_exam(req: StartExamRequest):
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Select questions across topics
        query = "SELECT * FROM questions"
        params = []
        if req.topic_ids:
            placeholders = ",".join("?" for _ in req.topic_ids)
            query += f" WHERE topic_id IN ({placeholders})"
            params.extend(req.topic_ids)
        
        query += " ORDER BY RANDOM() LIMIT ?;"
        params.append(req.num_questions)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        if not rows:
            raise HTTPException(status_code=400, detail="No hay suficientes preguntas para generar el examen.")

        session_id = str(uuid.uuid4())
        cursor.execute("""
        INSERT INTO exam_sessions (id, user_id, total_questions, duration_minutes, started_at)
        VALUES (?, ?, ?, ?, datetime('now'));
        """, (session_id, req.user_id, len(rows), req.duration_minutes))

        client_questions = []
        for r in rows:
            opts = json.loads(r["options"]) if r["options"] else None
            client_questions.append({
                "id": r["id"],
                "topic_id": r["topic_id"],
                "concept_id": r["concept_id"],
                "type": r["type"],
                "difficulty": r["difficulty"],
                "question": r["question"],
                "options": opts,
                "source_document": r["source_document"]
            })

        return {
            "session_id": session_id,
            "total_questions": len(client_questions),
            "duration_minutes": req.duration_minutes,
            "started_at": datetime.now().isoformat(),
            "questions": client_questions
        }

@router.post("/submit")
def submit_exam(req: SubmitExamRequest):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM exam_sessions WHERE id = ?;", (req.session_id,))
        sess = cursor.fetchone()
        if not sess:
            raise HTTPException(status_code=404, detail="Exam session not found")

        total_questions = sess["total_questions"]
        evaluated_questions = []
        topic_scores = {}
        total_score_sum = 0.0
        correct_count = 0

        for q_id, user_ans in req.answers.items():
            cursor.execute("""
            SELECT q.*, c.name as concept_name, c.definition, c.explanation, t.name as topic_name
            FROM questions q
            JOIN concepts c ON q.concept_id = c.id
            JOIN topics t ON q.topic_id = t.id
            WHERE q.id = ?;
            """, (q_id,))
            row = cursor.fetchone()
            if not row:
                continue

            q = dict(row)
            topic_name = q["topic_name"]
            if topic_name not in topic_scores:
                topic_scores[topic_name] = {"correct": 0, "total": 0}
            topic_scores[topic_name]["total"] += 1

            # Grade
            if q["type"] in ["multiple_choice", "true_false", "fill_blank", "matching", "order_steps"]:
                res = grade_objective_question(q["type"], user_ans, q["correct_answer"], q["options"])
            else:
                res = grade_semantic_open_question(user_ans, q["correct_answer"], q)

            score = res["score"]
            total_score_sum += score
            if res["is_correct"]:
                correct_count += 1
                topic_scores[topic_name]["correct"] += 1

            evaluated_questions.append({
                "question_id": q_id,
                "question": q["question"],
                "topic_name": topic_name,
                "concept_name": q["concept_name"],
                "type": q["type"],
                "user_answer": user_ans,
                "model_answer": res["model_answer"],
                "is_correct": res["is_correct"],
                "score": score,
                "explanation": q["explanation"],
                "strengths": res["strengths"],
                "missing": res["missing"]
            })

            # Record attempt
            cursor.execute("""
            INSERT INTO question_attempts (
                user_id, question_id, concept_id, user_answer, is_correct,
                score, ai_feedback, time_seconds, attempt_type, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'exam', datetime('now'));
            """, (
                req.user_id, q_id, q["concept_id"], user_ans, 1 if res["is_correct"] else 0,
                score, json.dumps(res, ensure_ascii=False), req.time_spent_seconds // max(len(req.answers), 1)
            ))

        # Calculate final grade (0.0 to 10.0)
        avg_percentage = (total_score_sum / max(total_questions, 1))
        grade_10 = round((avg_percentage / 10.0), 1)

        # Categorize strengths and weaknesses
        strengths = []
        weaknesses = []
        for t_name, sc in topic_scores.items():
            pct = (sc["correct"] / sc["total"]) * 100.0
            if pct >= 75.0:
                strengths.append(f"{t_name} ({round(pct)}% aciertos)")
            else:
                weaknesses.append(f"{t_name} ({round(pct)}% aciertos)")

        # Update session
        cursor.execute("""
        UPDATE exam_sessions SET
            completed_at = datetime('now'),
            final_score = ?,
            strengths = ?,
            weaknesses = ?,
            answers_snapshot = ?
        WHERE id = ?;
        """, (
            grade_10,
            json.dumps(strengths, ensure_ascii=False),
            json.dumps(weaknesses, ensure_ascii=False),
            json.dumps(evaluated_questions, ensure_ascii=False),
            req.session_id
        ))

        # Award XP for exam completion
        cursor.execute("UPDATE users SET xp = xp + ?, study_time_seconds = study_time_seconds + ? WHERE id = ?;", (100, req.time_spent_seconds, req.user_id))

        passed = grade_10 >= 4.0
        if grade_10 >= 9.0:
            grade_letter = "Sobresaliente (10/10)"
        elif grade_10 >= 7.0:
            grade_letter = "Distinguido"
        elif grade_10 >= 4.0:
            grade_letter = "Aprobado"
        else:
            grade_letter = "Insuficiente (A Recuperatorio)"

        return {
            "session_id": req.session_id,
            "final_score_10": grade_10,
            "final_grade_10": grade_10,
            "passed": passed,
            "grade_letter": grade_letter,
            "percentage": round(avg_percentage, 1),
            "correct_count": correct_count,
            "total_questions": total_questions,
            "time_spent_seconds": req.time_spent_seconds,
            "diagnostic": {
                "strengths": strengths,
                "weaknesses": weaknesses
            },
            "strengths": strengths,
            "weaknesses": weaknesses,
            "details": evaluated_questions,
            "questions_review": evaluated_questions
        }
