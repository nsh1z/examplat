"""
Unit 1 Data: Fundamentos de la Ingeniería de Datos y SGBD
Source PDFs:
- Clase I - Ingeniería de Datos 1.pdf
- Material_de_Estudio_Ingenieria_de_Datos_I.pdf (Unidad 1)
"""

TOPICS = [
    {
        "id": "u1_t1",
        "unit_number": 1,
        "name": "Dato vs. Información y Procesamiento",
        "description": "Distinción epistemológica entre dato e información, y etapas del ciclo de procesamiento.",
        "icon": "Database",
        "order_idx": 1
    },
    {
        "id": "u1_t2",
        "unit_number": 1,
        "name": "Evolución de Sistemas de Archivos y Fórmulas de Acceso",
        "description": "Sistemas secuenciales, de acceso directo (hashing) e indexados con sus modelos matemáticos de latencia.",
        "icon": "HardDrive",
        "order_idx": 2
    },
    {
        "id": "u1_t3",
        "unit_number": 1,
        "name": "Ficheros Tradicionales vs. Bases de Datos",
        "description": "Problemas de redundancia, inconsistencia, aislamiento y la solución mediante SGBD.",
        "icon": "Layers",
        "order_idx": 3
    },
    {
        "id": "u1_t4",
        "unit_number": 1,
        "name": "Transacciones ACID",
        "description": "Atomicidad, Consistencia, Aislamiento (Isolation) y Durabilidad en entornos de misión crítica.",
        "icon": "ShieldCheck",
        "order_idx": 4
    },
    {
        "id": "u1_t5",
        "unit_number": 1,
        "name": "Arquitectura ANSI/SPARC e Independencia de Datos",
        "description": "Los 3 niveles (Externo, Conceptual, Interno) e independencias física y lógica.",
        "icon": "Columns",
        "order_idx": 5
    },
    {
        "id": "u1_t6",
        "unit_number": 1,
        "name": "El Ciclo de 14 Pasos de una Consulta",
        "description": "Mecanismo interno paso a paso de ejecución de una consulta en arquitectura cliente/servidor.",
        "icon": "RefreshCw",
        "order_idx": 6
    },
    {
        "id": "u1_t7",
        "unit_number": 1,
        "name": "Modelos de Bases de Datos",
        "description": "Jerárquico, En Red, Relacional, Orientado a Objetos, Objeto-Relacional y NoSQL.",
        "icon": "GitFork",
        "order_idx": 7
    },
    {
        "id": "u1_t8",
        "unit_number": 1,
        "name": "Roles de Usuarios: DBA vs. Administrador de Datos",
        "description": "Usuarios finales, programadores, y delimitación precisa entre DBA (técnico) y DA (directivo).",
        "icon": "Users",
        "order_idx": 8
    }
]

