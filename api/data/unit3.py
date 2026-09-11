"""
Unit 3 Data: Modelo Entidad-Relación Mejorado (EER)
Source: Clase nro 11 - Mássss DER.pdf (Slides 1 a 29)
"""

TOPICS = [
    {
        "id": "u3_t1",
        "unit_number": 3,
        "name": "Subclases, Superclases y Relación de Herencia",
        "description": "Subgrupos significativos de entidades, herencia de atributos y relaciones, y reglas de existencia.",
        "icon": "FolderTree",
        "order_idx": 15
    },
    {
        "id": "u3_t2",
        "unit_number": 3,
        "name": "Especialización vs. Generalización",
        "description": "Proceso Top-Down basado en diferencias vs proceso Bottom-Up basado en similitudes.",
        "icon": "ArrowDownUp",
        "order_idx": 16
    },
    {
        "id": "u3_t3",
        "unit_number": 3,
        "name": "Subclases de Predicado Definido y Atributo Discriminante",
        "description": "Condición de pertenencia en atributos de la superclase vs asignación manual por usuario.",
        "icon": "Filter",
        "order_idx": 17
    },
    {
        "id": "u3_t4",
        "unit_number": 3,
        "name": "Restricciones de Disyunción (d/o) y Completitud (Total/Parcial)",
        "description": "Exclusión mutua ('d') vs solapamiento ('o'). Línea doble (Total) vs línea simple (Parcial).",
        "icon": "CheckSquare",
        "order_idx": 18
    },
    {
        "id": "u3_t5",
        "unit_number": 3,
        "name": "Reglas de Inserción y Borrado en Jerarquías EER",
        "description": "Eliminación en cascada en superclase y requisitos obligatorios de inserción en subclases.",
        "icon": "Trash2",
        "order_idx": 19
    },
    {
        "id": "u3_t6",
        "unit_number": 3,
        "name": "Especialización Jerárquica, Entramada y Tipos UNION",
        "description": "Estructuras en árbol (un solo padre), mallas (múltiples padres) y categorías UNION (superclases heterogéneas).",
        "icon": "GitFork",
        "order_idx": 20
    }
]

