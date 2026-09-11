from fastapi import APIRouter
import re
from typing import Dict, Any, List
from database import get_db
from services.tutor_service import search_knowledge_base

router = APIRouter(prefix="/api/search", tags=["search"])

COMPARISON_PRESETS = {
    ("drop", "truncate"): {
        "title": "DROP TABLE vs TRUNCATE TABLE",
        "rows": [
            {"criterion": "Categoría de Sentencia", "a_val": "DDL (Data Definition Language)", "b_val": "DDL (Data Definition Language)"},
            {"criterion": "Estructura de la Tabla", "a_val": "Elimina los datos Y la definición completa del esquema", "b_val": "Conserva la estructura, columnas y restricciones"},
            {"criterion": "Registro en Log de Transacciones", "a_val": "Mínimo (desasigna páginas de esquema)", "b_val": "Mínimo (desasigna extensiones completas de páginas)"},
            {"criterion": "Disparadores (Triggers)", "a_val": "No ejecuta disparadores de borrado", "b_val": "No activa triggers FOR DELETE"},
            {"criterion": "Reinicio de Identidad / Autoincrement", "a_val": "No aplica (la tabla desaparece)", "b_val": "Reinicia el contador al valor semilla inicial (SEED)"},
            {"criterion": "Restricción de Clave Foránea", "a_val": "Falla si otra tabla la referencia", "b_val": "Falla si está referenciada por FK, incluso si está vacía"}
        ],
        "summary": "Usar TRUNCATE para vaciar rápidamente una tabla preservando su estructura e índices; usar DROP para eliminar la tabla definitivamente de la base de datos."
    },
    ("where", "having"): {
        "title": "Cláusula WHERE vs Cláusula HAVING",
        "rows": [
            {"criterion": "Momento de Ejecución", "a_val": "Filtra filas individuales ANTES de la agrupación", "b_val": "Filtra grupos de filas DESPUÉS del GROUP BY"},
            {"criterion": "Funciones de Agregación", "a_val": "NO admite COUNT, SUM, AVG, MAX, MIN", "b_val": "Diseñada específicamente para evaluar funciones agregadas"},
            {"criterion": "Requerimiento de GROUP BY", "a_val": "Puede utilizarse sin GROUP BY", "b_val": "Usualmente requiere GROUP BY (aplica a nivel grupo)"},
            {"criterion": "Impacto en Rendimiento", "a_val": "Mayor eficiencia: reduce filas antes del cálculo", "b_val": "Aplica sobre el conjunto ya agrupado en memoria"}
        ],
        "summary": "Regla de oro de examen: WHERE filtra registros individuales; HAVING filtra resultados agregados de grupos."
    },
    ("inner join", "left join"): {
        "title": "INNER JOIN vs LEFT OUTER JOIN",
        "rows": [
            {"criterion": "Comportamiento ante No Coincidencias", "a_val": "Descarta filas sin coincidencia en ambas tablas", "b_val": "Conserva TODAS las filas de la tabla izquierda"},
            {"criterion": "Relleno con Valores Nulos (NULL)", "a_val": "No genera NULLs adicionales por discrepancia", "b_val": "Rellena con NULL los atributos de la derecha si no hay match"},
            {"criterion": "Cardinalidad Resultante", "a_val": "Cardinalidad <= min(N_izq, N_der)", "b_val": "Cardinalidad >= N_izq"},
            {"criterion": "Uso Típico de Examen", "a_val": "Relaciones estrictas donde existen datos vinculados", "b_val": "Encontrar registros huérfanos ('WHERE der.id IS NULL')"}
        ],
        "summary": "Usar LEFT JOIN cuando necesitás listar entidades principales que podrían no tener registros secundarios asociados (ej. clientes sin ventas)."
    }
}

@router.get("")
def search(q: str = ""):
    if not q or len(q.strip()) < 2:
        return {"query": q, "is_comparison": False, "results": [], "concepts": []}

    q_clean = q.strip()
    with get_db() as conn:
        cursor = conn.cursor()

        # Check for comparison intent:
        # e.g., "DROP vs TRUNCATE", "diferencia entre WHERE y HAVING", "DROP frente a TRUNCATE"
        comp_match = re.search(r'^(?:diferencia\s+entre\s+)?(.*?)\s+(?:vs\.?|frente\s+a|\by\b|\be\b)\s+(.*)$', q_clean, re.IGNORECASE)
        if comp_match:
            term_a = comp_match.group(1).strip().lower()
            term_b = comp_match.group(2).strip().lower()

            res_a = search_knowledge_base(conn, term_a)
            res_b = search_knowledge_base(conn, term_b)

            concept_a = res_a[0] if res_a else {"name": term_a.upper(), "definition": "Concepto extraído del curso"}
            concept_b = res_b[0] if res_b else {"name": term_b.upper(), "definition": "Concepto extraído del curso"}

            # Check for preset detailed comparison matrix
            preset_key = None
            for (k1, k2), data in COMPARISON_PRESETS.items():
                if (k1 in term_a and k2 in term_b) or (k2 in term_a and k1 in term_b):
                    preset_key = (k1, k2)
                    break

            if preset_key:
                comp_data = COMPARISON_PRESETS[preset_key]
                comparison_payload = {
                    "title": comp_data["title"],
                    "concept_a": concept_a,
                    "concept_b": concept_b,
                    "rows": comp_data["rows"],
                    "summary": comp_data["summary"]
                }
            else:
                comparison_payload = {
                    "title": f"Comparación: {concept_a['name']} vs {concept_b['name']}",
                    "concept_a": concept_a,
                    "concept_b": concept_b,
                    "rows": [
                        {"criterion": "Definición Conceptual", "a_val": concept_a.get("definition", "")[:120] + "...", "b_val": concept_b.get("definition", "")[:120] + "..."},
                        {"criterion": "Explicación Didáctica", "a_val": concept_a.get("simple_explanation", "")[:120] + "...", "b_val": concept_b.get("simple_explanation", "")[:120] + "..."},
                        {"criterion": "Fuente en Programa", "a_val": f"{concept_a.get('source_document', 'Doc')} (pág. {concept_a.get('source_page', '1')})", "b_val": f"{concept_b.get('source_document', 'Doc')} (pág. {concept_b.get('source_page', '1')})"}
                    ],
                    "summary": f"Distinción clave entre {concept_a['name']} y {concept_b['name']} evaluada en los exámenes de la cátedra."
                }

            all_concepts = []
            seen_ids = set()
            for c in res_a + res_b:
                if c["id"] not in seen_ids:
                    seen_ids.add(c["id"])
                    all_concepts.append(c)

            return {
                "query": q_clean,
                "is_comparison": True,
                "comparison_data": comparison_payload,
                "comparison": comparison_payload,
                "concepts": all_concepts,
                "results": all_concepts
            }

        # Regular ranked search
        results = search_knowledge_base(conn, q_clean)
        return {
            "query": q_clean,
            "is_comparison": False,
            "concepts": results,
            "results": results
        }
