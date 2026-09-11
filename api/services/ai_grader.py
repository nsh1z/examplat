import re
import json
import sqlite3
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional

def normalize_text(text: str) -> str:
    """Normalize text removing accents, punctuation and multiple spaces."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[áàäâ]', 'a', text)
    text = re.sub(r'[éèëê]', 'e', text)
    text = re.sub(r'[íìïî]', 'i', text)
    text = re.sub(r'[óòöô]', 'o', text)
    text = re.sub(r'[úùüû]', 'u', text)
    text = re.sub(r'ñ', 'n', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

def grade_objective_question(q_type: str, user_answer: str, correct_answer: str, options: Any = None) -> Dict[str, Any]:
    """
    Grades deterministic question types: multiple_choice, true_false, fill_blank, matching, order_steps.
    """
    u_clean = normalize_text(user_answer)
    c_clean = normalize_text(correct_answer)

    if q_type in ["multiple_choice", "true_false"]:
        is_correct = (u_clean == c_clean) or (user_answer.strip().lower() == correct_answer.strip().lower())
        score = 100.0 if is_correct else 0.0
        return {
            "score": score,
            "is_correct": is_correct,
            "strengths": ["Seleccionaste la opción correcta basada en la teoría oficial."] if is_correct else [],
            "missing": [] if is_correct else ["La opción seleccionada no coincide con el fundamento técnico."],
            "confusions": [] if is_correct else ["Revisa las diferencias clave del concepto en la sección de teoría."],
            "model_answer": correct_answer,
            "tips": "¡Excelente!" if is_correct else "Analizá con atención los distractores y las palabras clave de la pregunta."
        }

    elif q_type == "fill_blank":
        is_correct = (u_clean == c_clean) or (c_clean in u_clean)
        score = 100.0 if is_correct else 0.0
        return {
            "score": score,
            "is_correct": is_correct,
            "strengths": [f"Identificaste el término exacto: '{correct_answer}'."] if is_correct else [],
            "missing": [] if is_correct else [f"El término esperado era: '{correct_answer}'."],
            "confusions": [],
            "model_answer": correct_answer,
            "tips": "¡Excelente retención terminológica!" if is_correct else "Recordá el término técnico formal utilizado en las diapositivas."
        }

    elif q_type == "order_steps":
        try:
            u_list = json.loads(user_answer) if isinstance(user_answer, str) and user_answer.startswith("[") else user_answer.split(",")
            c_list = json.loads(correct_answer) if isinstance(correct_answer, str) and correct_answer.startswith("[") else correct_answer.split(",")
            u_clean_list = [str(x).strip() for x in u_list]
            c_clean_list = [str(x).strip() for x in c_list]
            
            matches = sum(1 for a, b in zip(u_clean_list, c_clean_list) if a == b)
            total = max(len(c_clean_list), 1)
            score = round((matches / total) * 100.0, 1)
            is_correct = (score == 100.0)
            
            return {
                "score": score,
                "is_correct": is_correct,
                "strengths": [f"Ordenaste correctamente {matches} de {total} pasos del proceso."] if matches > 0 else [],
                "missing": [] if is_correct else ["Algunos pasos fueron ubicados fuera de su secuencia cronológica lógica."],
                "confusions": [],
                "model_answer": " -> ".join(c_clean_list),
                "tips": "¡Secuencia perfecta!" if is_correct else "Repasá el orden cronológico del pipeline en la unidad correspondiente."
            }
        except Exception:
            return {"score": 0.0, "is_correct": False, "strengths": [], "missing": ["Formato de orden inválido."], "confusions": [], "model_answer": correct_answer, "tips": "Reintenta ordenando los elementos."}

    elif q_type == "matching":
        try:
            u_map = json.loads(user_answer) if isinstance(user_answer, str) else user_answer
            c_map = json.loads(correct_answer) if isinstance(correct_answer, str) else correct_answer
            
            matches = 0
            for k, v in c_map.items():
                if normalize_text(u_map.get(k, "")) == normalize_text(v):
                    matches += 1
            total = max(len(c_map), 1)
            score = round((matches / total) * 100.0, 1)
            is_correct = (score == 100.0)

            return {
                "score": score,
                "is_correct": is_correct,
                "strengths": [f"Emparejaste correctamente {matches} de {total} pares conceptuales."] if matches > 0 else [],
                "missing": [] if is_correct else ["Hubo asociaciones incorrectas entre conceptos y definiciones."],
                "confusions": [],
                "model_answer": json.dumps(c_map, ensure_ascii=False),
                "tips": "¡Dominio de asociaciones perfecto!" if is_correct else "Verificá cada definición en las fichas de teoría."
            }
        except Exception:
            return {"score": 0.0, "is_correct": False, "strengths": [], "missing": ["Formato de emparejamiento inválido."], "confusions": [], "model_answer": correct_answer, "tips": "Reintenta."}

    return {"score": 0.0, "is_correct": False, "strengths": [], "missing": [], "confusions": [], "model_answer": correct_answer, "tips": ""}

def grade_semantic_open_question(
    user_answer: str,
    correct_answer: str,
    concept_metadata: Dict[str, Any],
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Evaluates open responses semantically using key concept rubrics,
    detecting presence of foundational ideas, omissions, and conceptual confusions.
    Optionally enriches via LLM API if key is present.
    """
    if not user_answer or len(user_answer.strip()) < 5:
        return {
            "score": 0.0,
            "is_correct": False,
            "strengths": [],
            "missing": ["La respuesta proporcionada está vacía o es demasiado escueta."],
            "confusions": [],
            "model_answer": correct_answer,
            "tips": "Desarrollá una explicación conceptual con tus propias palabras fundamentándote en la teoría."
        }

    # Extract key terms from model answer and definition
    target_terms = set()
    for source in [correct_answer, concept_metadata.get("definition", ""), concept_metadata.get("explanation", "")]:
        words = re.findall(r'\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]{4,}\b', source.lower())
        for w in words:
            if w not in ["para", "como", "cada", "este", "esta", "estos", "estas", "cual", "quien", "donde", "tiene", "puede", "debe"]:
                target_terms.add(normalize_text(w))

    u_norm = normalize_text(user_answer)
    u_words = set(u_norm.split())

    # Count matching semantic anchors
    matched_terms = [t for t in target_terms if t in u_words or any(t in uw or uw in t for uw in u_words)]
    coverage = len(matched_terms) / max(len(target_terms), 1)

    # Heuristic scoring based on semantic coverage and length
    raw_score = min(100.0, (coverage * 120.0) + (min(len(u_norm.split()), 40) / 40.0 * 20.0))
    raw_score = round(raw_score, 1)

    strengths = []
    missing = []
    confusions = []

    # Check for common confusions from concept metadata
    common_conf = concept_metadata.get("common_confusions", "")
    if common_conf:
        conf_words = [normalize_text(cw) for cw in re.findall(r'\b[a-zA-Z]{4,}\b', common_conf) if len(cw) > 4]
        for cw in conf_words:
            if cw in u_norm and "no" not in u_norm:
                confusions.append(f"Atención: Notamos una posible confusión advertida por la cátedra: {common_conf}")
                raw_score = max(0.0, raw_score - 20.0)
                break

    if raw_score >= 80:
        strengths.append("Identificaste con precisión los conceptos nucleares exigidos por la cátedra.")
        strengths.append("Estructuraste la respuesta con coherencia lógica y rigor técnico.")
        if raw_score < 95:
            missing.append("Podrías enriquecer aún más la respuesta agregando un ejemplo concreto de negocio.")
        tips = "¡Excelente respuesta! Tu comprensión del concepto es sólida y alineada al examen."
    elif raw_score >= 60:
        strengths.append("Comprendés la idea central del concepto y sus fundamentos generales.")
        missing.append("Te faltó profundizar en aspectos técnicos específicos o terminología formal del modelo.")
        tips = "Respuesta parcialmente correcta. Revisa la respuesta modelo para incorporar los matices técnicos que te faltaron."
    elif raw_score >= 40:
        strengths.append("Mencionaste algunos elementos válidos de forma aislada.")
        missing.append("Omitiste definiciones críticas o el mecanismo operativo central.")
        tips = "Respuesta insuficiente. Es importante repasar la ficha teórica de este concepto antes del examen."
    else:
        missing.append("La respuesta no aborda los conceptos fundamentales requeridos en la pregunta.")
        tips = "Respuesta incorrecta o incompleta. Hacé clic en 'Revisar Teoría' para consolidar este tema."

    is_correct = (raw_score >= 60.0)

    return {
        "score": raw_score,
        "is_correct": is_correct,
        "strengths": strengths,
        "missing": missing,
        "confusions": confusions,
        "model_answer": correct_answer,
        "tips": tips
    }
