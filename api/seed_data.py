import json
import sys
import os
from pathlib import Path

# Add backend directory to sys.path
BACKEND_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BACKEND_DIR))

from database import init_db, get_db
from data.unit1 import TOPICS as U1_TOPICS, CONCEPTS as U1_CONCEPTS, QUESTIONS as U1_QUESTIONS
from data.unit2 import TOPICS as U2_TOPICS, CONCEPTS as U2_CONCEPTS, QUESTIONS as U2_QUESTIONS
from data.unit3 import TOPICS as U3_TOPICS, CONCEPTS as U3_CONCEPTS, QUESTIONS as U3_QUESTIONS
from data.unit4 import TOPICS as U4_TOPICS, CONCEPTS as U4_CONCEPTS, QUESTIONS as U4_QUESTIONS
from data.unit5 import TOPICS as U5_TOPICS, CONCEPTS as U5_CONCEPTS, QUESTIONS as U5_QUESTIONS
from data.unit6 import TOPICS as U6_TOPICS, CONCEPTS as U6_CONCEPTS, QUESTIONS as U6_QUESTIONS
from data.data_cases_exams import ALGEBRA_16_QUESTIONS, EXAM_BANK_EXTRA_QUESTIONS

# Strictly calibrated to the 5 official course presentations:
# 1. Clase nro 1 Ingeniería de Datos 1.pdf
# 2. Diagramas de Entidad Relación y Modelo de Datos.pdf
# 3. Clase nro 11 - Mássss DER.pdf (EER y Mapeo)
# 4. El Modelo Relacional.pdf
# 5. Algebra Relacional.pdf
ALL_TOPICS = (
    U1_TOPICS + U2_TOPICS + U3_TOPICS + U4_TOPICS + U5_TOPICS + U6_TOPICS
)

ALL_CONCEPTS = (
    U1_CONCEPTS + U2_CONCEPTS + U3_CONCEPTS + U4_CONCEPTS + U5_CONCEPTS + U6_CONCEPTS
)

ALL_QUESTIONS = (
    U1_QUESTIONS + U2_QUESTIONS + U3_QUESTIONS + U4_QUESTIONS + U5_QUESTIONS + U6_QUESTIONS +
    ALGEBRA_16_QUESTIONS + EXAM_BANK_EXTRA_QUESTIONS
)

def seed_database():
    print("Ensuring database schema...")
    init_db()

    with get_db() as conn:
        cursor = conn.cursor()

        # Temporarily disable foreign keys to safely clean old schema
        cursor.execute("PRAGMA foreign_keys = OFF;")
        cursor.execute("DELETE FROM question_attempts;")
        cursor.execute("DELETE FROM concept_progress;")
        cursor.execute("DELETE FROM concept_user_notes;")
        cursor.execute("DELETE FROM exam_sessions;")
        cursor.execute("DELETE FROM questions;")
        cursor.execute("DELETE FROM concepts;")
        cursor.execute("DELETE FROM topics;")
        cursor.execute("PRAGMA foreign_keys = ON;")

        # 1. Seed Topics
        print(f"Seeding {len(ALL_TOPICS)} topics across the 6 official units...")
        for t in ALL_TOPICS:
            cursor.execute("""
            INSERT OR REPLACE INTO topics (id, unit_number, name, description, icon, order_idx)
            VALUES (?, ?, ?, ?, ?, ?);
            """, (t["id"], t["unit_number"], t["name"], t.get("description", ""), t.get("icon", "Folder"), t["order_idx"]))

        # 2. Seed Concepts
        print(f"Seeding {len(ALL_CONCEPTS)} structured concepts with academic citations...")
        for c in ALL_CONCEPTS:
            related_json = json.dumps(c.get("related_concepts", []), ensure_ascii=False)
            cursor.execute("""
            INSERT OR REPLACE INTO concepts (
                id, topic_id, name, definition, explanation, simple_explanation,
                example, related_concepts, common_confusions, difficulty,
                source_document, source_page, order_idx
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                c["id"], c["topic_id"], c["name"], c["definition"], c.get("explanation", ""),
                c.get("simple_explanation", ""), c.get("example", ""), related_json,
                c.get("common_confusions", ""), c.get("difficulty", "medio"),
                c.get("source_document", "Programa Oficial"), c.get("source_page", "1"),
                c.get("order_idx", 1)
            ))

        # 3. Seed Calibrated Questions
        print(f"Seeding {len(ALL_QUESTIONS)} calibrated questions...")
        for q in ALL_QUESTIONS:
            options_json = json.dumps(q.get("options", []), ensure_ascii=False)
            cursor.execute("""
            INSERT OR REPLACE INTO questions (
                id, topic_id, concept_id, type, difficulty, question, options,
                correct_answer, explanation, hint1, hint2, source_document,
                source_page, semantic_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                q["id"], q["topic_id"], q["concept_id"], q["type"], q.get("difficulty", "medio"),
                q["question"], options_json, q["correct_answer"], q.get("explanation", ""),
                q.get("hint1", ""), q.get("hint2", ""), q.get("source_document", "Programa Oficial"),
                q.get("source_page", "1"), q.get("semantic_hash", "")
            ))

        # 4. Ensure default user exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE id = 'default_user';")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
            INSERT INTO users (id, name, email, xp, level, streak_days, study_time_seconds)
            VALUES ('default_user', 'Estudiante', 'alumno@uade.edu.ar', 0, 1, 1, 0);
            """)

        conn.commit()
        print(f"Database successfully calibrated: {len(ALL_TOPICS)} topics, {len(ALL_CONCEPTS)} concepts, {len(ALL_QUESTIONS)} questions.")

if __name__ == "__main__":
    seed_database()
