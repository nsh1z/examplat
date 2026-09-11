"""
Unit 6 Data: Metodología Sistemática de Mapeo DER/EER a Esquema Relacional
Source: Clase nro 11 - Mássss DER.pdf (Slides 30 a 58)
"""

TOPICS = [
    {
        "id": "u6_t1",
        "unit_number": 6,
        "name": "Mapeo de Entidades Fuertes (Paso 1) y Entidades Débiles (Paso 2)",
        "description": "Conversión de entidades regulares a tablas y reglas de clave compuesta con FK del propietario para débiles.",
        "icon": "Box",
        "order_idx": 33
    },
    {
        "id": "u6_t2",
        "unit_number": 6,
        "name": "Mapeo de Relaciones Binarias 1:N (Paso 3) y 1:1 (Paso 4)",
        "description": "FK en el lado N. Las 3 metodologías oficiales para relaciones 1:1: foreign key, relación mezclada y referencia cruzada.",
        "icon": "GitCommit",
        "order_idx": 34
    },
    {
        "id": "u6_t3",
        "unit_number": 6,
        "name": "Mapeo de Relaciones M:N (Paso 5) y Relaciones Ternarias (Paso 7)",
        "description": "Creación obligatoria de tablas intermedias asociativas con claves primarias compuestas y atributos de relación.",
        "icon": "Network",
        "order_idx": 35
    },
    {
        "id": "u6_t4",
        "unit_number": 6,
        "name": "Mapeo de Atributos Multivaluados (Paso 6) y Compuestos",
        "description": "Las 3 opciones para atributos multivalor (delimitador en 1 tabla, columnas fijas, tabla independiente) y aplanado de compuestos.",
        "icon": "ListPlus",
        "order_idx": 36
    },
    {
        "id": "u6_t5",
        "unit_number": 6,
        "name": "Mapeo de Relaciones Recursivas o Reflexivas (Paso 8)",
        "description": "Tratamiento de relaciones consigo misma según cardinalidad: 1:1 (rol irrelevante), 1:N (FK en rol de 1), N:N (dos FKs en tabla intermedia).",
        "icon": "RefreshCw",
        "order_idx": 37
    },
    {
        "id": "u6_t6",
        "unit_number": 6,
        "name": "Mapeo de Especialización/Generalización EER (Las 4 Opciones)",
        "description": "Opción 1 (Superclase y subclases), Opción 2 (Solo subclases), Opción 3 (Tabla única con discriminante), Opción 4 (Tabla única con booleanos).",
        "icon": "Layers",
        "order_idx": 38
    }
]