CONCEPTS = [
    {
        "id": "c_subclase_superclase",
        "topic_id": "u3_t1",
        "name": "Subclase, Superclase y Relación de Herencia",
        "definition": "Un tipo de entidad puede contar con varios subgrupos significativos que deben representarse de forma explícita: estos subgrupos se denominan Subclases y el tipo general Superclase. Los elementos de una subclase poseen todas las características (atributos y relaciones) de la superclase pero juegan un papel específico. Regla de existencia: una entidad no puede existir en la base de datos siendo sólo miembro de una subclase; para existir también debe pertenecer a una superclase. En cambio, no es necesario que toda entidad de la superclase sea miembro de alguna subclase.",
        "explanation": "El símbolo de subconjunto (∪ en dirección a la subclase) denota que el conjunto de instancias de la subclase es un subconjunto estricto de la superclase.",
        "simple_explanation": "Todo Licenciado o Técnico es un Empleado y hereda su legajo y nombre; pero un Empleado no necesariamente tiene que ser Licenciado.",
        "example": "Superclase EMPLEADO (Legajo, Nombre, Fecha_nacimiento) con subclases TÉCNICO (Grado_experiencia), SECRETARIA (Velocidad_escritura) y LICENCIADO (Especialización).",
        "related_concepts": ["c_especializacion_generalizacion", "c_disyuncion_solapamiento"],
        "common_confusions": "Creer que una entidad puede insertarse en una subclase sin existir en la superclase.",
        "difficulty": "facil",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Págs. 4-7",
        "order_idx": 1
    },
    {
        "id": "c_especializacion_generalizacion",
        "topic_id": "u3_t2",
        "name": "Especialización vs. Generalización",
        "definition": "Dos procesos de abstracción conceptual complementarios: 1) Especialización (Top-Down): proceso de definir un conjunto de subclases a partir de una superclase basándose en características distintivas (énfasis en las diferencias; alguna instancia de la superclase puede no ser instancia de ningún subtipo); 2) Generalización (Bottom-Up): proceso inverso en el que se eliminan las diferencias existentes entre distintas entidades, identificando sus características comunes para generalizarlas en una única superclase (énfasis en las similitudes; toda instancia del supertipo es también instancia de alguno de los subtipos).",
        "explanation": "La especialización desglosa hacia abajo agregando atributos locales; la generalización abstrae hacia arriba sintetizando entidades existentes.",
        "simple_explanation": "Especializar: tengo 'Vehículo' y lo divido en Auto, Camión y Moto. Generalizar: tengo 'Coche' y 'Camión' y descubro que ambos son 'Vehículos' con patente y precio.",
        "example": "Especialización de EMPLEADO por función (Técnico, Secretaria) o por tipo de contratación (Planta, Contratado). Generalización de COCHE y CAMIÓN en VEHÍCULO.",
        "related_concepts": ["c_subclase_superclase", "c_predicado_definido"],
        "common_confusions": "Confundir la dirección del diseño: especializar es analítico y hacia abajo; generalizar es sintético y hacia arriba.",
        "difficulty": "medio",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Págs. 14-19",
        "order_idx": 2
    },
    {
        "id": "c_predicado_definido",
        "topic_id": "u3_t3",
        "name": "Subclases de Predicado Definido y Atributo Discriminante",
        "definition": "Ocurre cuando es posible determinar con exactitud las entidades que se convertirán en miembros de cada subclase situando una condición sobre el valor de un atributo de la superclase. Si todas las subclases tienen su condición en el mismo atributo, se denomina 'especialización de atributo definido'. El atributo de la superclase que da la condición de pertenencia se denomina Atributo Discriminante o Definitorio. En contraposición, en las subclases 'definidas por el usuario', las pertenencias son especificadas individual y manualmente por los usuarios, sin regla automática.",
        "explanation": "En el DER se anota la condición al lado de la línea que conecta la subclase al círculo de especialización.",
        "simple_explanation": "Si el campo 'tipo_vehiculo' dice 'M', el sistema sabe automáticamente que es de la subclase MOTO sin intervención humana.",
        "example": "En VEHÍCULO, el atributo discriminante 'tipo' determina la pertenencia a CAMIÓN ('C'), TURISMO ('T') o MOTO ('M').",
        "related_concepts": ["c_disyuncion_solapamiento", "c_subclase_superclase"],
        "common_confusions": "Confundir un atributo discriminante con la clave primaria de la superclase.",
        "difficulty": "medio",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Págs. 20-22",
        "order_idx": 3
    },
    {
        "id": "c_disyuncion_solapamiento",
        "topic_id": "u3_t4",
        "name": "Restricciones de Disyunción (d/o) y Completitud (Total/Parcial)",
        "definition": "Reglas de pertenencia en jerarquías EER: 1) Disyunción (d): establece que una entidad puede ser, como máximo, miembro de una sola subclase de la especialización (se dibuja 'd' en el círculo). Si el atributo discriminante es monovaluado, implica disyunción automática; 2) Solapamiento (o): las entidades pueden ser miembros de más de una subclase simultáneamente (se dibuja 'o' en el círculo); 3) Integridad Total: cada entidad de la superclase DEBE ser miembro de al menos una subclase (se representa con línea doble entre la superclase y el círculo); 4) Integridad Parcial: una entidad puede no pertenecer a ninguna subclase (línea simple).",
        "explanation": "Las combinaciones posibles son cuatro: (t, d) total disyunta, (p, d) parcial disyunta, (t, o) total solapada, (p, o) parcial solapada.",
        "simple_explanation": "Disyunción (d) = excluyente (o sos A o sos B). Solapamiento (o) = podés ser A y B al mismo tiempo. Total (doble línea) = obligatorio pertenecer a una. Parcial = podés no ser ninguna.",
        "example": "Disyunción: Una CUENTA es Corriente o Caja de Ahorro ('d'). Solapamiento: Una PARTE de una fábrica puede ser a la vez 'Fabricada' y 'Comprada' ('o').",
        "related_concepts": ["c_reglas_especializacion", "c_subclase_superclase"],
        "common_confusions": "Creer que 'd' significa doble línea. 'd' es disyunción (letra d en el círculo); la línea doble significa completitud total.",
        "difficulty": "medio",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Págs. 23-25",
        "order_idx": 4
    },
    {
        "id": "c_reglas_especializacion",
        "topic_id": "u3_t5",
        "name": "Reglas de Inserción y Borrado en Jerarquías",
        "definition": "Reglas operativas estrictas que preservan la integridad semántica del EER: 1) Borrado: El borrado de una entidad de una superclase implica su eliminación automática en cascada de todas las subclases a las que pertenece; 2) Inserción en predicado definido: Insertar una entidad en la superclase supone que debe insertarse automáticamente en todas las subclases cuyas reglas cumpla; 3) Inserción en especialización total: La inserción de una entidad en una superclase de especialización total conlleva que sea incluida obligatoriamente en al menos una de las subclases.",
        "explanation": "Garantizan que no existan tuplas huérfanas en las subclases ni violaciones a la restricción de completitud.",
        "simple_explanation": "Si despiden al empleado de la empresa, desaparece automáticamente de la tabla de técnicos y secretarias.",
        "example": "Si se borra el Empleado con Legajo 100, se borra su registro en la subclase LICENCIADO de inmediato.",
        "related_concepts": ["c_disyuncion_solapamiento", "c_subclase_superclase"],
        "common_confusions": "Intentar borrar una entidad de la superclase manteniendo el registro en la subclase.",
        "difficulty": "medio",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Pág. 26",
        "order_idx": 5
    },
    {
        "id": "c_estructuras_eer_union",
        "topic_id": "u3_t6",
        "name": "Especialización Jerárquica, Entramada y Tipos UNION",
        "definition": "Topologías de herencia EER: 1) Especialización Jerárquica: cada subclase participa en una única relación clase/subclase, es decir, tiene un solo padre, formando una estructura estricta en árbol; 2) Especialización Entramada: una subclase participa en más de una relación clase/subclase, poseyendo múltiples padres (herencia múltiple o red); 3) Tipos UNION (Categorías): modelan una subclase común que representa la unión (U) de varias superclases de tipos de entidad completamente diferentes e independientes (superclases heterogéneas).",
        "explanation": "Una categoría UNION permite que una entidad pertenezca a una superclase O a otra (ej. un Propietario de un vehículo puede ser una Persona, un Banco o una Empresa).",
        "simple_explanation": "Jerárquica = un solo padre. Entramada = dos o más padres. Categoría UNION = una subclase que puede pertenecer a entidades distintas (Persona, Banco o Empresa).",
        "example": "Subclase PROPIETARIO conectada con círculo 'U' a tres superclases: PERSONA (DNI), BANCO (NumPermiso) y EMPRESA (CUIT).",
        "related_concepts": ["c_disyuncion_solapamiento", "c_subclase_superclase"],
        "common_confusions": "Confundir herencia múltiple (entramada, una entidad es todas las superclases) con Categoría UNION (una entidad es una superclase U otra).",
        "difficulty": "dificil",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Págs. 27-29",
        "order_idx": 6
    }
]

