from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
from database import get_db

router = APIRouter(prefix="/api/admin", tags=["admin"])

class QuestionEditRequest(BaseModel):
    topic_id: str
    concept_id: str
    type: str
    difficulty: str
    question: str
    options: Optional[Any] = None
    correct_answer: str
    explanation: str
    hint1: Optional[str] = ""
    hint2: Optional[str] = ""
    source_document: str
    source_page: Optional[str] = ""

class ConfigUpdateRequest(BaseModel):
    key: str
    value: str

DOCUMENTS_AUDIT = [
    {
        "num": 1,
        "filename": "Clase nro 1 Ingeniería de Datos 1.pdf",
        "pages": 48,
        "main_topic": "Dato/Información, Archivos, SGBD, ACID, ANSI/SPARC, 14 Pasos, Usuarios DBA/DA",
        "unit": 1,
        "concepts_count": 8,
        "status": "Fuente Oficial (Unidad 1)"
    },
    {
        "num": 2,
        "filename": "Diagramas de Entidad Relación y Modelo de Datos.pdf",
        "pages": 28,
        "main_topic": "DER Chen/Crow's Foot, Entidades Débiles, Cardinalidades, Reglas, Caso Constructora",
        "unit": 2,
        "concepts_count": 8,
        "status": "Fuente Oficial (Unidad 2)"
    },
    {
        "num": 3,
        "filename": "Clase nro 11 - Mássss DER.pdf",
        "pages": 58,
        "main_topic": "Modelo EER Extendido, Especialización/Generalización, d/o, Total/Parcial, Mapeo 1-8, Jerarquías A-D",
        "unit": "3 y 6",
        "concepts_count": 13,
        "status": "Fuente Oficial (Unidades 3 y 6)"
    },
    {
        "num": 4,
        "filename": "El Modelo Relacional.pdf",
        "pages": 34,
        "main_topic": "Estructura Relacional, Tuplas, Claves (Candidata, Primaria, Foránea), Integridad, 12 Reglas de Codd",
        "unit": 4,
        "concepts_count": 7,
        "status": "Fuente Oficial (Unidad 4)"
    },
    {
        "num": 5,
        "filename": "Algebra Relacional.pdf",
        "pages": 1,
        "main_topic": "16 Consultas Formales: σ, π, ×, ⋈, Theta Join, ∪, ∩, -, ÷ (Almacenes/Proveedores)",
        "unit": 5,
        "concepts_count": 7,
        "status": "Fuente Oficial (Unidad 5)"
    }
]

@router.get("/documents")
def get_documents():
    return DOCUMENTS_AUDIT

@router.get("/stats")
def get_admin_stats():
    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM topics;")
        total_topics = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM concepts;")
        total_concepts = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM questions;")
        total_questions = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM question_attempts;")
        total_attempts = cursor.fetchone()[0]

        # By Type
        cursor.execute("SELECT type, COUNT(*) as count FROM questions GROUP BY type;")
        by_type = {row[0]: row[1] for row in cursor.fetchall()}

        # By Difficulty
        cursor.execute("SELECT difficulty, COUNT(*) as count FROM questions GROUP BY difficulty;")
        by_difficulty = {row[0]: row[1] for row in cursor.fetchall()}

        # High Error Rate Questions
        cursor.execute("""
        SELECT q.id, q.question, q.type, q.difficulty, q.times_used, q.times_incorrect,
               ROUND(CAST(q.times_incorrect AS REAL) / MAX(q.times_used, 1) * 100, 1) as error_rate
        FROM questions q
        WHERE q.times_used > 0
        ORDER BY error_rate DESC, q.times_used DESC
        LIMIT 5;
        """)
        difficult_questions = [dict(r) for r in cursor.fetchall()]

        # Duplicate check (identical semantic_hash or text)
        cursor.execute("""
        SELECT semantic_hash, COUNT(*) as count
        FROM questions
        WHERE semantic_hash IS NOT NULL AND semantic_hash != ''
        GROUP BY semantic_hash
        HAVING count > 1;
        """)
        duplicates = [row[0] for row in cursor.fetchall()]

        return {
            "total_topics": total_topics,
            "total_concepts": total_concepts,
            "total_questions": total_questions,
            "total_attempts": total_attempts,
            "questions_by_type": by_type,
            "questions_by_difficulty": by_difficulty,
            "difficult_questions": difficult_questions,
            "duplicate_hashes_found": duplicates
        }

@router.get("/questions")
def list_questions(
    topic_id: Optional[str] = None,
    q_type: Optional[str] = None,
    difficulty: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    with get_db() as conn:
        cursor = conn.cursor()
        filters = []
        params = []
        if topic_id:
            filters.append("q.topic_id = ?")
            params.append(topic_id)
        if q_type:
            filters.append("q.type = ?")
            params.append(q_type)
        if difficulty:
            filters.append("q.difficulty = ?")
            params.append(difficulty)

        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
        sql = f"""
        SELECT q.*, c.name as concept_name, t.name as topic_name
        FROM questions q
        JOIN concepts c ON q.concept_id = c.id
        JOIN topics t ON q.topic_id = t.id
        {where_clause}
        ORDER BY q.created_at DESC
        LIMIT ? OFFSET ?;
        """
        params.extend([limit, offset])
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        
        result = []
        for r in rows:
            d = dict(r)
            if d.get("options"):
                try:
                    d["options"] = json.loads(d["options"])
                except Exception:
                    pass
            result.append(d)
        return result

@router.delete("/questions/{q_id}")
def delete_question(q_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM questions WHERE id = ?;", (q_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Question not found")
        return {"status": "success", "message": f"Pregunta {q_id} eliminada correctamente."}

@router.get("/config")
def get_config():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM system_config;")
        return {r["key"]: r["value"] for r in cursor.fetchall()}

@router.post("/config")
def set_config(req: ConfigUpdateRequest):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO system_config (key, value) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value;
        """, (req.key, req.value))
        return {"status": "success", "message": f"Configuración '{req.key}' actualizada."}
