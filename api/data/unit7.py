"""
Unit 7 Data: Lenguaje SQL — Manipulación, Consultas y Transacciones (DML, TCL)
Source PDFs:
- Clase V Introduccion a SQL.pdf (Págs. 29-51)
- Clase nro VI.pdf (Págs. 1-35)
- Material_de_Estudio_Ingenieria_de_Datos_I.pdf (Unidad 7)
"""

TOPICS = [
    {
        "id": "u7_t1",
        "unit_number": 7,
        "name": "Modificación de Datos: INSERT, UPDATE y DELETE",
        "description": "Inserción de filas individuales y por subconsulta, actualizaciones condicionadas y borrado físico.",
        "icon": "Database",
        "order_idx": 39
    },
    {
        "id": "u7_t2",
        "unit_number": 7,
        "name": "Anatomía y Orden de Ejecución Lógica del SELECT",
        "description": "El pipeline de 7 fases del motor: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY.",
        "icon": "Cpu",
        "order_idx": 40
    },
    {
        "id": "u7_t3",
        "unit_number": 7,
        "name": "Filtros de Selección y Operadores Avanzados",
        "description": "Comodines de texto LIKE (% y _), membresía IN, rangos BETWEEN y evaluación de nulos con IS NULL.",
        "icon": "Filter",
        "order_idx": 41
    },
    {
        "id": "u7_t4",
        "unit_number": 7,
        "name": "Agregaciones, GROUP BY y Filtros HAVING vs. WHERE",
        "description": "COUNT, SUM, AVG, MIN, MAX. Regla de oro de columnas en el SELECT y filtrado de grupos consolidados.",
        "icon": "PieChart",
        "order_idx": 42
    },
    {
        "id": "u7_t5",
        "unit_number": 7,
        "name": "Catálogo Exhaustivo de Juntas (JOINs) y Casos AdventureWorks",
        "description": "INNER, LEFT, RIGHT, FULL OUTER, CROSS JOIN (producto cartesiano) y SELF JOIN reflexivo.",
        "icon": "GitPullRequest",
        "order_idx": 43
    },
    {
        "id": "u7_t6",
        "unit_number": 7,
        "name": "Transacciones (TCL) y Arquitectura Física (.mdf, .ndf, .ldf)",
        "description": "BEGIN TRAN, COMMIT, ROLLBACK. Mecanismo Write-Ahead Logging (WAL) y tipos de archivos de SQL Server.",
        "icon": "Save",
        "order_idx": 44
    }
]