QUESTIONS = [
    {
        "id": "q_u3_1",
        "topic_id": "u3_t4",
        "concept_id": "c_disyuncion_solapamiento",
        "type": "multiple_choice",
        "difficulty": "medio",
        "question": "En un diagrama EER, ¿qué significado formal tiene la presencia de una 'LÍNEA DOBLE' que conecta una superclase con el círculo de especialización?",
        "options": [
            {"id": "a", "text": "Restricción de Integridad Total (toda entidad de la superclase debe pertenecer obligatoriamente al menos a una subclase)."},
            {"id": "b", "text": "Restricción de Disyunción estricta (no puede haber solapamiento)."},
            {"id": "c", "text": "Que las subclases poseen claves foráneas compuestas."},
            {"id": "d", "text": "Que la superclase es una entidad débil."}
        ],
        "correct_answer": "a",
        "explanation": "La línea doble denota Completitud o Integridad Total: no pueden existir entidades en la superclase que queden sin clasificar en alguna de las subclases (Pág. 25).",
        "hint1": "Línea doble = totalidad / obligatoriedad.",
        "hint2": "La línea simple indica participación parcial.",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Pág. 25",
        "semantic_hash": "hash_u3_q1"
    },
    {
        "id": "q_u3_2",
        "topic_id": "u3_t1",
        "concept_id": "c_subclase_superclase",
        "type": "true_false",
        "difficulty": "facil",
        "question": "En el modelo EER, una entidad puede existir en la base de datos perteneciendo únicamente a una subclase sin figurar en la superclase.",
        "options": [
            {"id": "v", "text": "VERDADERO"},
            {"id": "f", "text": "FALSO"}
        ],
        "correct_answer": "f",
        "explanation": "FALSO. Una de las reglas de existencia fundamentales del EER (Pág. 5) establece que una entidad no puede existir en la base de datos siendo sólo miembro de una subclase; para existir debe pertenecer obligatoriamente también a la superclase.",
        "hint1": "Regla de existencia en subclases.",
        "hint2": "Toda instancia de una subclase es ante todo una instancia de la superclase.",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Pág. 5",
        "semantic_hash": "hash_u3_q2"
    },
    {
        "id": "q_u3_3",
        "topic_id": "u3_t6",
        "concept_id": "c_estructuras_eer_union",
        "type": "multiple_choice",
        "difficulty": "dificil",
        "question": "¿Cómo se denomina la estructura del modelo EER en la cual una subclase representa la unión de varias superclases heterogéneas con claves primarias independientes (por ejemplo, PROPIETARIO siendo Persona, Banco o Empresa)?",
        "options": [
            {"id": "a", "text": "Tipo UNION o Categoría"},
            {"id": "b", "text": "Especialización Jerárquica"},
            {"id": "c", "text": "Especialización Entramada Pura"},
            {"id": "d", "text": "Relación Recursiva Reflexiva"}
        ],
        "correct_answer": "a",
        "explanation": "El Tipo UNION o Categoría (Pág. 29) modela una relación donde la subclase es una colección de superclases distintas (representada con la letra U en el círculo de conexión).",
        "hint1": "Se denota con una 'U'.",
        "hint2": "Modela superclases que tienen distintas claves primarias.",
        "source_document": "Clase nro 11 - Mássss DER.pdf",
        "source_page": "Pág. 29",
        "semantic_hash": "hash_u3_q3"
    }
]
