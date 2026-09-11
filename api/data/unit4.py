"""
Unit 4 Data: El Modelo Relacional y las 12 Reglas de Codd
Source: El Modelo Relacional.pdf (34 slides)
"""

TOPICS = [
    {
        "id": "u4_t1",
        "unit_number": 4,
        "name": "Historia, Objetivos y Pilares del Modelo Relacional",
        "description": "Edgar F. Codd (1970), Cantor y Childs (teoría de conjuntos). Los 3 pilares: Estructura, Manipulación e Integridad.",
        "icon": "History",
        "order_idx": 21
    },
    {
        "id": "u4_t2",
        "unit_number": 4,
        "name": "Estructura Formal: Dominios, Relaciones, Tuplas, Grado y Cardinalidad",
        "description": "Definición matemática de dominio por extensión e intensión, atributos, tuplas, grado (columnas) y cardinalidad (filas).",
        "icon": "Table",
        "order_idx": 22
    },
    {
        "id": "u4_t3",
        "unit_number": 4,
        "name": "Propiedades de las Relaciones y Sinónimos Referenciales",
        "description": "Unicidad de tuplas, atomicidad monovaluada, orden irrelevante y cuadro de correspondencias (MR vs SGBD vs Ficheros).",
        "icon": "Repeat",
        "order_idx": 23
    },
    {
        "id": "u4_t4",
        "unit_number": 4,
        "name": "Teoría de Claves: Superclave, Candidata, Primaria, Alternativa y Foránea",
        "description": "Unicidad y minimidad. Selección de clave primaria, restricciones UNIQUE y claves ajenas.",
        "icon": "Key",
        "order_idx": 24
    },
    {
        "id": "u4_t5",
        "unit_number": 4,
        "name": "Semántica Estricta del Valor NULL",
        "description": "Ausencia de valor o valor desconocido. Distinción ontológica: NULL no es cadena vacía ('') ni cero numérico (0).",
        "icon": "HelpCircle",
        "order_idx": 25
    },
    {
        "id": "u4_t6",
        "unit_number": 4,
        "name": "Reglas de Integridad, Restricciones y Políticas de FK",
        "description": "Reglas de usuario vs modelo. Restricciones inherentes vs semánticas. Políticas: NO ACTION, CASCADE, SET NULL, DEFAULT.",
        "icon": "ShieldAlert",
        "order_idx": 26
    },
    {
        "id": "u4_t7",
        "unit_number": 4,
        "name": "Las 12 Reglas de Codd Comentadas",
        "description": "Análisis exhaustivo de los 12 principios fundacionales de Edgar F. Codd para sistemas relacionales plenos.",
        "icon": "Award",
        "order_idx": 27
    }
]

