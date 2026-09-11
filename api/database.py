import sqlite3
import os
import shutil
import json
from pathlib import Path
from contextlib import contextmanager

BASE_DIR = Path(__file__).resolve().parent

# If running on Vercel or AWS Lambda serverless function:
if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
    DB_PATH = Path("/tmp/plataforma.db")
    if not DB_PATH.exists():
        src_db = BASE_DIR / "plataforma.db"
        if src_db.exists():
            try:
                shutil.copy2(src_db, DB_PATH)
            except Exception as e:
                print(f"Error copying DB to /tmp: {e}")
else:
    DB_PATH = BASE_DIR / "plataforma.db"

def get_connection():
    # Fallback and auto-sync if in Vercel and source DB is updated
    if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        src_db = BASE_DIR / "plataforma.db"
        if src_db.exists():
            try:
                if not DB_PATH.exists() or src_db.stat().st_size != DB_PATH.stat().st_size or src_db.stat().st_mtime > DB_PATH.stat().st_mtime:
                    shutil.copy2(src_db, DB_PATH)
            except Exception as e:
                print(f"Error syncing DB to /tmp: {e}")
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Users
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            streak_days INTEGER DEFAULT 1,
            last_study_date TEXT,
            study_time_seconds INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # Insert default user if not exists
        cursor.execute("SELECT id FROM users WHERE id = 'default_user';")
        if not cursor.fetchone():
            cursor.execute("""
            INSERT INTO users (id, name, email, xp, level, streak_days, last_study_date, study_time_seconds)
            VALUES ('default_user', 'Estudiante UADE', 'estudiante@uade.edu.ar', 0, 1, 1, date('now'), 0);
            """)

        # 2. Topics
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id TEXT PRIMARY KEY,
            unit_number INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            icon TEXT,
            order_idx INTEGER NOT NULL
        );
        """)
        
        # 3. Concepts
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS concepts (
            id TEXT PRIMARY KEY,
            topic_id TEXT NOT NULL,
            name TEXT NOT NULL,
            definition TEXT NOT NULL,
            explanation TEXT NOT NULL,
            simple_explanation TEXT NOT NULL,
            example TEXT,
            related_concepts TEXT, -- JSON array of concept names/IDs
            common_confusions TEXT,
            difficulty TEXT DEFAULT 'medio', -- facil, medio, dificil, experto
            source_document TEXT NOT NULL,
            source_page TEXT,
            order_idx INTEGER DEFAULT 0,
            FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
        );
        """)

        # 4. Questions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id TEXT PRIMARY KEY,
            topic_id TEXT NOT NULL,
            concept_id TEXT NOT NULL,
            type TEXT NOT NULL, -- multiple_choice, true_false, fill_blank, matching, order_steps, open_question, practical_case
            difficulty TEXT NOT NULL, -- facil, medio, dificil, experto
            question TEXT NOT NULL,
            options TEXT, -- JSON array of options for multiple choice / matching / order
            correct_answer TEXT NOT NULL, -- exact answer or JSON for matching/order
            explanation TEXT NOT NULL,
            hint1 TEXT,
            hint2 TEXT,
            source_document TEXT NOT NULL,
            source_page TEXT,
            semantic_hash TEXT,
            times_used INTEGER DEFAULT 0,
            times_correct INTEGER DEFAULT 0,
            times_incorrect INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE,
            FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE
        );
        """)

        # 5. Question Attempts (Historial de respuestas)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS question_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            question_id TEXT NOT NULL,
            concept_id TEXT NOT NULL,
            user_answer TEXT,
            is_correct INTEGER NOT NULL, -- 1=correct, 0=incorrect
            score REAL NOT NULL, -- 0 to 100
            ai_feedback TEXT, -- JSON with feedback: score, strengths, missing, confusion, model_answer, tips
            time_seconds INTEGER DEFAULT 0,
            attempt_type TEXT DEFAULT 'practice', -- practice, exam, review
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
            FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE
        );
        """)

        # 6. Concept Progress (Sistema de Dominio y Repetición Espaciada SM-2)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS concept_progress (
            user_id TEXT NOT NULL,
            concept_id TEXT NOT NULL,
            mastery REAL DEFAULT 0.0, -- 0.0 to 100.0
            status TEXT DEFAULT 'no_estudiado', -- no_estudiado, en_progreso, debil, dominado
            correct_count INTEGER DEFAULT 0,
            incorrect_count INTEGER DEFAULT 0,
            last_attempt_at TEXT,
            next_review_at TEXT, -- ISO Date for spaced repetition
            interval_days REAL DEFAULT 1.0,
            ease_factor REAL DEFAULT 2.5,
            needs_practice_flag INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, concept_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE
        );
        """)

        # 7. Exam Sessions (Simulacros de Examen)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS exam_sessions (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            total_questions INTEGER NOT NULL,
            duration_minutes INTEGER NOT NULL,
            started_at TEXT DEFAULT CURRENT_TIMESTAMP,
            completed_at TEXT,
            final_score REAL,
            strengths TEXT, -- JSON array of mastered topics
            weaknesses TEXT, -- JSON array of weak topics
            answers_snapshot TEXT, -- JSON snapshot of questions and answers
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # 8. User Concept Notes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS concept_user_notes (
            user_id TEXT NOT NULL,
            concept_id TEXT NOT NULL,
            note_text TEXT NOT NULL,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, concept_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE
        );
        """)

        # 9. System Config (API keys, settings)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_config (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        """)

        # Default configs
        cursor.execute("INSERT OR IGNORE INTO system_config (key, value) VALUES ('dark_mode', 'false');")
        cursor.execute("INSERT OR IGNORE INTO system_config (key, value) VALUES ('gemini_api_key', '');")
        cursor.execute("INSERT OR IGNORE INTO system_config (key, value) VALUES ('openai_api_key', '');")
        cursor.execute("INSERT OR IGNORE INTO system_config (key, value) VALUES ('active_user', 'default_user');")

        # Indexes for rapid querying and anti-repetition lookup
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_concepts_topic ON concepts(topic_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_concept ON questions(concept_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_type ON questions(type);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_attempts_user ON question_attempts(user_id, question_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_attempts_created ON question_attempts(created_at);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_progress_review ON concept_progress(user_id, next_review_at);")

if __name__ == "__main__":
    init_db()
    print("Database schema successfully initialized at:", DB_PATH)