CONCEPTS = [
    {
        "id": "c_mapeo_entidades_fuertes_debiles",
        "topic_id": "u6_t1",
        "name": "Mapeo de Entidades Fuertes (Paso 1) y Débiles (Paso 2)",
        "definition": "1) Paso 1 (Entidades Fuertes): Por cada entidad regular E del DER, crear una relación R con todos los atributos simples de E y elegir una clave principal; 2) Paso 2 (Entidades Débiles): Por cada entidad débil W con propietario E, crear una relación R con los atributos simples de W más la clave principal de E como clave foránea (FK). La clave principal de R es la combinación de la FK del propietario más la clave parcial (discriminante) de W.",
        "explanation": "La entidad débil no tiene existencia independiente y su clave primaria está forzosamente ligada a la clave de su entidad padre.",
        "simple_explanation": "Para la entidad fuerte hacés una tabla normal. Para la débil, le copiás la clave del dueño y la unís a su número para formar la clave primaria.",
        "example": "Pelicula(id_pelicula, titulo, genero, anio) y Copia_Pelicula(id_pelicula, num_copia), donde la PK de Copia_Pelicula es (id_pelicula, num_copia).",
        "related_concepts": ["c_mapeo_relaciones_1n_11", "c_mapeo_relaciones_mn_ternarias"],
        "common_confusions": "Creer que la entidad débil solo tiene como clave su número de copia (dos películas distintas pueden tener una copia con num_copia = 1; se requiere el id_pelicula).",
        "difficulty": "medio",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Págs. 31-33",
        "order_idx": 1
    },
    {
        "id": "c_mapeo_relaciones_1n_11",
        "topic_id": "u6_t2",
        "name": "Mapeo de Relaciones 1:N (Paso 3) y 1:1 (Paso 4)",
        "definition": "1) Paso 3 (1:N Binaria): Se identifica la relación S del lado N y se incluye como clave foránea (FK) la clave primaria de la relación T del lado 1, junto con los atributos de la relación. Se hace así porque cada instancia del lado N se relaciona a lo sumo con una del lado 1; 2) Paso 4 (1:1 Binaria): Tres metodologías posibles: a) Metodología de la foreign key: colocar la FK en cualquiera de las dos tablas (lo mejor es elegir la que tenga participación total); b) Metodología de la relación mezclada: fusionar ambas entidades y la relación en una única tabla cuando ambas participaciones son totales; c) Metodología de referencia cruzada: crear una tabla intermedia con las claves de ambas entidades.",
        "explanation": "En 1:N no se crea tabla intermedia salvo que la relación posea atributos que requieran independizarse.",
        "simple_explanation": "En 1:N, la clave del lado '1' viaja a la tabla del lado 'N'. En 1:1, ponés la clave foránea del lado que sea obligatorio (participación total).",
        "example": "1:N: Empleado(legajo, nombre, DNI, nombre_depto) y Departamento(nombre_depto, descripcion). 1:1: Empleado(legajo...) y Departamento(nombre_depto, funcion, legajo_director).",
        "related_concepts": ["c_mapeo_entidades_fuertes_debiles", "c_mapeo_relaciones_mn_ternarias"],
        "common_confusions": "Colocar la clave foránea en el lado 1 en una relación 1:N (provocaría que el departamento tuviese que almacenar múltiples legajos en una sola fila, violando 1NF).",
        "difficulty": "medio",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Págs. 34-40",
        "order_idx": 2
    },
    {
        "id": "c_mapeo_relaciones_mn_ternarias",
        "topic_id": "u6_t3",
        "name": "Mapeo de Relaciones M:N (Paso 5) y Ternarias (Paso 7)",
        "definition": "1) Paso 5 (M:N Binaria): Se crea obligatoriamente una nueva relación S para representar la relación. Se incluyen como atributos de foreign key las claves principales de las entidades participantes; su combinación forma la clave principal (PK compuesta) de S. Se incluyen también los atributos de la relación; 2) Paso 7 (Ternarias o grado > 2): Se crea una nueva relación S cuya clave principal es la combinación de las foreign keys que hacen referencia a todas las relaciones participantes, más los atributos propios de la relación.",
        "explanation": "No es posible representar una relación M:N o ternaria agregando columnas en las tablas existentes sin generar redundancia o valores nulos.",
        "simple_explanation": "Cada vez que veas una relación N:M o de 3 entidades, nace una tabla intermedia nueva con las claves de todas las tablas unidas.",
        "example": "M:N: Empleado(legajo...), Proyecto(cod_proyecto...) y Colabora(legajo, cod_proyecto, horas). Ternaria: Suministra(cuil_proveedor, id_producto, cod_proyecto, cantidad).",
        "related_concepts": ["c_mapeo_relaciones_1n_11", "c_mapeo_recursivas"],
        "common_confusions": "Olvidar incluir los atributos de la relación (como 'horas' o 'cantidad') dentro de la nueva tabla intermedia.",
        "difficulty": "medio",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Págs. 41-42, 49-50",
        "order_idx": 3
    },
    {
        "id": "c_mapeo_multivaluados_compuestos",
        "topic_id": "u6_t4",
        "name": "Mapeo de Atributos Multivaluados (Paso 6) y Compuestos",
        "definition": "1) Paso 6 (Atributos Multivalor): Tres opciones de diseño según la cátedra: Opción 1: Un solo campo con valores divididos por un carácter como ';' (NOTA: no cumple la Primera Forma Normal 1NF); Opción 2: Columnas finitas en la misma tabla (email_1, email_2), limita a cantidad fija pero da velocidad; Opción 3 (Regla general relacional): Crear una nueva relación R con el atributo multivalor más la clave K de la entidad (como FK), formando una PK compuesta (K, atributo); 2) Atributos Compuestos: Se aplanan en columnas simples independientes (ej. direccion_fisica se desglosa en calle, numero, depto, ciudad, provincia, codigo_postal).",
        "explanation": "La Opción 3 es la única que cumple estrictamente la teoría de normalización de Codd.",
        "simple_explanation": "Si un empleado tiene varios emails: la opción formal es crear una tabla 'Email' con (legajo, direccion_email).",
        "example": "Empleado(legajo, nombre, DNI, fec_nac) y Email(legajo, direccion_email), con PK compuesta (legajo, direccion_email).",
        "related_concepts": ["c_mapeo_entidades_fuertes_debiles", "c_mapeo_recursivas"],
        "common_confusions": "Elegir la Opción 1 en un examen teórico creyendo que es una solución normalizada (viola la atomicidad de la 1NF).",
        "difficulty": "medio",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Págs. 43-48",
        "order_idx": 4
    },
    {
        "id": "c_mapeo_recursivas",
        "topic_id": "u6_t5",
        "name": "Mapeo de Relaciones Recursivas o Reflexivas (Paso 8)",
        "definition": "Reglas para relaciones donde una entidad se relaciona consigo misma: 1) Recursiva 1:1: Se agrega una clave foránea en la misma entidad que referencia a la clave principal de la misma tabla (el rol no es relevante; ej. Persona con cuil_conyuge); 2) Recursiva 1:N: Se agrega una clave foránea en la misma entidad en el rol que tiene cardinalidad 1 (ej. Empleado con legajo_jefe); 3) Recursiva N:N: Se crea obligatoriamente una nueva tabla con el nombre de la relación que contiene la clave de la entidad dos veces (una por cada rol) como claves foráneas compuestas, más atributos de la relación (ej. Amigo con DNI_Persona1, DNI_Persona2, anios).",
        "explanation": "En las recursivas 1:1 y 1:N no se crea tabla intermedia; en la recursiva N:N siempre se crea una tabla con dos roles cruzados.",
        "simple_explanation": "Jefe-subordinado (1:N) es una columna más en Empleado ('legajo_jefe'). Amistad (N:N) requiere una tabla intermedia con dos personas ('DNI_Persona1', 'DNI_Persona2').",
        "example": "Empleado(legajo, DNI, nombre, legajo_jefe). Tabla intermedia Amigo(DNI_Persona1, DNI_Persona2, anios).",
        "related_concepts": ["c_mapeo_relaciones_1n_11", "c_mapeo_relaciones_mn_ternarias"],
        "common_confusions": "Crear una tabla intermedia para una relación recursiva 1:N (innecesario; duplica registros salvo que tenga atributos temporales de vigencia).",
        "difficulty": "dificil",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Págs. 51-53",
        "order_idx": 5
    },
    {
        "id": "c_mapeo_jerarquias_opciones",
        "topic_id": "u6_t6",
        "name": "Mapeo de Especialización EER: Las 4 Opciones Oficiales",
        "definition": "Cuatro opciones canónicas para mapear jerarquías EER según la cátedra: 1) Opción 1 (Múltiples relaciones: Superclase y Subclases): Tabla para la superclase con atributos comunes + tablas para cada subclase con su PK (que es a la vez FK a la superclase) y atributos específicos. Válida para cualquier jerarquía; 2) Opción 2 (Múltiples relaciones: Solo Subclases): Se elimina la superclase y se crean tablas únicamente para las subclases, duplicando los atributos comunes en cada una. Precondición obligatoria: Total y Disyunta (t, d); 3) Opción 3 (Una sola relación con atributo discriminante de tipo): Se fusiona todo en una única tabla con una columna 'tipo_empleado'. Precondición: Disyunción ('d'); 4) Opción 4 (Una sola relación con varios atributos booleanos de tipo): Una sola tabla con indicadores 'es_tecnico', 'es_secretaria', 'es_licenciado'. Diseñada específicamente para Solapamiento ('o').",
        "explanation": "La Opción 1 es la más general; la Opción 2 ahorra juntas si es (t,d); las Opciones 3 y 4 reducen tablas pero generan valores nulos en atributos que no aplican.",
        "simple_explanation": "Opción 1: Tabla arriba y tablas abajo. Opción 2: Solo tablas abajo (solo si es obligatorio y no se cruzan). Opción 3: Una sola tabla con una columna de tipo. Opción 4: Una sola tabla con casillas de verificación (si se pueden combinar).",
        "example": "Opción 1: Empleado(legajo, nombre, fec_nac) + Tecnico(legajo, grd_exp). Opción 3: Empleado(legajo, nombre, tipo_empleado, grd_exp, vel_esc, especializacion).",
        "related_concepts": ["c_disyuncion_solapamiento", "c_subclase_superclase"],
        "common_confusions": "Intentar aplicar la Opción 2 en una jerarquía con solapamiento (o) o participación parcial (p), lo que causaría pérdida de datos o duplicaciones graves.",
        "difficulty": "experto",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Págs. 54-58",
        "order_idx": 6
    }
]

