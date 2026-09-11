"""
Unit 5 Data: Álgebra Relacional Formal y las 16 Consultas de Cátedra
Source: Algebra Relacional.pdf (16 consultas formales)
"""

TOPICS = [
    {
        "id": "u5_t1",
        "unit_number": 5,
        "name": "Naturaleza Procedimental y Propiedad de Clausura",
        "description": "El álgebra relacional como lenguaje formal matemático paso a paso y su propiedad de cierre algebraico.",
        "icon": "Calculator",
        "order_idx": 28
    },
    {
        "id": "u5_t2",
        "unit_number": 5,
        "name": "Operadores Unarios: Selección (σ), Proyección (Π) y Renombramiento (ρ)",
        "description": "Filtros horizontales basados en predicados lógicos, filtros verticales de columnas y renombramiento.",
        "icon": "Sliders",
        "order_idx": 29
    },
    {
        "id": "u5_t3",
        "unit_number": 5,
        "name": "Operadores de Conjuntos y Unión-Compatibilidad",
        "description": "Unión (∪), Diferencia (-), Intersección (∩) y Producto Cartesiano (×). Requisitos estrictos de grado y tipo de dominios.",
        "icon": "Grid",
        "order_idx": 30
    },
    {
        "id": "u5_t4",
        "unit_number": 5,
        "name": "Operadores Relacionales Complejos: Juntas (⋈) y División (÷)",
        "description": "Junta Theta, Junta Natural, Equijoint y la División Relacional para resolver el cuantificador universal ('para todo').",
        "icon": "GitMerge",
        "order_idx": 31
    },
    {
        "id": "u5_t5",
        "unit_number": 5,
        "name": "Las 16 Consultas Formales del Esquema de Cátedra",
        "description": "Resolución matemática de la guía oficial sobre Almacén, Artículo, Material, Proveedor, Tiene, Compuesto_por y Provisto_por.",
        "icon": "ListChecks",
        "order_idx": 32
    }
]