CONCEPTS = [
    {
        "id": "c_historia_pilares_mr",
        "topic_id": "u4_t1",
        "name": "Historia, Objetivos y Pilares del Modelo Relacional",
        "definition": "Publicado en 1970 por Edgar Frank Codd ('A Relational Model of Data for Large Shared Data Banks'), apoyado en la teoría de conjuntos de Cantor y Childs. Define tres componentes fundamentales: 1) Estructura: representa la información en forma de relaciones (tablas); 2) Manipulación: operaciones de consulta y actualización algebraica/declarativa; 3) Integridad: condiciones que los datos deben cumplir obligatoriamente. Objetivos clave: Independencia física, Independencia lógica, Flexibilidad, Uniformidad (solo tablas) y Sencillez de manejo.",
        "explanation": "Codd buscaba que los usuarios no tuviesen que aprender los detalles físicos del almacenamiento (como ocurría en el modelo en red CODASYL).",
        "simple_explanation": "Antes de Codd los datos eran archivos complejos entrelazados; Codd propuso ver todo como tablas matemáticas simples e independientes del disco.",
        "example": "El paso del modelo en red al estándar SQL/ANSI en 1986 y el surgimiento de Oracle, DB2, Postgres y MySQL.",
        "related_concepts": ["c_estructura_mr", "c_teoria_claves"],
        "common_confusions": "Creer que Codd inventó el SQL (Codd definió el modelo relacional matemático; el lenguaje Sequel/SQL fue desarrollado por Chamberlin y Boyce en IBM).",
        "difficulty": "facil",
        "source_document": "El Modelo Relacional.pdf",
        "source_page": "Págs. 3-9",
        "order_idx": 1
    },
    {
        "id": "c_estructura_mr",
        "topic_id": "u4_t2",
        "name": "Dominio, Relación, Atributo, Tupla, Grado y Cardinalidad",
        "definition": "Elementos formales del Modelo Relacional: 1) Dominio: conjunto nominado, homogéneo y válido de valores atómicos de referencia (definible por Extensión [enumeración de elementos] o por Intensión [propiedad/rango de valores admisibles], así como dominios compuestos como Fecha); 2) Atributo: propiedad de la relación definida sobre un dominio (columna); 3) Tupla: ocurrencia o elemento del conjunto de la relación (fila); 4) Grado: número de atributos o dominios de la relación (n° de columnas); 5) Cardinalidad: número de tuplas que contiene la relación en un momento dado (n° de filas).",
        "explanation": "Una relación R sobre los dominios D1, D2, ..., Dn es un subconjunto formal del producto cartesiano D1 × D2 × ... × Dn.",
        "simple_explanation": "Grado = cantidad de columnas. Cardinalidad = cantidad de filas. Dominio = el tipo de dato y sus valores permitidos.",
        "example": "Tabla ALUMNOS con 5 columnas (legajo, nombre, apellido, fecha_nac, email) y 100 estudiantes registrados: Grado = 5, Cardinalidad = 100.",
        "related_concepts": ["c_propiedades_relaciones", "c_teoria_claves"],
        "common_confusions": "Invertir los términos: creer que el Grado son las filas y la Cardinalidad las columnas.",
        "difficulty": "medio",
        "source_document": "El Modelo Relacional.pdf",
        "source_page": "Págs. 10-13",
        "order_idx": 2
    },
    {
        "id": "c_propiedades_relaciones",
        "topic_id": "u4_t3",
        "name": "Propiedades de las Relaciones y Sinónimos Referenciales",
        "definition": "Seis propiedades inviolables de toda relación relacional: 1) Cada tabla debe tener un nombre distinto en el esquema; 2) Cada atributo solo puede tomar un valor único atómico en cada tupla (no multivaluado); 3) Cada atributo tiene un nombre distinto dentro de la tabla; 4) Cada tupla es única (no existen tuplas duplicadas); 5) El orden de los atributos no importa; 6) El orden de las tuplas no importa. Cuadro de sinónimos referenciales: Relación = Tabla = Fichero; Tupla = Fila = Registro; Atributo = Columna = Campo; Grado = N° Columnas = N° Campos; Cardinalidad = N° Filas = N° Registros.",
        "explanation": "Dado que una relación es matemáticamente un conjunto, no admite elementos repetidos ni orden posicional intrínseco.",
        "simple_explanation": "En una tabla no puede haber dos filas exactamente iguales y no importa si una fila está arriba o abajo: la información es la misma.",
        "example": "Si cambiás de orden las columnas Nombre y Apellido en un SELECT, la relación formal sigue siendo matemáticamente equivalente.",
        "related_concepts": ["c_estructura_mr", "c_teoria_claves"],
        "common_confusions": "Asumir que las filas se almacenan ordenadas cronológicamente en el modelo relacional (eso es solo una propiedad de archivos secuenciales antiguos).",
        "difficulty": "facil",
        "source_document": "El Modelo Relacional.pdf",
        "source_page": "Págs. 14-15",
        "order_idx": 3
    },
    {
        "id": "c_teoria_claves",
        "topic_id": "u4_t4",
        "name": "Teoría de Claves: Superclave, Candidata, Primaria, Alternativa y Foránea",
        "definition": "Jerarquía formal de identificación: 1) Superclave: subconjunto de atributos que identifica inequívocamente cada tupla de la relación; 2) Clave Candidata: superclave mínima (no contiene ningún subconjunto propio que sea superclave); 3) Clave Primaria (PK): clave candidata elegida por el diseñador para identificar las filas (debe ser única, no nula y preferentemente pequeña e inmutable); 4) Clave Alternativa (AK / Unique Key): cualquier clave candidata no seleccionada como primaria; 5) Clave Foránea / Externa (FK): atributo(s) cuyos valores hacen referencia obligatoria a la clave primaria de otra tabla relacionada.",
        "explanation": "Las claves primarias son los únicos datos que generan redundancia planificada en el modelo relacional al propagarse como claves foráneas para vincular tablas.",
        "simple_explanation": "Superclave = cualquier combinación que no se repita. Candidata = la combinación justa sin sobras. Primaria = la que elegís como ID oficial.",
        "example": "En ESCRITOR (DNI, Nombre, Apellido, Email): {DNI, Nombre} es superclave; {DNI} y {Email} son claves candidatas; se elige {DNI} como Primaria y {Email} queda como Alternativa.",
        "related_concepts": ["c_politicas_fk", "c_semantica_null"],
        "common_confusions": "Pensar que una superclave no puede tener atributos redundantes. Sí puede tenerlos; es la clave candidata la que exige minimidad.",
        "difficulty": "medio",
        "source_document": "El Modelo Relacional.pdf",
        "source_page": "Págs. 16-19",
        "order_idx": 4
    },
    {
        "id": "c_semantica_null",
        "topic_id": "u4_t5",
        "name": "Semántica Estricta del Valor NULL",
        "definition": "En el modelo relacional, NULL indica la ausencia de valor o que el valor es desconocido o no aplicable. Para Codd, el nulo otorga significado tanto como un dato numérico o de texto. Principio fundamental: el texto vacío '' NO significa lo mismo que valor nulo, y el valor numérico cero (0) TAMPOCO significa nulo. En operaciones lógicas, el NULL introduce la lógica trivaluada (True, False, Unknown).",
        "explanation": "Cero es un número conocido; cadena vacía es un texto conocido de longitud cero; NULL es la total ausencia de información.",
        "simple_explanation": "Tener saldo $0 en el banco no es lo mismo que no tener cuenta (NULL). Tener teléfono sin registrar (NULL) no es lo mismo que tener teléfono número 0.",
        "example": "Si una persona no informa su teléfono, la columna `telefono` almacena NULL. Si se ejecuta `telefono = NULL` en SQL, el resultado no es True ni False, sino Unknown.",
        "related_concepts": ["c_teoria_claves", "c_politicas_fk"],
        "common_confusions": "Comparar un atributo con NULL usando el operador '=' (debe usarse siempre `IS NULL` o `IS NOT NULL`).",
        "difficulty": "medio",
        "source_document": "El Modelo Relacional.pdf",
        "source_page": "Pág. 20",
        "order_idx": 5
    },
    {
        "id": "c_politicas_fk",
        "topic_id": "u4_t6",
        "name": "Restricciones de Integridad y Políticas de FK",
        "definition": "Clasificación de restricciones según la cátedra: 1) Inherentes: surgen de la propia naturaleza relacional (no hay filas repetidas, orden no significativo, intersección atómica fila-columna); 2) Semánticas: reglas impuestas al esquema (PRIMARY KEY, UNIQUE, NOT NULL, CHECK, DEFAULT, FOREIGN KEY). Políticas de Actualización y Eliminación ante borrado en la tabla principal referenciada por FK: a) Prohibir la operación (NO ACTION / RESTRICT): no permite modificar o borrar la PK si existen FKs vinculadas (opción rígida por defecto); b) Cascada (CASCADE): propaga el borrado o modificación a todas las filas hijas relacionadas; c) Colocar nulos (SET NULL): cambia el valor de la FK a NULL en las filas hijas; d) Valor por defecto (SET DEFAULT): asigna un valor predeterminado fijado en el esquema.",
        "explanation": "La Integridad Referencial asegura que nunca existan registros hijos con claves foráneas apuntando a registros padres inexistentes.",
        "simple_explanation": "Si borrás un cliente: NO ACTION no te deja borrarlo si tiene facturas; CASCADE te borra el cliente y todas sus facturas; SET NULL deja las facturas con cliente vacío.",
        "example": "En una tabla EMPLEADO con FK a DEPARTAMENTO: si se borra el departamento Ventas, con CASCADE se borran todos los empleados de Ventas; con SET NULL los empleados quedan con departamento en NULL.",
        "related_concepts": ["c_teoria_claves", "c_12_reglas_codd"],
        "common_confusions": "Creer que SET NULL puede aplicarse si la columna de la clave foránea está definida con la restricción NOT NULL (provocaría un error de violación de integridad).",
        "difficulty": "dificil",
        "source_document": "El Modelo Relacional.pdf",
        "source_page": "Págs. 21-29",
        "order_idx": 6
    },
    {
        "id": "c_12_reglas_codd",
        "topic_id": "u4_t7",
        "name": "Las 12 Reglas de Codd Comentadas",
        "definition": "Doce mandamientos formulados por Edgar F. Codd para evaluar si un SGBD es verdaderamente relacional: [1] Información (todos los datos y metadatos residen en tablas lógicas); [2] Acceso Garantizado (todo dato es accesible por nombre de tabla + clave primaria + nombre de columna); [3] Tratamiento Sistemático de Valores Nulos (manejo uniforme e independiente del tipo de dato); [4] Catálogo en Línea basado en el modelo relacional (el diccionario de datos se consulta igual que las tablas de usuario); [5] Sublenguaje de Datos Completo (debe soportar DDL, DML, DCL, TCL en un solo lenguaje como SQL); [6] Actualización de Vistas (el motor debe permitir modificar datos a través de vistas teóricamente actualizables); [7] Inserción, Modificación y Eliminación de Alto Nivel (operaciones sobre conjuntos de filas, no registro a registro tipo cursor); [8] Independencia Física de Datos (cambios en almacenamiento no afectan esquemas externos); [9] Independencia Lógica de Datos (cambios en tablas lógicas no rompen vistas ni programas); [10] Independencia de Integridad (las reglas se almacenan en el catálogo de la BD, no en el código de la app); [11] Independencia de la Distribución (las consultas funcionan idéntico si la BD está distribuida o centralizada); [12] No Subversión (ningún lenguaje de bajo nivel puede saltarse las reglas de integridad del modelo).",
        "explanation": "Constituyen el estándar de oro de fidelidad arquitectónica para cualquier SGBD relacional moderno.",
        "simple_explanation": "Son las 12 reglas que inventó Codd para certificar que una base de datos es un verdadero sistema relacional y no un engaño comercial.",
        "example": "Regla 10: Definir un `CHECK (precio > 0)` en la base de datos en vez de programarlo en un `if` de JavaScript en la interfaz web.",
        "related_concepts": ["c_historia_pilares_mr", "c_politicas_fk"],
        "common_confusions": "Confundir la Regla 8 (Independencia Física) con la Regla 9 (Independencia Lógica).",
        "difficulty": "dificil",
        "source_document": "El Modelo Relacional.pdf",
        "source_page": "Págs. 30-32",
        "order_idx": 7
    }
]