QUESTIONS = [
    {
        "id": "q_u6_1",
        "topic_id": "u6_t6",
        "concept_id": "c_mapeo_jerarquias_opciones",
        "type": "multiple_choice",
        "difficulty": "dificil",
        "question": "Al mapear una especialización EER, ¿cuál de las 4 opciones requiere de forma estricta e indispensable que la jerarquía sea de Participación Total y Disyunta (t, d) para poder aplicarse válidamente?",
        "options": [
            {"id": "a", "text": "Opción 2: Varias relaciones (solo relaciones de subclase, eliminando la superclase)."},
            {"id": "b", "text": "Opción 1: Varias relaciones (superclase y subclases)."},
            {"id": "c", "text": "Opción 3: Una sola relación con un atributo de tipo."},
            {"id": "d", "text": "Opción 4: Una sola relación con varios atributos de tipo booleanos."}
        ],
        "correct_answer": "a",
        "explanation": "La Opción 2 elimina la tabla de la superclase. Si no fuera total, las entidades que no son de ninguna subclase se perderían. Si no fuera disyunta, una entidad en dos subclases duplicaría sus atributos comunes en dos tablas distintas (Págs. 54-56).",
        "hint1": "Precondición estricta de eliminación de la superclase.",
        "hint2": "Total y Disyunta.",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Págs. 54-56",
        "semantic_hash": "hash_u6_q1"
    },
    {
        "id": "q_u6_2",
        "topic_id": "u6_t2",
        "concept_id": "c_mapeo_relaciones_1n_11",
        "type": "multiple_choice",
        "difficulty": "medio",
        "question": "En el mapeo de una relación binaria 1:1, ¿cuál es el criterio metodológico recomendado por la cátedra para decidir en cuál de las dos entidades debe colocarse la clave foránea (FK)?",
        "options": [
            {"id": "a", "text": "Elegir la entidad que posea participación total (obligatoria) en la relación."},
            {"id": "b", "text": "Elegir siempre la entidad que tenga menor cantidad de atributos."},
            {"id": "c", "text": "Colocar obligatoriamente la clave foránea en ambas entidades de forma simultánea."},
            {"id": "d", "text": "Elegir la entidad con participación parcial para evitar nulos."}
        ],
        "correct_answer": "a",
        "explanation": "En la diapositiva 38 de Clase nro 11 se indica: 'La clave foránea puede estar en cualquiera de las dos entidades. Lo mejor es elegir un tipo de entidad con participación total' (así se evitan valores nulos en la columna de la FK).",
        "hint1": "Se busca minimizar la presencia de valores NULL.",
        "hint2": "Participación total.",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Pág. 38",
        "semantic_hash": "hash_u6_q2"
    },
    {
        "id": "q_u6_3",
        "topic_id": "u6_t5",
        "concept_id": "c_mapeo_recursivas",
        "type": "true_false",
        "difficulty": "medio",
        "question": "Para mapear una relación recursiva o reflexiva con cardinalidad N:N (como la relación de 'amistad' entre personas), se debe agregar una columna en la tabla Persona sin necesidad de crear una tabla nueva.",
        "options": [
            {"id": "v", "text": "VERDADERO"},
            {"id": "f", "text": "FALSO"}
        ],
        "correct_answer": "f",
        "explanation": "FALSO. En el caso de una relación reflexiva N:N (Pág. 53), se crea obligatoriamente una nueva tabla intermedia con el nombre de la relación (ej. Amigo), conteniendo la clave de la entidad dos veces (una por cada rol: DNI_Persona1, DNI_Persona2) como claves foráneas compuestas.",
        "hint1": "Toda relación N:M requiere tabla intermedia.",
        "hint2": "Dos claves foráneas a la misma entidad.",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Pág. 53",
        "semantic_hash": "hash_u6_q3"
    },
    {
        "id": "q_u6_4",
        "topic_id": "u6_t4",
        "concept_id": "c_mapeo_multivaluados_compuestos",
        "type": "multiple_choice",
        "difficulty": "medio",
        "question": "Al mapear un atributo multivaluado (por ejemplo, múltiples correos electrónicos de un empleado), ¿por qué la Opción 1 (guardar todos los correos en un solo campo separados por punto y coma ';') es señalada por la cátedra como no recomendable?",
        "options": [
            {"id": "a", "text": "Porque viola formalmente la Primera Forma Normal (1NF) al almacenar datos no atómicos."},
            {"id": "b", "text": "Porque SQL Server no permite almacenar el carácter punto y coma."},
            {"id": "c", "text": "Porque obliga a crear una relación ternaria."},
            {"id": "d", "text": "Porque duplica la clave primaria en el diccionario de datos."}
        ],
        "correct_answer": "a",
        "explanation": "La diapositiva 44 advierte expresamente: 'NOTA: de esta manera no estamos cumpliendo con la primera forma normal (1NF)' debido a que el atributo almacena múltiples valores en una sola intersección fila-columna.",
        "hint1": "Principio de atomicidad del modelo relacional.",
        "hint2": "Primera Forma Normal (1NF).",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Pág. 44",
        "semantic_hash": "hash_u6_q4"
    }
]