CONCEPTS = [
    {
        "id": "c_dato_info",
        "topic_id": "u1_t1",
        "name": "Dato vs. Información",
        "definition": "Un dato es una representación simbólica atómica y objetiva de un hecho o entidad desprovista de contexto intrínseco. La información es un conjunto de datos estructurados, procesados y contextualizados que reduce la incertidumbre y posee valor para la toma de decisiones.",
        "explanation": "El dato es la materia prima abstracta; la información es el producto final procesado y dotado de sentido semántico.",
        "simple_explanation": "El dato es '25'. La información es 'Juan tiene 25 años y aprobó el examen con 10'.",
        "example": "Datos aislados: '25', 'Buenos Aires', '08:30'. Información: 'Juan Pérez, residente de Buenos Aires y de 25 años, ingresó a la empresa a las 08:30.'",
        "related_concepts": ["c_ciclo_procesamiento", "c_sgbd_def"],
        "common_confusions": "Usar 'dato' e 'información' como sinónimos. Un dato sin contexto no comunica nada.",
        "difficulty": "facil",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 4-6",
        "order_idx": 1
    },
    {
        "id": "c_ciclo_procesamiento",
        "topic_id": "u1_t1",
        "name": "Ciclo de Procesamiento de la Información",
        "definition": "Cadena de cuatro fases sucesivas que transforman datos crudos en conocimiento accionable: 1) Recolección/Entrada, 2) Limpieza/Calidad, 3) Almacenamiento/Estructuración y 4) Análisis/Consumo.",
        "explanation": "Cada fase asegura la integridad, fiabilidad y disponibilidad de la información para el negocio.",
        "simple_explanation": "Ingresa el dato, se limpia de errores, se guarda ordenado en tablas y finalmente se usa en reportes.",
        "example": "Sensores de telemetría envían coordenadas (Entrada), se descartan lecturas erróneas (Limpieza), se guardan en SQL Server (Almacenamiento), y un tablero de PowerBI muestra rutas óptimas (Consumo).",
        "related_concepts": ["c_dato_info", "c_archivos_trad"],
        "common_confusions": "Creer que el almacenamiento ocurre antes de la depuración o validación.",
        "difficulty": "medio",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Pág. 7",
        "order_idx": 2
    },
    {
        "id": "c_arch_secuencial",
        "topic_id": "u1_t2",
        "name": "Archivo Secuencial y Tiempo Medio de Acceso",
        "definition": "Organización física de archivos donde los registros se graban cronológicamente contiguos. Para acceder al registro k, es obligatorio recorrer secuencialmente los k-1 registros previos. El tiempo medio de acceso teórico es t_medio = (t_a * N) / 2.",
        "explanation": "Es altamente eficiente para barridos masivos por lotes (batch), pero inviable para consultas puntuales o transacciones concurrentes.",
        "simple_explanation": "Funciona como una cinta de casete: para escuchar la canción 5 hay que adelantar todas las anteriores.",
        "example": "Con N=1.000.000 registros y t_a=10 ms, t_medio = (10 ms * 1.000.000)/2 = 5.000 segundos (~1,38 horas) para leer un registro.",
        "related_concepts": ["c_arch_directo", "c_arch_indexado"],
        "common_confusions": "Confundir el tiempo medio (la mitad de N) con el peor caso (recorrer N completo).",
        "difficulty": "medio",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 9-11",
        "order_idx": 3
    },
    {
        "id": "c_arch_directo",
        "topic_id": "u1_t2",
        "name": "Acceso Directo (Aleatorio / Hashing)",
        "definition": "Estructura donde la dirección física del registro se calcula matemáticamente aplicando una función de dispersión (hash) sobre el valor de la clave. Tiempo medio: t_medio = t_calculo + t_a.",
        "explanation": "Permite lecturas y escrituras puntuales en tiempo casi constante, independiente del número total de registros N.",
        "simple_explanation": "Sabés exactamente en qué casillero está guardado gracias a una fórmula matemática inmediata.",
        "example": "Con t_calculo=0,5 ms y t_a=10 ms, el acceso tarda 10,5 ms tanto para 100 como para 10.000.000 de registros.",
        "related_concepts": ["c_arch_secuencial", "c_arch_indexado"],
        "common_confusions": "Creer que el acceso directo es eficiente para recorrer rangos ordenados (requiere reordenar o múltiples colisiones).",
        "difficulty": "medio",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 10-12",
        "order_idx": 4
    },
    {
        "id": "c_arch_indexado",
        "topic_id": "u1_t2",
        "name": "Archivos Indexados",
        "definition": "Estructura híbrida que asocia al archivo principal una tabla o árbol auxiliar ordenado (índice) con pares (clave, puntero a bloque). Tiempo medio: t_medio = t_busqueda + t_calculo + t_a.",
        "explanation": "Combina la velocidad de acceso puntual del índice con la capacidad de realizar barridos ordenados eficientes.",
        "simple_explanation": "Como el índice de un libro al final: buscás el tema y vas directo a la página exacta.",
        "example": "Índice B-Tree en SQL Server sobre la columna DNI.",
        "related_concepts": ["c_arch_directo", "c_arch_secuencial"],
        "common_confusions": "Olvidar el costo de mantenimiento: cada INSERT o DELETE obliga a actualizar el índice en disco.",
        "difficulty": "medio",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Pág. 12",
        "order_idx": 5
    },
    {
        "id": "c_ficheros_vs_bd",
        "topic_id": "u1_t3",
        "name": "Ficheros Tradicionales vs. Bases de Datos",
        "definition": "En ficheros tradicionales cada aplicación gestiona sus propios archivos aislados, produciendo redundancia descontrolada, inconsistencia y alto acoplamiento. Un SGBD centraliza los datos, controlando la redundancia y garantizando integridad y concurrencia multiusuario.",
        "explanation": "La base de datos desacopla los programas de la representación física de los datos mediante esquemas formales.",
        "simple_explanation": "Antes cada área tenía su propio archivo Excel desactualizado; con una BD todos acceden a una única fuente de verdad compartida.",
        "example": "El departamento de Ventas y el de Cobranzas acceden a la misma tabla CLIENTES en lugar de mantener dos planillas desfasadas.",
        "related_concepts": ["c_sgbd_def", "c_independencia_datos"],
        "common_confusions": "Creer que en una BD nunca hay redundancia: la redundancia no se elimina a cero, se *controla rigurosamente* (claves foráneas).",
        "difficulty": "medio",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 13-16",
        "order_idx": 6
    },
    {
        "id": "c_sgbd_def",
        "topic_id": "u1_t3",
        "name": "Concepto y Objetivos del SGBD (DBMS)",
        "definition": "Un Sistema Gestor de Bases de Datos es un software de sistema complejo que actúa como intermediario entre los usuarios/aplicaciones y los datos físicos almacenados, proporcionando lenguajes de definición (DDL) y manipulación (DML), seguridad, integridad y control de transacciones.",
        "explanation": "Sus objetivos fundamentales son: independencia de datos, integridad referencial, concurrencia sin anomalías, seguridad ante fallos y optimización de consultas.",
        "simple_explanation": "Es el motor inteligente (como SQL Server u Oracle) que cuida, organiza y busca los datos de forma segura.",
        "example": "Microsoft SQL Server ejecutando transacciones concurrentes con aislamiento.",
        "related_concepts": ["c_acid", "c_ansi_sparc"],
        "common_confusions": "Confundir la Base de Datos (los datos almacenados) con el SGBD (el software que los administra).",
        "difficulty": "facil",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 17-19",
        "order_idx": 7
    },
    {
        "id": "c_acid",
        "topic_id": "u1_t4",
        "name": "Transacciones y Propiedades ACID",
        "definition": "Una transacción es una unidad lógica de ejecución indivisible. El SGBD garantiza cuatro propiedades inviolables: Atomicidad (todo o nada), Consistencia (preservación de invariantes y reglas), Aislamiento (operaciones invisibles entre sí antes del commit) y Durabilidad (persistencia tras confirmación).",
        "explanation": "Si ocurre una falla antes del COMMIT, el motor ejecuta un ROLLBACK automático restaurando el estado original.",
        "simple_explanation": "Atomicidad: Ocurre todo o no ocurre nada. Consistencia: No rompe ninguna regla. Aislamiento: Nadie ve cambios a medias. Durabilidad: No se borra si se corta la luz.",
        "example": "Transferencia de $10.000 de Cuenta A a Cuenta B: restar de A y sumar a B. Si se corta la luz a mitad de camino, se revierte todo.",
        "related_concepts": ["c_sgbd_def", "c_archivos_fisicos_sql"],
        "common_confusions": "Confundir Consistencia (no violar reglas de integridad) con Aislamiento (manejo de concurrencia de accesos simultáneos).",
        "difficulty": "dificil",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 20-22",
        "order_idx": 8
    },
    {
        "id": "c_ansi_sparc",
        "topic_id": "u1_t5",
        "name": "Arquitectura ANSI/SPARC (3 Niveles)",
        "definition": "Estándar arquitectónico que divide un SGBD en tres niveles de abstracción: 1) Nivel Externo (vistas de usuario y aplicaciones), 2) Nivel Conceptual (esquema lógico global independiente del almacenamiento) y 3) Nivel Interno (esquema físico de bloques, punteros e índices).",
        "explanation": "Permite desacoplar el diseño lógico del negocio de los detalles de implementación física en hardware.",
        "simple_explanation": "Nivel Externo: lo que ve cada usuario. Conceptual: el mapa de todas las tablas y relaciones. Interno: cómo se guardan los bytes en el disco.",
        "example": "Un cajero sólo ve la vista de Saldos (Externo); la tabla global tiene 40 campos (Conceptual); en disco se usa un índice B-Tree particionado (Interno).",
        "related_concepts": ["c_independencia_datos", "c_14_pasos"],
        "common_confusions": "Creer que hay una base de datos distinta por cada usuario; hay una sola BD conceptual con múltiples vistas externas.",
        "difficulty": "dificil",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 23-24",
        "order_idx": 9
    },
    {
        "id": "c_independencia_datos",
        "topic_id": "u1_t5",
        "name": "Independencia de Datos: Física y Lógica",
        "definition": "Independencia Física: Capacidad de alterar el esquema interno (índices, discos, compresión) sin modificar el esquema conceptual ni las aplicaciones. Independencia Lógica: Capacidad de alterar el esquema conceptual (añadir tablas, columnas) sin quebrar las vistas externas existentes.",
        "explanation": "Es la mayor ventaja económica de un SGBD frente a los sistemas de archivos tradicionales.",
        "simple_explanation": "Física: Cambiás el disco rígido o agregás un índice y el sistema sigue andando igual. Lógica: Agregás una columna nueva en la tabla y los reportes viejos siguen funcionando.",
        "example": "Física: Migrar una tabla a un disco SSD. Lógica: Añadir la columna 'email_secundario' en Clientes sin reprogramar el módulo de facturación.",
        "related_concepts": ["c_ansi_sparc", "c_ficheros_vs_bd"],
        "common_confusions": "Invertir la definición: pensar que la física refiere a cambios de columnas y la lógica a cambios de disco.",
        "difficulty": "medio",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 24-25",
        "order_idx": 10
    },
    {
        "id": "c_14_pasos",
        "topic_id": "u1_t6",
        "name": "Ciclo de 14 Pasos de Ejecución de una Consulta",
        "definition": "Secuencia determinista que describe el procesamiento cliente/servidor: 1) Solicitud del usuario, 2) Paso al SGBD, 3) Consulta al diccionario, 4) Traducción conceptual/física, 5) Solicitud al SO, 6) Búsqueda en almacenamiento, 7) Copia a buffer del SO, 8) Transferencia al SGBD, 9) Extracción de registros, 10) Retorno al área de trabajo, 11) Notificación de estado, 12) Envío de datos al usuario, 13) Formateo y 14) Visualización final.",
        "explanation": "Muestra la interacción coordinada entre la interfaz de usuario, el SGBD, el Sistema Operativo y los buffers de memoria.",
        "simple_explanation": "El usuario pide datos, el SGBD consulta el diccionario, le pide los bloques al SO, el SO lee el disco, el SGBD filtra y devuelve el resultado.",
        "example": "Ejecutar `SELECT nombre FROM Alumnos WHERE id=5;` recorriendo desde la red hasta el disco y de regreso a la pantalla.",
        "related_concepts": ["c_ansi_sparc", "c_sgbd_def"],
        "common_confusions": "Creer que el SGBD accede directamente al disco físico sin pasar por los controladores y llamadas al Sistema Operativo.",
        "difficulty": "experto",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 26-28",
        "order_idx": 11
    },
    {
        "id": "c_modelos_bd",
        "topic_id": "u1_t7",
        "name": "Evolución de Modelos de Bases de Datos",
        "definition": "Taxonomía histórica: Jerárquico (árbol padre-hijo, sin N:M directo), En Red (grafos CODASYL, punteros directos), Relacional (tablas y tuplas con fundamento en lógica de predicados), Orientado a Objetos (persistencia de clases y métodos), Objeto-Relacional (híbrido SQL:1999) y NoSQL (documental, clave-valor, columnas, grafos).",
        "explanation": "Cada modelo surgió para resolver limitaciones del paradigma previo, siendo el relacional el estándar dominante en la industria transaccional.",
        "simple_explanation": "Pasamos de árboles rígidos a tablas matemáticas con SQL, y luego a modelos no relacionales para Big Data.",
        "example": "IMS (Jerárquico) -> IDMS (Red) -> PostgreSQL / SQL Server (Relacional / Objeto-Relacional) -> MongoDB / Cassandra (NoSQL).",
        "related_concepts": ["c_sgbd_def", "c_codd_reglas"],
        "common_confusions": "Creer que NoSQL reemplazó por completo al modelo relacional; coexisten según requerimientos de ACID vs escalabilidad horizontal.",
        "difficulty": "medio",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 29-37",
        "order_idx": 12
    },
    {
        "id": "c_roles_dba_da",
        "topic_id": "u1_t8",
        "name": "Roles de Usuarios: DBA vs. Administrador de Datos (DA)",
        "definition": "El Administrador de Base de Datos (DBA) es el responsable técnico y operativo (diseño físico, rendimiento, backups, permisos y tuning). El Administrador de Datos (DA) es el responsable directivo y estratégico de la información (políticas de gobernanza, ciclo de vida del dato, calidad y valor para el negocio).",
        "explanation": "El DA define *qué* información necesita la organización y sus políticas; el DBA implementa y mantiene *cómo* se almacena y resguarda físicamente.",
        "simple_explanation": "El DA es el gerente de políticas de datos; el DBA es el ingeniero técnico que cuida los servidores y la velocidad.",
        "example": "El DA decide que los datos de clientes deben conservarse por 10 años por regulación legal. El DBA configura el particionamiento de tablas y las cintas de backup para cumplirlo.",
        "related_concepts": ["c_sgbd_def", "c_ficheros_vs_bd"],
        "common_confusions": "Asumir que el DBA y el DA son el mismo rol con nombres distintos.",
        "difficulty": "facil",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 38-42",
        "order_idx": 13
    }
]