CONCEPTS = [
    {
        "id": "c_orden_logico_sql",
        "topic_id": "u7_t2",
        "name": "Orden Cronológico de Procesamiento Lógico del SELECT",
        "definition": "A diferencia de cómo se escribe en el código, el motor relacional procesa la consulta en un orden cronológico estricto de 7 etapas: 1) FROM & JOINs (identifica y junta las tablas), 2) WHERE (filtra filas individuales), 3) GROUP BY (colapsa en grupos), 4) HAVING (filtra grupos consolidados), 5) SELECT (proyecta y evalúa expresiones y alias), 6) DISTINCT (elimina duplicados) y 7) ORDER BY (ordena el resultado final para visualización).",
        "explanation": "Esta es la razón por la cual es estrictamente imposible utilizar en el WHERE un alias creado en el SELECT (el WHERE se procesa en el paso 2, cuando el SELECT del paso 5 todavía no existe en memoria).",
        "simple_explanation": "Aunque escribas SELECT primero, el motor hace: 1° busca las tablas (FROM), 2° filtra las filas (WHERE), 3° agrupa (GROUP BY), 4° filtra los grupos (HAVING), 5° recién ahí corta las columnas (SELECT) y al final ordena (ORDER BY).",
        "example": "`SELECT precio * 1.21 AS precio_iva FROM Productos WHERE precio_iva > 100;` FALLA con error: 'Invalid column name precio_iva' porque el alias nace en el paso 5 y el WHERE se ejecuta en el paso 2.",
        "related_concepts": ["c_having_vs_where", "c_sql_joins"],
        "common_confusions": "Intentar usar alias calculados del SELECT dentro de las cláusulas WHERE o GROUP BY.",
        "difficulty": "dificil",
        "source_document": "Clase nro VI.pdf / Material de Estudio Integral",
        "source_page": "Unidad 7, Pág. 20",
        "order_idx": 47
    },
    {
        "id": "c_having_vs_where",
        "topic_id": "u7_t4",
        "name": "Filtros de Fila vs. Filtros de Grupo: WHERE vs. HAVING",
        "definition": "WHERE filtra registros individuales *antes* de que ocurra la operación de agrupamiento; nunca puede contener funciones de agregación (como `SUM` o `COUNT`). HAVING opera *después* de que las filas han sido colapsadas en grupos por el GROUP BY, evaluando predicados exclusivamente sobre valores agregados o columnas presentes en el agrupamiento.",
        "explanation": "Cualquier condición que dependa de una función agregada (ej. `COUNT(*) > 5`) debe ubicarse obligatoriamente en el HAVING.",
        "simple_explanation": "WHERE filtra renglón por renglón antes de juntar. HAVING filtra los grupos ya armados (ej. 'sucursales con más de 10 empleados').",
        "example": "`SELECT id_depto, COUNT(*) FROM Empleados WHERE sueldo > 50000 GROUP BY id_depto HAVING COUNT(*) >= 5;` (Filtra empleados bien pagos en el WHERE y luego conserva solo los departamentos con al menos 5 de ellos en el HAVING).",
        "related_concepts": ["c_orden_logico_sql", "c_agregaciones_sql"],
        "common_confusions": "Escribir `WHERE COUNT(*) > 1`: genera un error de sintaxis inmediato en cualquier motor SQL.",
        "difficulty": "medio",
        "source_document": "Clase nro VI.pdf",
        "source_page": "Págs. 6-12",
        "order_idx": 48
    },
    {
        "id": "c_sql_joins",
        "topic_id": "u7_t5",
        "name": "Catálogo de Juntas: INNER, LEFT, RIGHT, FULL, CROSS y SELF JOIN",
        "definition": "1) INNER JOIN: Retorna solo las tuplas que satisfacen la condición en ambas tablas. 2) LEFT OUTER JOIN: Retorna todas las tuplas de la tabla izquierda; si no hay coincidencia a la derecha, completa con NULL. 3) RIGHT OUTER JOIN: Retorna todas las tuplas de la tabla derecha. 4) FULL OUTER JOIN: Retorna todas las tuplas de ambas tablas, rellenando con NULL las discrepancias. 5) CROSS JOIN: Producto cartesiano absoluto (N × M tuplas). 6) SELF JOIN: Junta de una tabla consigo misma usando alias distintos para resolver relaciones recursivas.",
        "explanation": "La combinación `LEFT JOIN ... WHERE tabla_derecha.PK IS NULL` es el patrón canónico para resolver 'detección de no existencia' (ej. clientes sin compras).",
        "simple_explanation": "INNER: solo los que coinciden en ambos lados. LEFT: todos los de la izquierda, aunque no tengan nada a la derecha. CROSS: todos contra todos.",
        "example": "`SELECT c.nombre FROM Clientes c LEFT JOIN Ventas v ON c.id = v.id_cliente WHERE v.id IS NULL;` (retorna clientes que nunca realizaron compras).",
        "related_concepts": ["c_orden_logico_sql", "c_junta_natural"],
        "common_confusions": "Olvidar la condición `ON`: un `JOIN` sin condición `ON` se convierte en un producto cartesiano (`CROSS JOIN`).",
        "difficulty": "medio",
        "source_document": "Clase nro VI.pdf",
        "source_page": "Págs. 14-34",
        "order_idx": 49
    },
    {
        "id": "c_archivos_fisicos_sql",
        "topic_id": "u7_t6",
        "name": "Control de Transacciones (TCL) y Archivos Físicos (.mdf, .ndf, .ldf)",
        "definition": "TCL: Delimita unidades indivisibles con `BEGIN TRANSACTION`, las asienta permanentemente con `COMMIT` o las revierte por completo con `ROLLBACK`. Arquitectura física (SQL Server): 1) `.mdf` (Master Data File): Archivo de datos primario que contiene tablas e índices en páginas de 8 KB. 2) `.ndf` (Secondary Data File): Archivo de datos secundario opcional. 3) `.ldf` (Log Data File): Diario transaccional que registra cronológicamente cada cambio antes de escribirse en el archivo de datos (protocolo Write-Ahead Logging WAL).",
        "explanation": "El archivo de log `.ldf` es el que permite ejecutar un `ROLLBACK` y garantiza la Atomicidad y Durabilidad ante fallos de energía.",
        "simple_explanation": "El archivo .mdf guarda las tablas; el archivo .ldf es la bitácora donde se anota cada cambio antes de aplicarlo para poder deshacerlo si se corta la luz.",
        "example": "Si un analista ejecuta `UPDATE Clientes SET saldo=0;` sin WHERE dentro de una transacción explícita, puede ejecutar inmediatamente `ROLLBACK;` y recuperar los datos gracias al `.ldf`.",
        "related_concepts": ["c_acid", "c_ddl_create_truncate"],
        "common_confusions": "Creer que si se borra el archivo `.ldf` no pasa nada: sin el archivo de log la base de datos entra en estado de sospecha ('Suspect') y no puede arrancar.",
        "difficulty": "dificil",
        "source_document": "Clase V Introduccion a SQL.pdf",
        "source_page": "Págs. 44-50",
        "order_idx": 50
    }
]

