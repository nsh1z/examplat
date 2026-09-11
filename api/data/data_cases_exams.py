"""
Data Cases and Exam Questions strictly calibrated to the Official Exam Scope:
- Clase nro 1 Ingeniería de Datos 1.pdf
- Diagramas de Entidad Relación y Modelo de Datos.pdf
- Clase nro 11 - Mássss DER.pdf
- El Modelo Relacional.pdf
- Algebra Relacional.pdf
"""

ALGEBRA_16_QUESTIONS = [
    {
        "id": "q_alg_1",
        "topic_id": "u4_t5",
        "concept_id": "c_operadores_unarios",
        "type": "open_question",
        "difficulty": "facil",
        "question": "[Álgebra Relacional - Consulta 1]\nEsquema: Proveedor(Cod_prov, Nombre, Domicilio, Ciudad)\nRequerimiento: Listar los nombres de los proveedores de la ciudad de La Plata.",
        "options": [],
        "correct_answer": "Π_Nombre(σ_Ciudad = 'La Plata'(Proveedor))",
        "explanation": "Selecciona horizontalmente (σ) los proveedores cuya Ciudad sea 'La Plata' y proyecta verticalmente (Π) el atributo Nombre.",
        "hint1": "Filtro en Ciudad y proyección en Nombre.",
        "hint2": "Π_Nombre(σ_Ciudad='La Plata'(Proveedor))",
        "source_document": "Algebra Relacional.pdf",
        "source_page": "Consulta 1",
        "semantic_hash": "hash_alg_q1"
    },
    {
        "id": "q_alg_2",
        "topic_id": "u4_t5",
        "concept_id": "c_operadores_unarios",
        "type": "open_question",
        "difficulty": "facil",
        "question": "[Álgebra Relacional - Consulta 2]\nEsquema: Articulo(Cod_art, descripcion, Precio)\nRequerimiento: Listar los números de artículos cuyo precio sea inferior a $10.",
        "options": [],
        "correct_answer": "Π_Cod_art(σ_Precio < 10(Articulo))",
        "explanation": "Selecciona los artículos con Precio < 10 y proyecta su código (Cod_art).",
        "hint1": "Filtro: Precio < 10.",
        "hint2": "Π_Cod_art(σ_Precio < 10(Articulo))",
        "source_document": "Algebra Relacional.pdf",
        "source_page": "Consulta 2",
        "semantic_hash": "hash_alg_q2"
    },
    {
        "id": "q_alg_3",
        "topic_id": "u4_t5",
        "concept_id": "c_operadores_unarios",
        "type": "open_question",
        "difficulty": "facil",
        "question": "[Álgebra Relacional - Consulta 3]\nEsquema: Almacen(Nro, Responsable)\nRequerimiento: Listar los responsables de los almacenes.",
        "options": [],
        "correct_answer": "Π_Responsable(Almacen)",
        "explanation": "Proyección directa sobre la columna Responsable (elimina automáticamente duplicados).",
        "hint1": "No hay condición de filtro; es solo una proyección vertical.",
        "hint2": "Π_Responsable(Almacen)",
        "source_document": "Algebra Relacional.pdf",
        "source_page": "Consulta 3",
        "semantic_hash": "hash_alg_q3"
    },
    {
        "id": "q_alg_4",
        "topic_id": "u4_t5",
        "concept_id": "c_operadores_conjuntos",
        "type": "open_question",
        "difficulty": "medio",
        "question": "[Álgebra Relacional - Consulta 4]\nEsquema: Provisto_por(Cod_mat, Cod_prov)\nRequerimiento: Listar los códigos de los materiales que provea el proveedor 10 y no los provea el proveedor 15.",
        "options": [],
        "correct_answer": "Π_Cod_mat(σ_Cod_prov = 10(Provisto_por)) - Π_Cod_mat(σ_Cod_prov = 15(Provisto_por))",
        "explanation": "Aplica la diferencia de conjuntos (-) entre la proyección de materiales provistos por el proveedor 10 y los del proveedor 15 (requiere unión-compatibilidad).",
        "hint1": "Usar el operador diferencia (-) entre dos proyecciones del mismo grado.",
        "hint2": "Π_Cod_mat(σ_Cod_prov=10) - Π_Cod_mat(σ_Cod_prov=15)",
        "source_document": "Algebra Relacional.pdf",
        "source_page": "Consulta 4",
        "semantic_hash": "hash_alg_q4"
    },
    {
        "id": "q_alg_7",
        "topic_id": "u4_t5",
        "concept_id": "c_operadores_conjuntos",
        "type": "open_question",
        "difficulty": "medio",
        "question": "[Álgebra Relacional - Consulta 7]\nEsquema: Tiene(Nro, Cod_art)\nRequerimiento: Listar los almacenes que contienen los artículos 'A' y los artículos 'B' (ambos simultáneamente).",
        "options": [],
        "correct_answer": "Π_Nro(σ_Cod_art = 'A'(Tiene)) ∩ Π_Nro(σ_Cod_art = 'B'(Tiene))",
        "explanation": "Intersección formal (∩) entre los almacenes que tienen el artículo A y los que tienen el B.",
        "hint1": "Debe usarse intersección (∩), no un simple AND.",
        "hint2": "Π_Nro(σ_Cod_art='A'(Tiene)) ∩ Π_Nro(σ_Cod_art='B'(Tiene))",
        "source_document": "Algebra Relacional.pdf",
        "source_page": "Consulta 7",
        "semantic_hash": "hash_alg_q7"
    },
    {
        "id": "q_alg_16",
        "topic_id": "u4_t5",
        "concept_id": "c_juntas_y_division",
        "type": "open_question",
        "difficulty": "experto",
        "question": "[Álgebra Relacional - Consulta 16]\nEsquema: Tiene(Nro, Cod_art), Articulo(Cod_art, descripcion, Precio)\nRequerimiento: Listar los números de almacenes que contienen TODOS los artículos existentes en el catálogo.",
        "options": [],
        "correct_answer": "Tiene ÷ (Π_Cod_art(Articulo))",
        "explanation": "Aplica la División Relacional (÷) de Tiene entre la totalidad de los artículos proyectados del catálogo general para resolver el cuantificador universal.",
        "hint1": "División de la tabla Tiene por todos los artículos.",
        "hint2": "Tiene ÷ (Π_Cod_art(Articulo))",
        "source_document": "Algebra Relacional.pdf",
        "source_page": "Consulta 16",
        "semantic_hash": "hash_alg_q16"
    }
]

