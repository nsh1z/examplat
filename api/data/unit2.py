"""
Unit 2 Data: Modelado Conceptual — Diagramas Entidad-Relación (DER Clásico)
Source: Diagramas de Entidad Relación y Modelo de Datos.pdf (28 slides)
"""

TOPICS = [
    {
        "id": "u2_t1",
        "unit_number": 2,
        "name": "Definición, Importancia y Niveles de Abstracción",
        "description": "Definición del DER, valor para desarrolladores y niveles conceptual, lógico y físico.",
        "icon": "Network",
        "order_idx": 9
    },
    {
        "id": "u2_t2",
        "unit_number": 2,
        "name": "Elementos Fundamentales del DER y Notaciones",
        "description": "Entidades (sustantivos/rectángulos), Relaciones (verbos/rombos), Atributos (óvalos) y Cardinalidades.",
        "icon": "Box",
        "order_idx": 10
    },
    {
        "id": "u2_t3",
        "unit_number": 2,
        "name": "Diferencias entre Modelo Entidad-Relación y Modelo Relacional",
        "description": "Cuadro comparativo oficial: Labor, Descripción de datos, Relación y Cartografía de cardinalidades.",
        "icon": "Columns",
        "order_idx": 11
    },
    {
        "id": "u2_t4",
        "unit_number": 2,
        "name": "Reglas Estrictas de Construcción de un DER",
        "description": "Normas inviolables de conectividad en grafos DER, prohibiciones de enlace y depuración.",
        "icon": "CheckSquare",
        "order_idx": 12
    },
    {
        "id": "u2_t5",
        "unit_number": 2,
        "name": "Limitaciones del Modelo Entidad-Relación",
        "description": "Exclusividad para datos relacionales, inadecuación para datos no estructurados y problemas de integración.",
        "icon": "AlertTriangle",
        "order_idx": 13
    },
    {
        "id": "u2_t6",
        "unit_number": 2,
        "name": "Caso Integral de Modelado: Empresa Constructora de Edificios",
        "description": "Análisis y diagrama del caso oficial: Personal, Obras, Tareas, Profesionales, Recursos y Proveedores.",
        "icon": "Building",
        "order_idx": 14
    }
]