QUESTIONS = [
    {
        "id": "q_u4_1",
        "topic_id": "u4_t4",
        "concept_id": "c_teoria_claves",
        "type": "multiple_choice",
        "difficulty": "medio",
        "question": "En el modelo relacional de Codd, ¿cuál de las siguientes afirmaciones describe con rigor la diferencia entre una Superclave y una Clave Candidata?",
        "options": [
            {"id": "a", "text": "Una superclave es cualquier conjunto de atributos que identifica unívocamente a cada tupla; la clave candidata es una superclave minimal (sin atributos redundantes)."},
            {"id": "b", "text": "La superclave es la clave primaria elegida y la candidata es la que se descarta."},
            {"id": "c", "text": "La superclave admite valores nulos en todos sus campos y la clave candidata no."},
            {"id": "d", "text": "Una relación solo puede tener una única superclave pero múltiples claves candidatas."}
        ],
        "correct_answer": "a",
        "explanation": "La opción A es la definición formal exacta: la clave candidata es una superclave con la propiedad de minimidad (si se elimina cualquier atributo, pierde la capacidad de identificar unívocamente las tuplas).",
        "hint1": "Criterio de minimidad.",
        "hint2": "Si le agregás cualquier campo extra a una clave candidata, sigue siendo superclave pero deja de ser candidata.",
        "source_document": "El Modelo Relacional.pdf",
        "source_page": "Pág. 16",
        "semantic_hash": "hash_u4_q1"
    },
    {
        "id": "q_u4_2",
        "topic_id": "u4_t5",
        "concept_id": "c_semantica_null",
        "type": "true_false",
        "difficulty": "facil",
        "question": "En el modelo relacional, un valor NULL es exactamente equivalente a una cadena de caracteres vacía ('') en campos de texto, o al valor cero (0) en campos numéricos.",
        "options": [
            {"id": "v", "text": "VERDADERO"},
            {"id": "f", "text": "FALSO"}
        ],
        "correct_answer": "f",
        "explanation": "FALSO. El texto vacío '' es un dato de texto conocido de longitud cero, y 0 es un valor numérico definido. NULL representa la ausencia de valor o valor desconocido (Pág. 20).",
        "hint1": "Ausencia de valor no es cero.",
        "hint2": "Revisá la diapositiva 20 de El Modelo Relacional.",
        "source_document": "El Modelo Relacional.pdf",
        "source_page": "Pág. 20",
        "semantic_hash": "hash_u4_q2"
    },
    {
        "id": "q_u4_3",
        "topic_id": "u4_t6",
        "concept_id": "c_politicas_fk",
        "type": "multiple_choice",
        "difficulty": "dificil",
        "question": "Al definir una clave foránea (FK), ¿qué política de eliminación provoca que, al intentar borrar un registro de la tabla principal, la operación sea rechazada y abortada si existen registros relacionados en la tabla secundaria?",
        "options": [
            {"id": "a", "text": "NO ACTION (o RESTRICT)"},
            {"id": "b", "text": "CASCADE"},
            {"id": "c", "text": "SET NULL"},
            {"id": "d", "text": "SET DEFAULT"}
        ],
        "correct_answer": "a",
        "explanation": "La opción NO ACTION (Pág. 28) prohíbe la operación: no permite hacer en las claves principales ninguna eliminación si existen claves secundarias relacionadas con ellas. Es la opción más rígida y habitual por defecto.",
        "hint1": "Prohibir la operación.",
        "hint2": "Protege a los registros hijos impidiendo que se borre su padre.",
        "source_document": "El Modelo Relacional.pdf",
        "source_page": "Pág. 28",
        "semantic_hash": "hash_u4_q3"
    },
    {
        "id": "q_u4_4",
        "topic_id": "u4_t7",
        "concept_id": "c_12_reglas_codd",
        "type": "multiple_choice",
        "difficulty": "dificil",
        "question": "¿Cuál es el postulado de la Regla 10 (Independencia de Integridad) de las 12 Reglas de Codd?",
        "options": [
            {"id": "a", "text": "Las reglas de integridad deben almacenarse en el diccionario de datos de la base de datos, no en los programas de aplicación."},
            {"id": "b", "text": "Todos los datos deben ser accesibles únicamente conociendo la posición física del archivo en disco."},
            {"id": "c", "text": "Las vistas deben actualizarse manualmente por el DBA una vez por semana."},
            {"id": "d", "text": "El sublenguaje relacional no debe permitir transacciones concurrentes."}
        ],
        "correct_answer": "a",
        "explanation": "La Regla 10 (Pág. 32) establece: 'Las reglas de integridad deben almacenarse en la base de datos (en el diccionario de datos), no en los programas de aplicación. Eso permite que dichas reglas se cumplan siempre independientemente de la forma de acceder.'",
        "hint1": "Integridad en la base de datos, no en el frontend.",
        "hint2": "Diccionario de datos centralizado.",
        "source_document": "El Modelo Relacional.pdf",
        "source_page": "Pág. 32",
        "semantic_hash": "hash_u4_q4"
    }
]
