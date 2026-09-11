from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json
from database import get_db

router = APIRouter(prefix="/api/theory", tags=["theory"])

class ConceptFeedback(BaseModel):
    user_id: str = "default_user"
    action: str # "entendido" or "practicar"

class ConceptNote(BaseModel):
    user_id: str = "default_user"
    note_text: str

@router.get("/units")
def get_units(user_id: str = "default_user"):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT 
            t.unit_number,
            t.id as topic_id,
            t.name as topic_name,
            t.description as topic_description,
            t.icon,
            COUNT(c.id) as concept_count,
            AVG(COALESCE(cp.mastery, 0)) as topic_mastery
        FROM topics t
        LEFT JOIN concepts c ON c.topic_id = t.id
        LEFT JOIN concept_progress cp ON cp.concept_id = c.id AND cp.user_id = ?
        GROUP BY t.id
        ORDER BY t.unit_number ASC, t.order_idx ASC;
        """, (user_id,))
        rows = cursor.fetchall()

        units_map = {}
        UNIT_TITLES = {
            1: "Fundamentos de la Ingeniería de Datos y SGBD",
            2: "Modelado Conceptual: DER y EER Extendido",
            3: "El Modelo Relacional y las 12 Reglas de Codd",
            4: "Álgebra Relacional Procedimental",
            5: "Metodología Sistemática de Mapeo DER/EER a Relacional",
            6: "Lenguaje SQL: Definición de Datos y Restricciones (DDL)",
            7: "Lenguaje SQL: Consultas, Manipulación y Transacciones (DML, TCL)",
            8: "Casos de Estudio y Práctica Integral de Cátedra"
        }

        for r in rows:
            u_num = r["unit_number"]
            if u_num not in units_map:
                units_map[u_num] = {
                    "unit_number": u_num,
                    "title": UNIT_TITLES.get(u_num, f"Unidad {u_num}"),
                    "topics": [],
                    "total_concepts": 0
                }
            units_map[u_num]["topics"].append({
                "id": r["topic_id"],
                "name": r["topic_name"],
                "description": r["topic_description"],
                "icon": r["icon"],
                "concept_count": r["concept_count"],
                "mastery": round(r["topic_mastery"] or 0.0, 1)
            })
            units_map[u_num]["total_concepts"] += r["concept_count"]

        return list(units_map.values())

@router.get("/topics/{topic_id}")
def get_topic_detail(topic_id: str, user_id: str = "default_user"):
    with get_db() as conn:
        cursor = conn.cursor()
        # Topic info
        cursor.execute("SELECT * FROM topics WHERE id = ?;", (topic_id,))
        topic_row = cursor.fetchone()
        if not topic_row:
            raise HTTPException(status_code=404, detail="Topic not found")
        topic = dict(topic_row)

        # Concepts in topic
        cursor.execute("""
        SELECT c.*, 
               COALESCE(cp.mastery, 0.0) as user_mastery,
               COALESCE(cp.status, 'no_estudiado') as user_status,
               COALESCE(cp.needs_practice_flag, 0) as needs_practice_flag,
               un.note_text
        FROM concepts c
        LEFT JOIN concept_progress cp ON cp.concept_id = c.id AND cp.user_id = ?
        LEFT JOIN concept_user_notes un ON un.concept_id = c.id AND un.user_id = ?
        WHERE c.topic_id = ?
        ORDER BY c.order_idx ASC;
        """, (user_id, user_id, topic_id))

        concepts = []
        for r in cursor.fetchall():
            c_dict = dict(r)
            if c_dict.get("related_concepts"):
                try:
                    c_dict["related_concepts"] = json.loads(c_dict["related_concepts"])
                except Exception:
                    pass
            concepts.append(c_dict)

        topic["concepts"] = concepts
        return topic

@router.post("/concept/{concept_id}/feedback")
def set_concept_feedback(concept_id: str, feedback: ConceptFeedback):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM concept_progress WHERE user_id = ? AND concept_id = ?;", (feedback.user_id, concept_id))
        row = cursor.fetchone()

        if feedback.action == "entendido":
            # Boost mastery slightly and clear needs_practice_flag
            new_mastery = min(100.0, (row["mastery"] + 20.0) if row else 60.0)
            cursor.execute("""
            INSERT INTO concept_progress (user_id, concept_id, mastery, status, needs_practice_flag, last_attempt_at)
            VALUES (?, ?, ?, 'en_progreso', 0, datetime('now'))
            ON CONFLICT(user_id, concept_id) DO UPDATE SET
                mastery = ?,
                needs_practice_flag = 0,
                status = CASE WHEN ? >= 85 THEN 'dominado' ELSE 'en_progreso' END,
                last_attempt_at = datetime('now');
            """, (feedback.user_id, concept_id, new_mastery, new_mastery, new_mastery))
            return {"status": "success", "message": "¡Concepto marcado como entendido!", "mastery": new_mastery}

        elif feedback.action == "practicar":
            # Set high priority in adaptive practice
            cursor.execute("""
            INSERT INTO concept_progress (user_id, concept_id, mastery, status, needs_practice_flag, last_attempt_at)
            VALUES (?, ?, 20.0, 'debil', 1, datetime('now'))
            ON CONFLICT(user_id, concept_id) DO UPDATE SET
                needs_practice_flag = 1,
                status = 'debil',
                last_attempt_at = datetime('now');
            """, (feedback.user_id, concept_id))
            return {"status": "success", "message": "Prioridad de práctica elevada para este concepto.", "needs_practice": True}

@router.post("/concept/{concept_id}/note")
def save_concept_note(concept_id: str, note: ConceptNote):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO concept_user_notes (user_id, concept_id, note_text, updated_at)
        VALUES (?, ?, ?, datetime('now'))
        ON CONFLICT(user_id, concept_id) DO UPDATE SET
            note_text = excluded.note_text,
            updated_at = datetime('now');
        """, (note.user_id, concept_id, note.note_text))
        return {"status": "success", "message": "Nota guardada correctamente."}