CONCEPTS = [
    {
        "id": "c_niveles_modelado",
        "topic_id": "u2_t1",
        "name": "Modelos de Datos: Conceptual, Lógico y Físico",
        "definition": "El modelado de datos describe una manera de diseñar la base de datos a tres niveles de abstracción: 1) Conceptual: visualización de más alto nivel con menor cantidad de detalle que representa el alcance y arquitectura global; 2) Lógico: define entidades transaccionales y operativas detalladas de forma independiente de la tecnología (DER, Modelo Relacional); 3) Físico: muestra los detalles tecnológicos de implementación (tablas, columnas, tipos y claves en el SGBD).",
        "explanation": "Cada nivel traduce los requerimientos del mundo real hacia la implementación física en disco.",
        "simple_explanation": "El conceptual es el plano del arquitecto; el lógico es el plano estructural; el físico es cómo se construyen las paredes con ladrillos específicos.",
        "example": "Conceptual: Diagrama de alto nivel con 'Cliente' y 'Pedido'. Lógico: Entidad CLIENTE con clave DNI y relación 'Realiza' 1:N. Físico: Tabla CLIENTES en PostgreSQL con tipos VARCHAR(50), INT y restricciones.",
        "related_concepts": ["c_elementos_der", "c_der_vs_mr"],
        "common_confusions": "Pensar que en el modelo lógico ya se eligen tipos de datos específicos de un motor como SQL Server u Oracle.",
        "difficulty": "facil",
        "source_document": "Diagramas de Entidad Relación y Modelo de Datos.pdf",
        "source_page": "Págs. 7-8",
        "order_idx": 1
    },
    {
        "id": "c_elementos_der",
        "topic_id": "u2_t2",
        "name": "Elementos Fundamentales del Diagrama Entidad-Relación",
        "definition": "Herramienta gráfica que representa el esquema de la base de datos mediante tres elementos principales: 1) Entidades: personas, objetos o conceptos del mundo real que poseen datos almacenados (sustantivos, representados con rectángulos); 2) Relaciones: describen cómo interactúan o se asocian las entidades entre sí (verbos, representados con rombos); 3) Atributos: características o propiedades de las entidades y relaciones (óvalos).",
        "explanation": "Un DER modela los datos como una red de entidades conectadas a través de relaciones etiquetadas con su cardinalidad (1-1, 1-N, N-M).",
        "simple_explanation": "Las entidades son sustantivos (Estudiante, Curso); las relaciones son verbos que las unen (Se inscribe en).",
        "example": "Entidad 'Estudiante' conectada mediante el rombo 'Se Inscribe' (1:N) con la entidad 'Curso'.",
        "related_concepts": ["c_reglas_construccion_der", "c_niveles_modelado"],
        "common_confusions": "Confundir una entidad con un atributo (ej. crear una entidad 'Precio' en lugar de colocarlo como atributo de Producto).",
        "difficulty": "facil",
        "source_document": "Diagramas de Entidad Relación y Modelo de Datos.pdf",
        "source_page": "Págs. 11-12",
        "order_idx": 2
    },
    {
        "id": "c_der_vs_mr",
        "topic_id": "u2_t3",
        "name": "Diferencias entre Modelo Entidad-Relación y Modelo Relacional",
        "definition": "Comparación estructural y metodológica según la cátedra: 1) Labor: El Modelo ER representa la colección de objetos (entidades) y sus relaciones conceptuales; el Modelo Relacional representa la colección de tablas y la relación entre ellas; 2) Descripción: El ER describe datos como conjunto de entidades, relaciones y atributos; el Relacional los describe en tablas con Dominios, Atributos y Tuplas; 3) Relación: En el ER es más fácil entender visualmente la relación entre entidades; en el Relacional es menos fácil derivar relaciones directas entre tablas; 4) Cartografía: El ER describe la asignación explícita de cardinalidades (1-1, 1-N, N-M); el Relacional no describe cardinalidades de mapeo en su estructura básica.",
        "explanation": "El Modelo E-R es específico para cada entidad del mundo real, mientras que el Modelo Relacional es específico para cada tabla implementada en el sistema.",
        "simple_explanation": "El DER es visual y conceptual para entender el negocio; el Relacional es matemático y en tablas para que la computadora lo procese.",
        "example": "En el DER una relación M:N se dibuja como un simple rombo entre dos rectángulos; en el Modelo Relacional debe crearse obligatoriamente una tercera tabla intermedia.",
        "related_concepts": ["c_elementos_der", "c_estructura_mr"],
        "common_confusions": "Creer que 'relación' significa lo mismo en ambos modelos: en el DER es la asociación entre entidades (el rombo); en el Modelo Relacional de Codd la relación es la tabla misma.",
        "difficulty": "medio",
        "source_document": "Diagramas de Entidad Relación y Modelo de Datos.pdf",
        "source_page": "Págs. 9-10",
        "order_idx": 3
    },
    {
        "id": "c_reglas_construccion_der",
        "topic_id": "u2_t4",
        "name": "Reglas Inviolables de Construcción de un DER",
        "definition": "Conjunto de normas formales para garantizar la validez sintáctica y semántica de un DER: 1) Una entidad puede estar conectada a una o más relaciones; 2) Una relación debe conectarse a una o más entidades; 3) Una entidad NUNCA puede estar conectada directamente a otra entidad; 4) Una relación NUNCA puede estar conectada directamente a otra relación; 5) No pueden existir distintos elementos con el mismo nombre; 6) No incluir relaciones irrelevantes para el sistema; 7) Si una entidad solo tiene su identificador como atributo, debe eliminarse e incluirse la información en otra entidad.",
        "explanation": "Toda línea en un DER debe conectar alternadamente una entidad con una relación. Dos rectángulos o dos rombos unidos directamente violan la gramática formal.",
        "simple_explanation": "Siempre se dibuja: Rectángulo - Línea - Rombo - Línea - Rectángulo. Nunca dos rectángulos pegados ni dos rombos pegados.",
        "example": "Si en un modelo tenemos 'Cliente' y 'Factura', no se puede trazar una línea directa entre ambos: debe insertarse el rombo 'Emite'.",
        "related_concepts": ["c_elementos_der", "c_limitaciones_der"],
        "common_confusions": "Conectar dos rombos para indicar que un proceso ocurre después de otro (los eventos secuenciales se modelan como entidades o atributos, no uniendo rombos).",
        "difficulty": "facil",
        "source_document": "Diagramas de Entidad Relación y Modelo de Datos.pdf",
        "source_page": "Pág. 17",
        "order_idx": 4
    },
    {
        "id": "c_limitaciones_der",
        "topic_id": "u2_t5",
        "name": "Limitaciones del Modelo Entidad-Relación",
        "definition": "Restricciones intrínsecas del paradigma DER señaladas por la cátedra: 1) Exclusivo para datos relacionales: su propósito es solo mostrar relaciones y estructuras tabulares; 2) Inadecuado para datos no estructurados o semiestructurados (como logs, XML, documentos JSON o audio/video); 3) Complicaciones de integración: unir modelos ER con bases de datos ya existentes puede ser complejo debido a discrepancias arquitectónicas.",
        "explanation": "El DER fue concebido para esquemas altamente estructurados con relaciones discretas; pierde eficacia ante paradigmas NoSQL de grafos o documentos libres.",
        "simple_explanation": "El DER sirve para bases de datos relacionales tradicionales; no sirve para modelar publicaciones de Twitter o archivos multimedia no estructurados.",
        "example": "Modelar comentarios anidados en árbol de una red social con claves foráneas en un DER clásico resulta rígido comparado con una base documental NoSQL.",
        "related_concepts": ["c_reglas_construccion_der", "c_modelos_bd"],
        "common_confusions": "Intentar usar DER para diseñar esquemas NoSQL o arquitecturas de Data Lakes.",
        "difficulty": "medio",
        "source_document": "Diagramas de Entidad Relación y Modelo de Datos.pdf",
        "source_page": "Pág. 15",
        "order_idx": 5
    },
    {
        "id": "c_caso_constructora",
        "topic_id": "u2_t6",
        "name": "Caso Práctico: Empresa Constructora de Edificios",
        "definition": "Ejercicio troncal de modelado de la cátedra que involucra múltiples entidades y relaciones cruzadas: Nómina de Personal asignado a Obras (con Ficha de Actividad que almacena fecha, hora y actividad); Tareas especializadas ejecutadas por Personal; Profesionales externos asignados a Obras (relación 0:N a 1:N); Recursos (mezcladoras, martillos) usados en Obras con Planilla de Uso (fechas y roturas); y Recursos propios vs alquilados a Proveedores mediante Contrato de Alquiler.",
        "explanation": "Demuestra la aplicación de relaciones muchos a muchos (N:M) con atributos propios en la relación (ej. Ficha de Actividad, Planilla de Uso).",
        "simple_explanation": "Es el caso típico de examen donde tenés personas trabajando en obras, con fichas de actividad y planillas de uso de máquinas alquiladas.",
        "example": "La relación 'Planilla de Uso' conecta 'Obras' con 'Recursos' y contiene los atributos: fecha_uso y sufrio_rotura.",
        "related_concepts": ["c_elementos_der", "c_reglas_construccion_der"],
        "common_confusions": "Colocar la fecha de la ficha de actividad dentro de la entidad Personal en lugar de ubicarla en la relación que los vincula con la Obra.",
        "difficulty": "dificil",
        "source_document": "Diagramas de Entidad Relación y Modelo de Datos.pdf",
        "source_page": "Págs. 19-20",
        "order_idx": 6
    }
]