CONCEPTS = [
    {
        "id": "c_clausura_algebraica",
        "topic_id": "u5_t1",
        "name": "Propiedad de Clausura o Cierre Algebraico",
        "definition": "Propiedad formal que establece que todo operador del álgebra relacional toma como argumentos una o dos relaciones válidas y produce invariablemente como resultado una nueva relación válida. Esto permite anidar y componer expresiones algebraicas complejas de forma recursiva sin salir del modelo.",
        "explanation": "Al igual que en el álgebra numérica la suma de dos reales produce un real, en el álgebra relacional toda operación devuelve una relación.",
        "simple_explanation": "El resultado de cualquier filtro o combinación de tablas siempre es otra tabla, lista para seguir aplicándole más operaciones.",
        "example": "La proyección sobre el resultado de una selección previa: Π_Nombre(σ_Ciudad = 'La Plata'(Proveedor)).",
        "related_concepts": ["c_operadores_unarios", "c_juntas_y_division"],
        "common_confusions": "Creer que la proyección devuelve una lista o vector primitivo; devuelve una relación formal (sin duplicados).",
        "difficulty": "facil",
        "source_document": "Algebra Relacional.pdf",
        "source_page": "Teoría Álgebra",
        "order_idx": 1
    },
    {
        "id": "c_operadores_unarios",
        "topic_id": "u5_t2",
        "name": "Operadores Unarios: Selección (σ) y Proyección (Π)",
        "definition": "Operadores que actúan sobre una única relación: 1) Selección (σ_condicion(R)): produce un subconjunto horizontal de tuplas que satisfacen un predicado booleano dado (preserva el grado n de la relación original y su cardinalidad resultante es menor o igual a m); 2) Proyección (Π_lista_atributos(R)): produce un subconjunto vertical seleccionando solo las columnas indicadas y eliminando automáticamente tuplas duplicadas resultantes; 3) Renombramiento (ρ_S(R)): cambia el nombre de la relación o de sus atributos.",
        "explanation": "La selección filtra filas (WHERE en SQL); la proyección filtra columnas (SELECT en SQL).",
        "simple_explanation": "Selección (σ) corta filas horizontalmente; Proyección (Π) corta columnas verticalmente.",
        "example": "Listar nombres de proveedores de La Plata: Π_Nombre(σ_Ciudad = 'La Plata'(Proveedor)).",
        "related_concepts": ["c_clausura_algebraica", "c_operadores_conjuntos"],
        "common_confusions": "Olvidar que la proyección relacional matemática elimina automáticamente tuplas duplicadas (a diferencia del SELECT básico de SQL que requiere DISTINCT).",
        "difficulty": "medio",
        "source_document": "Algebra Relacional.pdf",
        "source_page": "Consultas 1 a 3",
        "order_idx": 2
    },
    {
        "id": "c_operadores_conjuntos",
        "topic_id": "u5_t3",
        "name": "Operadores de Conjuntos y Unión-Compatibilidad",
        "definition": "Operaciones binarias derivadas de la teoría de conjuntos: Unión (R ∪ S), Diferencia (R - S) e Intersección (R ∩ S). Exigen estrictamente que las relaciones R y S sean 'Unión-Compatibles': deben tener exactamente el mismo grado (mismo número de atributos) y los dominios de los atributos correspondientes ordenados deben ser idénticos o compatibles.",
        "explanation": "El Producto Cartesiano (R × S) no exige unión-compatibilidad: concatena cada tupla de R con cada tupla de S, con grado resultante n_R + n_S y cardinalidad m_R * m_S.",
        "simple_explanation": "Para unir o restar tablas, tienen que tener la misma cantidad de columnas y el mismo tipo de datos.",
        "example": "Materiales provistos por prov 10 y no por 15: Π_Cod_mat(σ_Cod_prov=10(Provisto_por)) - Π_Cod_mat(σ_Cod_prov=15(Provisto_por)).",
        "related_concepts": ["c_operadores_unarios", "c_juntas_y_division"],
        "common_confusions": "Intentar hacer la unión de una tabla de 2 columnas con una de 3 columnas (provoca un error de incompatibilidad de grado).",
        "difficulty": "medio",
        "source_document": "Algebra Relacional.pdf",
        "source_page": "Consultas 4 y 7",
        "order_idx": 3
    },
    {
        "id": "c_juntas_y_division",
        "topic_id": "u5_t4",
        "name": "Operadores Relacionales Complejos: Juntas (⋈) y División (÷)",
        "definition": "Operadores avanzados: 1) Junta Theta (R ⋈_θ S): equivale a un Producto Cartesiano seguido de una Selección por la condición θ (σ_θ(R × S)); 2) Junta Natural (R ⋈ S): junta por igualdad implícita sobre todos los atributos que compartan el mismo nombre, proyectando una sola copia de dichos atributos; 3) División Relacional (R ÷ S): operador para relaciones donde R tiene atributos (X, Y) y S tiene atributos (Y); devuelve todas las tuplas de X en R que están asociadas con TODAS y cada una de las tuplas de S (resuelve el cuantificador universal 'para todo').",
        "explanation": "La división relacional es el operador clave para responder preguntas de examen del tipo 'almacenes que contienen todos los artículos'.",
        "simple_explanation": "La Junta Natural une tablas por las columnas con igual nombre. La División (÷) busca los registros que cumplen 'con todos' los elementos de otra lista.",
        "example": "Almacenes con todos los artículos: Tiene ÷ (Π_Cod_art(Articulo)).",
        "related_concepts": ["c_operadores_conjuntos", "c_16_consultas_algebra"],
        "common_confusions": "Creer que la división relacional es un operador primitivo; es un operador derivado definido a partir de producto cartesiano, diferencia y proyección.",
        "difficulty": "experto",
        "source_document": "Algebra Relacional.pdf",
        "source_page": "Consulta 16",
        "order_idx": 4
    },
    {
        "id": "c_16_consultas_algebra",
        "topic_id": "u5_t5",
        "name": "Resolución de las 16 Consultas Formales de Cátedra",
        "definition": "Solución exhaustiva de los 16 requerimientos oficiales de la cátedra sobre el esquema Almacén-Artículo-Material-Proveedor: 1 a 3 unarias; 4 diferencia; 5 selección; 6 selección compuesta con AND; 7 intersección; 8 unión con OR; 9 a 14 juntas múltiples encadenadas; 15 máximo precio mediante diferencia del producto cartesiano autorreferencial; 16 división relacional.",
        "explanation": "Constituye la referencia matemática completa para resolver los ejercicios prácticos del parcial.",
        "simple_explanation": "Las 16 consultas son las preguntas oficiales de examen que combinan filtros, cruces de tablas y división.",
        "example": "Consulta 15 (artículos de mayor precio): Π_Cod_art(Articulo) - Π_A1.Cod_art(Articulo A1 ⋈_(A1.Precio < A2.Precio) Articulo A2).",
        "related_concepts": ["c_juntas_y_division", "c_operadores_unarios"],
        "common_confusions": "En la consulta 15 (máximo), no existe función MAX en álgebra relacional pura; debe resolverse restándole al universo de artículos aquellos para los cuales existe otro artículo con precio mayor.",
        "difficulty": "experto",
        "source_document": "Algebra Relacional.pdf",
        "source_page": "Págs. 1-16",
        "order_idx": 5
    }
]

