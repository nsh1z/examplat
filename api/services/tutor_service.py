import sqlite3
import re
from typing import Dict, Any, List

def explain_differently(concept: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates an alternative didactic pedagogical explanation
    with analogies, real business cases, and pitfall warnings.
    """
    name = concept.get("name", "")
    simple_exp = concept.get("simple_explanation", "")
    example = concept.get("example", "")
    common_confusions = concept.get("common_confusions", "")
    definition = concept.get("definition", "")

    analogy = f"Pensá en '{name}' como una regla de seguridad en la vida real: si no se cumple estrictamente, el sistema entero colapsa o produce inconsistencias."
    if "acid" in name.lower() or "transacción" in name.lower():
        analogy = "Imaginate una máquina expendedora de café: si ponés la moneda pero se corta la luz antes de tirar el café, la máquina te devuelve la moneda o te da el café al volver; nunca se queda con tu dinero sin darte nada (eso es Atomicidad)."
    elif "clave" in name.lower() or "primary" in name.lower():
        analogy = "Es exactamente como tu número de DNI o pasaporte: no pueden existir dos personas en el país con el mismo número, y nadie puede nacer sin un número asignado."
    elif "foreign" in name.lower() or "foránea" in name.lower():
        analogy = "Es como la pulsera de un hotel All-Inclusive: para que te sirvan una bebida, tenés que mostrar la pulsera que demuestra que estás registrado como huésped en la lista principal."
    elif "where" in name.lower() or "having" in name.lower():
        analogy = "WHERE es el patovica en la puerta del boliche que filtra persona por persona antes de entrar; HAVING es el jurado de la fiesta que premia a los grupos que tienen más de 10 personas."

    return {
        "concept_name": name,
        "super_simple_summary": simple_exp or definition,
        "real_world_analogy": analogy,
        "practical_case": example or "Ejemplo de aplicación directa en sistemas transaccionales bancarios y comerciales.",
        "pitfall_warning": common_confusions or "No confundir el concepto teórico formal con los detalles de implementación de un motor específico.",
        "source": f"{concept.get('source_document', '')} — {concept.get('source_page', '')}"
    }

def search_knowledge_base(conn: sqlite3.Connection, query: str) -> List[Dict[str, Any]]:
    """
    Fast keyword and semantic search across all topics and concepts.
    Returns ranked matches with exact PDF citations.
    """
    cursor = conn.cursor()
    terms = [t.strip().lower() for t in query.split() if len(t.strip()) > 2]
    if not terms:
        return []

    like_clauses = []
    params = []
    for t in terms:
        like_clauses.append("(LOWER(c.name) LIKE ? OR LOWER(c.definition) LIKE ? OR LOWER(c.explanation) LIKE ? OR LOWER(t.name) LIKE ?)")
        wildcard = f"%{t}%"
        params.extend([wildcard, wildcard, wildcard, wildcard])

    sql = f"""
    SELECT c.*, t.name as topic_name, t.unit_number
    FROM concepts c
    JOIN topics t ON c.topic_id = t.id
    WHERE {' OR '.join(like_clauses)}
    ORDER BY 
        CASE WHEN LOWER(c.name) LIKE ? THEN 1
             WHEN LOWER(c.name) LIKE ? THEN 2
             ELSE 3 END ASC
    LIMIT 15;
    """
    rank_params = [f"%{query.lower()}%", f"%{terms[0]}%"]
    cursor.execute(sql, params + rank_params)
    rows = cursor.fetchall()

    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "unit_number": r["unit_number"],
            "topic_name": r["topic_name"],
            "name": r["name"],
            "definition": r["definition"],
            "simple_explanation": r["simple_explanation"],
            "example": r["example"],
            "source_document": r["source_document"],
            "source_page": r["source_page"]
        })
    return results