EXAM_BANK_EXTRA_QUESTIONS = [
    {
        "id": "q_exam_1",
        "topic_id": "u1_t5",
        "concept_id": "c_independencia_datos",
        "type": "multiple_choice",
        "difficulty": "medio",
        "question": "En el marco de la arquitectura ANSI/SPARC de 3 niveles, ¿cuál de los siguientes cambios constituye un ejemplo estricto de Independencia Física de datos?",
        "options": [
            {"id": "a", "text": "Reorganizar los archivos de datos en disco o agregar un nuevo índice sin alterar el esquema conceptual ni requerir modificaciones en los programas de aplicación."},
            {"id": "b", "text": "Agregar una nueva columna a una tabla lógica del esquema conceptual y recompilar las aplicaciones."},
            {"id": "c", "text": "Cambiar el nombre de una tabla y romper las consultas de los usuarios."},
            {"id": "d", "text": "Crear una nueva vista externa para el departamento de finanzas."}
        ],
        "correct_answer": "a",
        "explanation": "La opción A es correcta. La Independencia Física es la capacidad de modificar el esquema interno (físico/almacenamiento) sin alterar el esquema conceptual ni romper el funcionamiento de las aplicaciones de usuario.",
        "hint1": "Pensá en cambios a nivel de hardware o estructuras internas de almacenamiento.",
        "hint2": "No se modifican las tablas conceptuales ni las vistas.",
        "source_document": "Clase nro 1 Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 23-25",
        "semantic_hash": "hash_exam_q1_indep_fisica"
    },
    {
        "id": "q_exam_2",
        "topic_id": "u3_t4",
        "concept_id": "c_disyuncion_solapamiento",
        "type": "multiple_choice",
        "difficulty": "medio",
        "question": "¿Cuál es la diferencia fundamental entre una restricción de Disyunción (d) y una de Solapamiento (o) en el Modelo Entidad-Relación Extendido (EER)?",
        "options": [
            {"id": "a", "text": "En la disyunción (d) una entidad puede pertenecer como máximo a una subclase; en el solapamiento (o) puede pertenecer a más de una subclase simultáneamente."},
            {"id": "b", "text": "En la disyunción todas las entidades deben pertenecer obligatoriamente a una subclase; en el solapamiento es opcional."},
            {"id": "c", "text": "La disyunción solo aplica a entidades débiles y el solapamiento a entidades fuertes."},
            {"id": "d", "text": "No existe diferencia; son sinónimos según la notación de Chen."}
        ],
        "correct_answer": "a",
        "explanation": "La opción A es correcta. La disyunción ('d') impone exclusión mutua: una instancia de la superclase puede ser miembro de a lo sumo una subclase. El solapamiento ('o') permite pertenencia concurrente a múltiples subclases.",
        "hint1": "d = disjoint (disyunto / exclusivo); o = overlap (solapado / concurrente).",
        "hint2": "Pensá si un empleado puede ser Técnico y a la vez Licenciado.",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Págs. 23-24",
        "semantic_hash": "hash_exam_q2_disyuncion_solapamiento"
    },
    {
        "id": "q_exam_3",
        "topic_id": "u4_t4",
        "concept_id": "c_teoria_claves",
        "type": "multiple_choice",
        "difficulty": "medio",
        "question": "En la teoría relacional de Codd, ¿cuál es la diferencia exacta entre una Superclave y una Clave Candidata?",
        "options": [
            {"id": "a", "text": "Toda superclave identifica de forma única cada tupla; la clave candidata es una superclave mínima (sin atributos superfluos o redundantes)."},
            {"id": "b", "text": "La superclave es la elegida por el DBA y la candidata es la que se descarta."},
            {"id": "c", "text": "La superclave admite valores NULL y la clave candidata no los admite."},
            {"id": "d", "text": "La clave candidata se compone obligatoriamente de claves foráneas y la superclave no."}
        ],
        "correct_answer": "a",
        "explanation": "La opción A es correcta. Una superclave es cualquier conjunto de atributos que garantice la unicidad de las tuplas. Una clave candidata es una superclave minimal: si se le retira cualquier atributo, deja de ser superclave.",
        "hint1": "Principio de minimidad.",
        "hint2": "Si a una clave candidata le agregás cualquier otro atributo, obtenés una superclave.",
        "source_document": "El Modelo Relacional.pdf",
        "source_page": "Pág. 16",
        "semantic_hash": "hash_exam_q3_superclave_candidata"
    },
    {
        "id": "q_exam_4",
        "topic_id": "u6_t6",
        "concept_id": "c_mapeo_jerarquias_opciones",
        "type": "multiple_choice",
        "difficulty": "dificil",
        "question": "En el mapeo de jerarquías EER al modelo relacional, ¿cuál es la precondición OBLIGATORIA para poder aplicar la Opción B (tablas exclusivas para las subclases, eliminando la superclase)?",
        "options": [
            {"id": "a", "text": "Que la especialización sea estrictamente de Participación Total y Disyunción (t, d)."},
            {"id": "b", "text": "Que la especialización sea Parcial y con Solapamiento (p, o)."},
            {"id": "c", "text": "Que la superclase tenga más de 10 atributos específicos."},
            {"id": "d", "text": "Que todas las subclases posean relaciones recursivas."}
        ],
        "correct_answer": "a",
        "explanation": "La opción A es correcta. La Opción B descarta la tabla de la superclase. Si la especialización fuese parcial, se perderían las entidades que no pertenecen a ninguna subclase. Si hubiese solapamiento, se duplicarían los atributos comunes de la entidad en múltiples tablas. Por tanto, exige que sea Total y Disyunta.",
        "hint1": "Total (no hay entidades sueltas) y Disyunta (no hay duplicación entre subclases).",
        "hint2": "(t, d) es la única combinación matemáticamente segura para eliminar la superclase.",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Págs. 54-56",
        "semantic_hash": "hash_exam_q4_mapeo_opcion_b"
    },
    {
        "id": "q_exam_5",
        "topic_id": "u4_t5",
        "concept_id": "c_semantica_null",
        "type": "true_false",
        "difficulty": "facil",
        "question": "En el modelo relacional, el valor NULO (NULL) representa exactamente lo mismo que una cadena de texto vacía ('') o el número cero (0).",
        "options": [
            {"id": "v", "text": "VERDADERO"},
            {"id": "f", "text": "FALSO"}
        ],
        "correct_answer": "f",
        "explanation": "FALSO. Para Codd, el valor NULL indica ausencia de valor o valor desconocido. Una cadena vacía ('') es un dato de texto conocido de longitud cero, y el cero (0) es un valor numérico definido. Confundirlos transgrede la lógica trivaluada del modelo relacional.",
        "hint1": "NULL significa desconocido o no aplicable, no cero.",
        "hint2": "NULL no ocupa un valor en el dominio.",
        "source_document": "El Modelo Relacional.pdf",
        "source_page": "Pág. 20",
        "semantic_hash": "hash_exam_q5_null_no_es_cero"
    },
    {
        "id": "q_exam_6",
        "topic_id": "u2_t4",
        "concept_id": "c_reglas_construccion_der",
        "type": "true_false",
        "difficulty": "facil",
        "question": "En las reglas de construcción formal de un Diagrama Entidad-Relación (DER), es válido conectar una relación directamente a otra relación con una línea.",
        "options": [
            {"id": "v", "text": "VERDADERO"},
            {"id": "f", "text": "FALSO"}
        ],
        "correct_answer": "f",
        "explanation": "FALSO. Una de las reglas inviolables del DER establece que una relación no puede estar conectada directamente a otra relación. Las conexiones siempre deben alternar entre una entidad y una relación.",
        "hint1": "Entidad-Relación-Entidad.",
        "hint2": "Dos rombos nunca pueden estar unidos por una línea.",
        "source_document": "Diagramas de Entidad Relación y Modelo de Datos.pdf",
        "source_page": "Pág. 17",
        "semantic_hash": "hash_exam_q6_conexion_relaciones"
    }
]