QUESTIONS = [
    {
        "id": "q7_1",
        "topic_id": "u7_t2",
        "concept_id": "c_orden_logico_sql",
        "type": "order_steps",
        "difficulty": "dificil",
        "question": "Ordene de forma cronológica estricta las siguientes 7 fases que realiza el motor de base de datos para procesar lógicamente una consulta SQL `SELECT`:",
        "options": [
            {"id": "s1", "text": "FROM y combinaciones JOIN (identificación del espacio relacional)"},
            {"id": "s2", "text": "WHERE (filtrado de tuplas individuales)"},
            {"id": "s3", "text": "GROUP BY (agrupamiento y colapso de filas)"},
            {"id": "s4", "text": "HAVING (filtrado de grupos consolidados)"},
            {"id": "s5", "text": "SELECT (proyección de columnas y evaluación de expresiones/alias)"},
            {"id": "s6", "text": "DISTINCT (eliminación de tuplas duplicadas)"},
            {"id": "s7", "text": "ORDER BY (ordenamiento final de salida para presentación)"}
        ],
        "correct_answer": "[\"s1\", \"s2\", \"s3\", \"s4\", \"s5\", \"s6\", \"s7\"]",
        "explanation": "El orden de ejecución lógica es: 1. FROM -> 2. WHERE -> 3. GROUP BY -> 4. HAVING -> 5. SELECT -> 6. DISTINCT -> 7. ORDER BY.",
        "hint1": "Pensá qué necesita el motor primero para poder filtrar: necesita saber de qué tabla vienen los datos.",
        "hint2": "El SELECT se evalúa mucho después del WHERE y del HAVING; el ORDER BY es el último de todos.",
        "source_document": "Clase nro VI.pdf",
        "source_page": "Págs. 4-6",
        "semantic_hash": "hash_q7_1_orden_logico_select"
    },
    {
        "id": "q7_2",
        "topic_id": "u7_t4",
        "concept_id": "c_having_vs_where",
        "type": "multiple_choice",
        "difficulty": "medio",
        "question": "Considere la siguiente instrucción SQL:\n`SELECT id_categoria, COUNT(*) AS total FROM Productos WHERE COUNT(*) > 5 GROUP BY id_categoria;`\n¿Qué ocurrirá al intentar ejecutarla en cualquier motor SQL estándar?",
        "options": [
            {"id": "a", "text": "Fallará con un error de compilación de sintaxis, porque las funciones de agregación como `COUNT(*)` no están permitidas dentro de la cláusula `WHERE`; deben filtrarse en la cláusula `HAVING`."},
            {"id": "b", "text": "Se ejecutará con total normalidad devolviendo solo las categorías con más de 5 productos."},
            {"id": "c", "text": "Retornará una tabla vacía porque el alias `total` no coincide con el nombre de la columna en disco."},
            {"id": "d", "text": "El motor reemplazará automáticamente el WHERE por un HAVING sin avisar al usuario."}
        ],
        "correct_answer": "a",
        "explanation": "La opción A es correcta. En el orden lógico de procesamiento, el `WHERE` se evalúa sobre filas individuales ANTES de que los grupos existan; por lo tanto, no conoce el valor de ninguna función agregada. El filtro sobre agregaciones debe escribirse en el `HAVING`: `GROUP BY id_categoria HAVING COUNT(*) > 5;`.",
        "hint1": "¿Se pueden usar funciones como SUM o COUNT en el WHERE?",
        "hint2": "El WHERE filtra antes de agrupar; para filtrar después de agrupar se usa HAVING.",
        "source_document": "Clase nro VI.pdf",
        "source_page": "Págs. 7-11",
        "semantic_hash": "hash_q7_2_error_count_en_where"
    },
    {
        "id": "q7_3",
        "topic_id": "u7_t5",
        "concept_id": "c_sql_joins",
        "type": "multiple_choice",
        "difficulty": "medio",
        "question": "En el caso de un sistema de Ventas, ¿qué técnica SQL estándar permite obtener el listado de clientes que NUNCA han realizado ninguna compra en el sistema?",
        "options": [
            {"id": "a", "text": "Aplicar un `LEFT JOIN` entre Clientes y Ventas en el `FROM`, agregando la condición `WHERE Ventas.id_venta IS NULL`."},
            {"id": "b", "text": "Aplicar un `INNER JOIN` entre Clientes y Ventas con la condición `WHERE Ventas.monto = 0`."},
            {"id": "c", "text": "Hacer un `CROSS JOIN` entre ambas tablas y seleccionar `DISTINCT`."},
            {"id": "d", "text": "Es imposible de resolver en una sola consulta SQL; requiere dos consultas separadas en la aplicación."}
        ],
        "correct_answer": "a",
        "explanation": "La opción A es correcta. El `LEFT JOIN` conserva a todos los clientes; para aquellos que no tienen ventas asociadas, las columnas de la tabla Ventas quedan rellenas con valores `NULL`. El filtro `WHERE Ventas.id_venta IS NULL` descarta a los que sí compraron y conserva exactamente a los no compradores.",
        "hint1": "Buscás una junta externa que conserve a todos los clientes aunque no tengan compras.",
        "hint2": "Si una fila no tiene compra, el ID de la venta viene en NULL.",
        "source_document": "Clase nro VI.pdf",
        "source_page": "Págs. 18-24",
        "semantic_hash": "hash_q7_3_left_join_is_null"
    },
    {
        "id": "q7_4",
        "topic_id": "u7_t6",
        "concept_id": "c_archivos_fisicos_sql",
        "type": "open_question",
        "difficulty": "experto",
        "question": "Explique qué función cumple el archivo `.ldf` (Log Data File) en Microsoft SQL Server y por qué se recomienda ubicarlo físicamente en un disco o controladora separada del archivo `.mdf` (Master Data File).",
        "options": [],
        "correct_answer": "El archivo `.ldf` (Log Data File) es el diario transaccional que registra de forma secuencial, cronológica e inmutable todas las operaciones y modificaciones antes de que se asienten en el archivo de datos (protocolo Write-Ahead Logging WAL). Es indispensable para garantizar la Atomicidad y Durabilidad (ACID), permitiendo revertir transacciones abortadas (ROLLBACK) y recuperar la consistencia ante caídas del servidor. Se recomienda ubicarlo en un disco o controladora física independiente por dos razones críticas: 1) Rendimiento de I/O: El archivo `.ldf` realiza escrituras puramente secuenciales y continuas a alta velocidad, mientras que el `.mdf` sufre lecturas y escrituras aleatorias masivas de páginas de 8 KB; separarlos evita la competencia y el desgaste del cabezal de disco. 2) Tolerancia a fallos: Si el disco que aloja el `.mdf` sufre una rotura física irreversible, disponer del archivo `.ldf` intacto en otro disco permite restaurar el último backup completo y aplicar todas las transacciones hasta el instante exacto del desastre sin pérdida de datos.",
        "explanation": "Criterio de evaluación: Mencionar la función de WAL y rollback del .ldf, la diferencia de patrón de acceso I/O (secuencial vs aleatorio) y la ventaja de recuperación ante fallos de hardware.",
        "hint1": "Pensá en el tipo de acceso al log (secuencial) vs al archivo de datos (aleatorio).",
        "hint2": "Pensá qué pasa si se rompe el disco donde están las tablas: ¿cómo recuperás los cambios del día?",
        "source_document": "Clase V Introduccion a SQL.pdf",
        "source_page": "Págs. 44-50",
        "semantic_hash": "hash_q7_4_open_archivos_mdf_ldf"
    }
]