QUESTIONS = [
    {
        "id": "q_u5_1",
        "topic_id": "u5_t1",
        "concept_id": "c_clausura_algebraica",
        "type": "multiple_choice",
        "difficulty": "facil",
        "question": "¿Qué establece la Propiedad de Clausura o Cierre en el Álgebra Relacional?",
        "options": [
            {"id": "a", "text": "Que el resultado de aplicar cualquier operador algebraico sobre una o más relaciones es siempre una nueva relación válida."},
            {"id": "b", "text": "Que las relaciones no pueden cerrarse mientras haya usuarios conectados."},
            {"id": "c", "text": "Que toda clave primaria debe cerrarse con una clave foránea obligatoria."},
            {"id": "d", "text": "Que las consultas deben finalizar con punto y coma."}
        ],
        "correct_answer": "a",
        "explanation": "La propiedad de clausura garantiza que el resultado de cualquier expresión algebraica es una relación formal, lo que permite anidar operaciones sucesivamente.",
        "hint1": "Relación entra, relación sale.",
        "hint2": "Permite componer operaciones.",
        "source_document": "Algebra Relacional.pdf",
        "source_page": "Teoría Álgebra",
        "semantic_hash": "hash_u5_q1"
    },
    {
        "id": "q_u5_2",
        "topic_id": "u5_t3",
        "concept_id": "c_operadores_conjuntos",
        "type": "true_false",
        "difficulty": "medio",
        "question": "Para poder aplicar los operadores de Unión (∪), Intersección (∩) o Diferencia (-), las relaciones involucradas deben tener obligatoriamente el mismo grado y dominios compatibles (Unión-Compatibles).",
        "options": [
            {"id": "v", "text": "VERDADERO"},
            {"id": "f", "text": "FALSO"}
        ],
        "correct_answer": "v",
        "explanation": "VERDADERO. La unión-compatibilidad es el requisito matemático estricto para operar con unión, intersección o diferencia entre dos relaciones en el álgebra relacional.",
        "hint1": "Mismo número de columnas y tipos compatibles.",
        "hint2": "No se pueden unir peras con manzanas.",
        "source_document": "Algebra Relacional.pdf",
        "source_page": "Consultas 4 y 7",
        "semantic_hash": "hash_u5_q2"
    },
    {
        "id": "q_u5_3",
        "topic_id": "u5_t4",
        "concept_id": "c_juntas_y_division",
        "type": "multiple_choice",
        "difficulty": "dificil",
        "question": "Para responder a la consulta 'Listar los almacenes que contienen TODOS los artículos existentes en el catálogo', ¿cuál es el operador del álgebra relacional que se debe emplear?",
        "options": [
            {"id": "a", "text": "División Relacional (÷)"},
            {"id": "b", "text": "Producto Cartesiano (×)"},
            {"id": "c", "text": "Unión Externa Completa (FULL OUTER JOIN)"},
            {"id": "d", "text": "Diferencia Simétrica (Δ)"}
        ],
        "correct_answer": "a",
        "explanation": "La división relacional (÷) está expresamente diseñada para resolver el cuantificador universal 'para todo' (Consulta 16: Tiene ÷ Π_Cod_art(Articulo)).",
        "hint1": "Cuantificador universal 'todos'.",
        "hint2": "Consulta 16 de la guía oficial.",
        "source_document": "Algebra Relacional.pdf",
        "source_page": "Consulta 16",
        "semantic_hash": "hash_u5_q3"
    }
]