QUESTIONS = [
    {
        "id": "q_u2_1",
        "topic_id": "u2_t4",
        "concept_id": "c_reglas_construccion_der",
        "type": "true_false",
        "difficulty": "facil",
        "question": "En las reglas formales de construcción de un DER, es perfectamente válido conectar una entidad directamente con otra entidad mediante una línea cuando no se desea especificar el nombre de la relación.",
        "options": [
            {"id": "v", "text": "VERDADERO"},
            {"id": "f", "text": "FALSO"}
        ],
        "correct_answer": "f",
        "explanation": "FALSO. Una de las reglas inviolables del DER establece que una entidad nunca puede estar conectada directamente a otra entidad. Toda conexión debe pasar obligatoriamente a través de un rombo de relación.",
        "hint1": "Regla formal de conectividad.",
        "hint2": "Dos rectángulos jamás pueden conectarse directamente.",
        "source_document": "Diagramas de Entidad Relación y Modelo de Datos.pdf",
        "source_page": "Pág. 17",
        "semantic_hash": "hash_u2_q1"
    },
    {
        "id": "q_u2_2",
        "topic_id": "u2_t3",
        "concept_id": "c_der_vs_mr",
        "type": "multiple_choice",
        "difficulty": "medio",
        "question": "¿Cuál es la principal diferencia conceptual entre el Modelo Entidad-Relación y el Modelo Relacional según la cátedra?",
        "options": [
            {"id": "a", "text": "El Modelo E-R es específico para cada entidad del mundo real, y el Modelo Relacional es específico para cada tabla del sistema."},
            {"id": "b", "text": "El Modelo E-R almacena datos físicamente en disco y el Modelo Relacional solo existe en memoria RAM."},
            {"id": "c", "text": "El Modelo E-R utiliza lenguaje SQL para crearse y el Modelo Relacional no lo admite."},
            {"id": "d", "text": "El Modelo Relacional solo permite relaciones 1:1 mientras que el E-R permite N:M."}
        ],
        "correct_answer": "a",
        "explanation": "La opción A es la cita textual de la diapositiva 10: 'La principal diferencia entre el Modelo E-R y el Modelo Relacional es que el Modelo E-R es específico para cada entidad, y el Modelo Relacional es específico para cada tabla.'",
        "hint1": "Una se enfoca en entidades conceptuales, la otra en tablas estructuradas.",
        "hint2": "Revisá la diapositiva 10 de la presentación.",
        "source_document": "Diagramas de Entidad Relación y Modelo de Datos.pdf",
        "source_page": "Pág. 10",
        "semantic_hash": "hash_u2_q2"
    },
    {
        "id": "q_u2_3",
        "topic_id": "u2_t1",
        "concept_id": "c_niveles_modelado",
        "type": "multiple_choice",
        "difficulty": "medio",
        "question": "¿Cuál de los tres niveles de modelado de datos se caracteriza por definir las entidades transaccionales y operativas de forma TOTALMENTE INDEPENDIENTE de la tecnología de implementación?",
        "options": [
            {"id": "a", "text": "Modelo Lógico"},
            {"id": "b", "text": "Modelo Físico"},
            {"id": "c", "text": "Modelo Conceptual"},
            {"id": "d", "text": "Modelo Externo"}
        ],
        "correct_answer": "a",
        "explanation": "El Modelo Lógico contiene más detalle que el conceptual, define entidades operativas y transaccionales, y es estrictamente independiente de la tecnología física en la que se implementará.",
        "hint1": "Está en el medio entre el conceptual y el físico.",
        "hint2": "Independiente de la tecnología de bases de datos.",
        "source_document": "Diagramas de Entidad Relación y Modelo de Datos.pdf",
        "source_page": "Pág. 7",
        "semantic_hash": "hash_u2_q3"
    },
    {
        "id": "q_u2_4",
        "topic_id": "u2_t4",
        "concept_id": "c_reglas_construccion_der",
        "type": "multiple_choice",
        "difficulty": "medio",
        "question": "¿Qué debe hacerse según las reglas de diseño del DER si se detecta una entidad que únicamente posee su atributo identificador y ningún otro atributo descriptivo?",
        "options": [
            {"id": "a", "text": "Eliminarla e incluir la información en otra entidad relacionada."},
            {"id": "b", "text": "Convertirla obligatoriamente en una entidad débil con doble rectángulo."},
            {"id": "c", "text": "Asignarle atributos artificiales para justificar su permanencia."},
            {"id": "d", "text": "Crearle una relación recursiva consigo misma."}
        ],
        "correct_answer": "a",
        "explanation": "La regla 7 de construcción del DER (Pág. 17) establece: 'Si una entidad solo tiene su identificador como atributo, eliminarla e incluir la información en otra entidad.'",
        "hint1": "Una entidad sin atributos no justifica una tabla separada.",
        "hint2": "Se elimina y se absorbe.",
        "source_document": "Diagramas de Entidad Relación y Modelo de Datos.pdf",
        "source_page": "Pág. 17",
        "semantic_hash": "hash_u2_q4"
    }
]