QUESTIONS = [
    {
        "id": "q1_1",
        "topic_id": "u1_t1",
        "concept_id": "c_dato_info",
        "type": "multiple_choice",
        "difficulty": "facil",
        "question": "¿Cuál es la diferencia epistemológica y funcional entre 'dato' e 'información'?",
        "options": [
            {"id": "a", "text": "Un dato es una representación simbólica aislada sin contexto; la información es el conjunto de datos estructurados y procesados que reduce la incertidumbre."},
            {"id": "b", "text": "Los datos son exclusivamente números y la información está conformada exclusivamente por cadenas de texto."},
            {"id": "c", "text": "La información es la materia prima que se recolecta directamente de los sensores, mientras que los datos son el producto analizado."},
            {"id": "d", "text": "No existe diferencia en la ingeniería de datos; ambos términos son formalmente intercambiables."}
        ],
        "correct_answer": "a",
        "explanation": "La opción A es correcta. Por definición académica, el dato es un hecho atómico desprovisto de significado propio. Al asignarle semántica y contexto estructurado, se transforma en información útil para la toma de decisiones.",
        "hint1": "Pensá en qué necesitas agregarle a un número suelto para que le sirva a una persona para decidir.",
        "hint2": "El dato es la materia prima; la información es el producto elaborado.",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 4-6",
        "semantic_hash": "hash_q1_1_dato_info"
    },
    {
        "id": "q1_2",
        "topic_id": "u1_t2",
        "concept_id": "c_arch_secuencial",
        "type": "multiple_choice",
        "difficulty": "medio",
        "question": "En un sistema de archivos secuencial con N = 2.000.000 de registros contiguos y un tiempo de acceso a bloque ta = 5 ms, ¿cuál es el tiempo medio teórico de acceso para localizar un registro arbitrario?",
        "options": [
            {"id": "a", "text": "5.000 segundos (~1,38 horas)"},
            {"id": "b", "text": "10.000 segundos (~2,77 horas)"},
            {"id": "c", "text": "5 milisegundos"},
            {"id": "d", "text": "2.500 segundos (~41,6 minutos)"}
        ],
        "correct_answer": "a",
        "explanation": "La fórmula de acceso secuencial es t_medio = (ta * N) / 2. Reemplazando: (5 ms * 2.000.000) / 2 = 5.000.000 ms = 5.000 segundos (~1,38 horas).",
        "hint1": "Recordá que en promedio se recorre la mitad de los registros del archivo.",
        "hint2": "Multiplicá ta por N y dividilo por 2, luego convertí milisegundos a segundos.",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 9-11",
        "semantic_hash": "hash_q1_2_calculo_secuencial"
    },
    {
        "id": "q1_3",
        "topic_id": "u1_t2",
        "concept_id": "c_arch_directo",
        "type": "true_false",
        "difficulty": "medio",
        "question": "En un sistema de archivos de acceso directo mediante función de dispersión (hashing), el tiempo medio de acceso se incrementa proporcionalmente de forma lineal a medida que crece el número de registros N.",
        "options": [
            {"id": "v", "text": "VERDADERO"},
            {"id": "f", "text": "FALSO"}
        ],
        "correct_answer": "f",
        "explanation": "FALSO. El tiempo medio en acceso directo es t_medio = t_calculo + ta. La función de dispersión calcula la posición de almacenamiento de forma inmediata e independiente de N (tiempo prácticamente constante O(1)), salvo el costo menor de resolución de colisiones.",
        "hint1": "Analizá si la fórmula t_medio = t_calculo + ta contiene la variable N.",
        "hint2": "En hashing no se recorre el archivo; se aplica una fórmula matemática a la clave.",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 10-12",
        "semantic_hash": "hash_q1_3_hashing_independencia_n"
    },
    {
        "id": "q1_4",
        "topic_id": "u1_t4",
        "concept_id": "c_acid",
        "type": "matching",
        "difficulty": "dificil",
        "question": "Relacione cada propiedad del estándar transaccional ACID con su principio operativo fundamental:",
        "options": [
            {"left": "Atomicidad (A)", "right": "Principio de 'todo o nada'; si falla un paso, se revierten todos los cambios."},
            {"left": "Consistencia (C)", "right": "La transacción transforma la BD de un estado válido a otro, preservando invariantes."},
            {"left": "Aislamiento (I)", "right": "Las transacciones concurrentes operan de modo independiente sin ver estados intermedios."},
            {"left": "Durabilidad (D)", "right": "Una vez confirmada (COMMIT), los cambios persisten ante caídas del servidor o energía."}
        ],
        "correct_answer": "{\"Atomicidad (A)\": \"Principio de 'todo o nada'; si falla un paso, se revierten todos los cambios.\", \"Consistencia (C)\": \"La transacción transforma la BD de un estado válido a otro, preservando invariantes.\", \"Aislamiento (I)\": \"Las transacciones concurrentes operan de modo independiente sin ver estados intermedios.\", \"Durabilidad (D)\": \"Una vez confirmada (COMMIT), los cambios persisten ante caídas del servidor o energía.\"}",
        "explanation": "Atomicidad evita estados a medio camino; Consistencia asegura integridad lógica; Aislamiento controla la concurrencia simultánea; y Durabilidad garantiza persistencia física.",
        "hint1": "Asociá 'Atomicidad' con 'indivisible' y 'Durabilidad' con 'sobrevivir a cortes de luz'.",
        "hint2": "'Aislamiento' se relaciona con la concurrencia entre múltiples usuarios.",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 20-22",
        "semantic_hash": "hash_q1_4_match_acid"
    },
    {
        "id": "q1_5",
        "topic_id": "u1_t5",
        "concept_id": "c_independencia_datos",
        "type": "fill_blank",
        "difficulty": "medio",
        "question": "La capacidad de modificar la estructura física de almacenamiento de una base de datos (por ejemplo, agregar índices o cambiar de disco rígido a SSD) sin alterar el esquema conceptual ni las aplicaciones de usuario se denomina Independencia ________ de datos.",
        "options": [],
        "correct_answer": "Física",
        "explanation": "Se trata de la 'Independencia Física'. La 'Independencia Lógica', en cambio, refiere a la capacidad de añadir tablas o columnas en el esquema conceptual sin romper las vistas externas.",
        "hint1": "Refiere al nivel más bajo de la arquitectura ANSI/SPARC.",
        "hint2": "Se opone a la independencia 'Lógica'.",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 24-25",
        "semantic_hash": "hash_q1_5_fill_independencia_fisica"
    },
    {
        "id": "q1_6",
        "topic_id": "u1_t6",
        "concept_id": "c_14_pasos",
        "type": "order_steps",
        "difficulty": "experto",
        "question": "Ordene cronológicamente las siguientes etapas clave del ciclo de 14 pasos de ejecución de una consulta en arquitectura cliente/servidor:",
        "options": [
            {"id": "step1", "text": "El usuario o aplicación emite la solicitud de consulta hacia el subsistema gestor."},
            {"id": "step2", "text": "El SGBD intercepta la consulta y verifica las definiciones en el Diccionario de Datos."},
            {"id": "step3", "text": "El SGBD traduce la consulta conceptual a especificaciones físicas y solicita I/O al Sistema Operativo."},
            {"id": "step4", "text": "El Sistema Operativo accede al medio físico de almacenamiento y copia los bloques crudos a sus buffers."},
            {"id": "step5", "text": "El SGBD extrae los registros solicitados, formatea la estructura resultante y la entrega al área de trabajo del usuario."}
        ],
        "correct_answer": "[\"step1\", \"step2\", \"step3\", \"step4\", \"step5\"]",
        "explanation": "El flujo canónico va desde la interfaz de usuario -> SGBD -> Diccionario de datos -> Solicitud al SO -> Lectura de disco -> Buffers del SO -> Filtro del SGBD -> Entrega a la aplicación.",
        "hint1": "Primero se consulta el catálogo/diccionario antes de pedir datos al sistema operativo.",
        "hint2": "El Sistema Operativo es quien realmente dialoga con el hardware de disco.",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 26-28",
        "semantic_hash": "hash_q1_6_order_14_pasos"
    },
    {
        "id": "q1_7",
        "topic_id": "u1_t8",
        "concept_id": "c_roles_dba_da",
        "type": "open_question",
        "difficulty": "dificil",
        "question": "Distinga con precisión técnica las responsabilidades del Administrador de Datos (DA) frente a las del Administrador de Base de Datos (DBA). Dé un ejemplo de decisión estratégica correspondiente a cada rol.",
        "options": [],
        "correct_answer": "El Administrador de Datos (DA) opera a nivel directivo y estratégico, definiendo la gobernanza de la información, el valor del dato para el negocio, el ciclo de vida y las políticas de retención legal (ejemplo: establecer que los datos clínicos de pacientes deben conservarse 10 años). El DBA opera a nivel técnico y físico, administrando los servidores, la configuración del motor, planes de mantenimiento, índices B-Tree, backups y afinamiento de rendimiento (ejemplo: configurar particionamiento de tablas y compresión en disco SSD para soportar la retención de 10 años sin degradar las consultas).",
        "explanation": "Criterio de corrección: El alumno debe evidenciar que el DA es estratégico/negocio ('qué datos') y el DBA es operativo/técnico ('cómo implementarlo en software/hardware').",
        "hint1": "Pensá en quién define las políticas de la empresa y quién escribe scripts de configuración del servidor.",
        "hint2": "DA = Gobernanza y negocio; DBA = Rendimiento, backups, tuning y seguridad física.",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 38-42",
        "semantic_hash": "hash_q1_7_open_dba_vs_da"
    },
    {
        "id": "q1_8",
        "topic_id": "u1_t4",
        "concept_id": "c_acid",
        "type": "practical_case",
        "difficulty": "dificil",
        "question": "CASO PRÁCTICO — Falla en Cajeros Automáticos:\nDos clientes en cajeros distintos intentan extraer simultáneamente dinero de una cuenta compartida que tiene un saldo disponible de $10.000. Ambos cajeros leen el saldo disponible de $10.000 exactamente al mismo milisegundo y autorizan un retiro de $8.000 cada uno. Al finalizar, se entregaron $16.000 en efectivo y la cuenta quedó en un descubierto no autorizado.\n¿Qué propiedad del estándar ACID falló en este sistema y qué mecanismo debió haber implementado el SGBD para evitarlo?",
        "options": [
            {"id": "a", "text": "Falló el Aislamiento (Isolation - I); el SGBD debió aplicar bloqueos de concurrencia (locks) para que la segunda transacción espere la confirmación de la primera."},
            {"id": "b", "text": "Falló la Durabilidad (D); el SGBD debió guardar los cambios en un archivo de log antes de entregar el dinero."},
            {"id": "c", "text": "Falló la Atomicidad (A); debió haberse entregado la mitad del dinero a cada cajero."},
            {"id": "d", "text": "No falló ninguna propiedad ACID; se trata de una falla exclusiva del hardware del cajero automático."}
        ],
        "correct_answer": "a",
        "explanation": "La opción A es correcta. Se produjo una anomalía de concurrencia clásica (actualización perdida / lectura no aislada) que viola el Aislamiento. El SGBD debió bloquear el registro de la cuenta durante la lectura de la primera transacción para impedir lecturas sucias concurrentes.",
        "hint1": "La falla ocurrió por dos operaciones ejecutándose 'al mismo milisegundo'.",
        "hint2": "El problema es la falta de aislamiento entre sesiones paralelas.",
        "source_document": "Clase I - Ingeniería de Datos 1.pdf",
        "source_page": "Págs. 20-22",
        "semantic_hash": "hash_q1_8_caso_acid_concurrencia"
    }
]
