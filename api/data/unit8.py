"""
Unit 8 Data: Casos de Estudio y Práctica Integral Resuelta
Source PDFs:
- Ejercicio 1 DDL.pdf / Ejercicio 1 DDL Solucion.pdf (Pubs)
- Ejercicio 1 Para Resolver.pdf / Ejercicio 1 solucion.pdf (Viajes 34 consultas)
- Ejercicio 2 Para Resolver.pdf (Hospitales)
- TP_Ingeniería de Datos.pdf (Ventas 20 consignas)
- Algebra Relacional.pdf (16 consultas)
"""

TOPICS = [
    {
        "id": "u8_t1",
        "unit_number": 8,
        "name": "Caso 1: Cadena de Bares y Locales Nocturnos (DDL y CHECKS)",
        "description": "Modelado DDL, claves primarias compuestas y restricciones CHECK de dominio e integridad.",
        "icon": "Coffee",
        "order_idx": 45
    },
    {
        "id": "u8_t2",
        "unit_number": 8,
        "name": "Caso 2: Sistema de Agencia de Viajes (Jerarquías y 34 Consultas SQL)",
        "description": "Esquema completo con FK recursiva de viajes de conexión y resolución de 34 requerimientos de consulta.",
        "icon": "Plane",
        "order_idx": 46
    },
    {
        "id": "u8_t3",
        "unit_number": 8,
        "name": "Caso 3: Gestión Hospitalaria (DDL, Modificaciones y Vistas)",
        "description": "Hospitales, salas, plantilla médica, enfermos e internaciones. Creación y manipulación de VISTAS.",
        "icon": "Activity",
        "order_idx": 47
    },
    {
        "id": "u8_t4",
        "unit_number": 8,
        "name": "Caso 4: Comercio y Ventas (Trabajo Práctico Oficial de 20 Consignas)",
        "description": "Resolución estructurada del TP de cátedra: filtros, agrupaciones, juntas y detección de clientes inactivos.",
        "icon": "ShoppingCart",
        "order_idx": 48
    }
]

CONCEPTS = [
    {
        "id": "c_caso_pubs_ddl",
        "topic_id": "u8_t1",
        "name": "Modelo de Cadena de Bares (DDL y Restricciones CHECK)",
        "definition": "Caso de estudio de modelado físico con tablas: LOCALIDAD(COD_LOCALIDAD, NOMBRE), PUB(COD_PUB, NOMBRE, LICENCIA_FISCAL, DOMICILIO, FECHA_APERTURA, HORARIO, COD_LOCALIDAD), TITULAR, EMPLEADO, EXISTENCIAS y PUB_EMPLEADO. Destaca por el uso de restricciones CHECK de dominio: `CHECK (HORARIO IN ('HOR1', 'HOR2', 'HOR3'))` y `CHECK (PRECIO > 0)`.",
        "explanation": "Ilustra el uso de restricciones CHECK para forzar reglas de negocio directamente en el motor.",
        "simple_explanation": "El caso práctico de los bares donde aprendés a limitar horarios válidos y precios mayores a cero con CHECK.",
        "example": "`CONSTRAINT CK_PUB_HORARIO CHECK (HORARIO IN ('HOR1', 'HOR2', 'HOR3'))`.",
        "related_concepts": ["c_ddl_constraints", "c_reglas_integridad"],
        "common_confusions": "Olvidar asignar nombres a las restricciones CHECK: si no se nombran, el motor genera nombres crípticos difíciles de mantener.",
        "difficulty": "medio",
        "source_document": "Ejercicio 1 DDL Solucion.pdf",
        "source_page": "Págs. 1-2",
        "order_idx": 51
    },
    {
        "id": "c_caso_viajes_sql",
        "topic_id": "u8_t2",
        "name": "Caso Agencia de Viajes (Clave Foránea Recursiva y 34 Consultas)",
        "definition": "Esquema relacional compuesto por LUGAR(lug_codigo, lug_nombre, lug_tipo), VIAJE(v_codigo, v_fecha, v_cd_pasajero, v_origen, v_destino, v_precio, v_cd_viaje_rec) y PASAJERO(p_codigo, p_nombre). Incorpora una clave foránea recursiva `v_cd_viaje_rec` (viaje de conexión) y sirve de base para ejercitar 34 consultas que van desde selecciones simples hasta subconsultas correlacionadas.",
        "explanation": "La FK recursiva exige self-joins (`VIAJE v1 JOIN VIAJE v2 ON v1.v_cd_viaje_rec = v2.v_codigo`) para vincular un viaje con su tramo de conexión.",
        "simple_explanation": "El ejercicio integral con viajes y pasajeros: incluye vuelos de conexión donde un viaje apunta a otro viaje previo.",
        "example": "`SELECT v1.v_codigo, v2.v_codigo AS viaje_previo FROM VIAJE v1 JOIN VIAJE v2 ON v1.v_cd_viaje_rec = v2.v_codigo;`.",
        "related_concepts": ["c_sql_joins", "c_orden_logico_sql"],
        "common_confusions": "Confundir el origen y destino con tablas separadas: ambos son claves foráneas apuntando a la misma tabla LUGAR.",
        "difficulty": "dificil",
        "source_document": "Ejercicio 1 solucion.pdf",
        "source_page": "Págs. 1-7",
        "order_idx": 52
    },
    {
        "id": "c_caso_hospitales_vistas",
        "topic_id": "u8_t3",
        "name": "Caso Hospitales y Creación de Vistas (CREATE VIEW)",
        "definition": "Esquema compuesto por HOSPITAL, SALA, PLANTILLA, OCUPACION y ENFERMO. Introduce el concepto de VISTA como tabla virtual definida por una consulta SELECT almacenada en el catálogo. Permite simplificar consultas complejas, ocultar datos sensibles a ciertos perfiles y proveer independencia lógica de datos.",
        "explanation": "Una vista no almacena datos físicos replicados; ejecuta dinámicamente la consulta subyacente cada vez que es referenciada.",
        "simple_explanation": "Una vista es una consulta guardada con nombre que se puede consultar como si fuera una tabla normal.",
        "example": "`CREATE VIEW Vista_Medicos AS SELECT empleado_no, apellido, especialidad FROM PLANTILLA WHERE funcion = 'MEDICO';`.",
        "related_concepts": ["c_independencia_datos", "c_ansi_sparc"],
        "common_confusions": "Creer que una vista estándar duplica los datos en disco: solo almacena la definición del SELECT en el diccionario.",
        "difficulty": "medio",
        "source_document": "Ejercicio 2 Para Resolver.pdf",
        "source_page": "Págs. 1-2",
        "order_idx": 53
    },
    {
        "id": "c_caso_ventas_tp",
        "topic_id": "u8_t4",
        "name": "Caso Comercio y Ventas (Trabajo Práctico Oficial de Cátedra)",
        "definition": "Esquema empresarial compuesto por CLIENTES, PRODUCTOS, VENTAS, DETALLE_VENTA y EMPLEADOS. Abarca 20 requerimientos de negocio de examen que combinan funciones de agregación, filtros en WHERE y HAVING, ordenamiento, y detección de clientes inactivos con LEFT JOIN e IS NULL.",
        "explanation": "Es el trabajo práctico troncal de la cursada utilizado por los profesores para evaluar la destreza del alumno en SQL Server.",
        "simple_explanation": "El TP oficial de la materia con ventas, detalles y productos que integra todo lo visto en el año.",
        "example": "Consigna 18: `SELECT id_cliente, SUM(total) FROM Ventas GROUP BY id_cliente HAVING SUM(total) > 50000;`.",
        "related_concepts": ["c_sql_joins", "c_having_vs_where"],
        "common_confusions": "Intentar calcular el total de una venta sumando precios unitarios en la tabla Ventas en vez de hacer JOIN con Detalle_Venta.",
        "difficulty": "dificil",
        "source_document": "TP_Ingeniería de Datos.pdf",
        "source_page": "Págs. 1-2",
        "order_idx": 54
    }
]

QUESTIONS = [
    {
        "id": "q8_1",
        "topic_id": "u8_t1",
        "concept_id": "c_caso_pubs_ddl",
        "type": "multiple_choice",
        "difficulty": "medio",
        "question": "En el caso de la Cadena de Bares/Pubs, ¿cuál de las siguientes restricciones CHECK valida correctamente que el atributo 'HORARIO' admita de forma excluyente únicamente los códigos 'HOR1', 'HOR2' o 'HOR3'?",
        "options": [
            {"id": "a", "text": "CONSTRAINT CK_PUB_HORARIO CHECK (HORARIO IN ('HOR1', 'HOR2', 'HOR3'))"},
            {"id": "b", "text": "CONSTRAINT CK_PUB_HORARIO CHECK (HORARIO = 'HOR1' AND HORARIO = 'HOR2')"},
            {"id": "c", "text": "CONSTRAINT CK_PUB_HORARIO CHECK (HORARIO LIKE 'HOR%')"},
            {"id": "d", "text": "CONSTRAINT CK_PUB_HORARIO CHECK (HORARIO BETWEEN 'HOR1' AND 'HOR3')"}
        ],
        "correct_answer": "a",
        "explanation": "La opción A es correcta. El operador de membresía `IN ('HOR1', 'HOR2', 'HOR3')` exige que el valor coincida con alguno de los elementos explícitos del conjunto. La opción B es lógicamente imposible (un valor no puede ser igual a dos cosas distintas simultáneamente con AND).",
        "hint1": "Buscá el operador que verifica pertenencia a una lista de opciones válidas.",
        "hint2": "Se utiliza la palabra clave `IN`.",
        "source_document": "Ejercicio 1 DDL Solucion.pdf",
        "source_page": "Pág. 1",
        "semantic_hash": "hash_q8_1_check_horario_pubs"
    },
    {
        "id": "q8_2",
        "topic_id": "u8_t2",
        "concept_id": "c_caso_viajes_sql",
        "type": "multiple_choice",
        "difficulty": "dificil",
        "question": "En el modelo de la Agencia de Viajes, la tabla VIAJE contiene el atributo `v_cd_viaje_rec`. ¿Qué tipo de relación y diseño relacional modela este atributo?",
        "options": [
            {"id": "a", "text": "Una clave foránea recursiva (auto-referencial) que apunta a la propia tabla VIAJE(v_codigo) para representar el viaje previo de conexión del que depende el tramo actual."},
            {"id": "b", "text": "Una clave primaria alternativa generada automáticamente por el motor."},
            {"id": "c", "text": "Una relación N:M con la tabla PASAJERO."},
            {"id": "d", "text": "Un atributo derivado que calcula la distancia en kilómetros entre el origen y el destino."}
        ],
        "correct_answer": "a",
        "explanation": "La opción A es correcta. `v_cd_viaje_rec` es una Foreign Key reflexiva. Modela una relación 1:N sobre la misma entidad VIAJE, donde un viaje puede estar encadenado a un viaje previo (conexión aérea o terrestre).",
        "hint1": "Observá que termina con '_rec' por recursivo.",
        "hint2": "Vincula un viaje con otro viaje previo de conexión en la misma tabla.",
        "source_document": "Ejercicio 1 solucion.pdf",
        "source_page": "Pág. 1",
        "semantic_hash": "hash_q8_2_fk_recursiva_viajes"
    },
    {
        "id": "q8_3",
        "topic_id": "u8_t4",
        "concept_id": "c_caso_ventas_tp",
        "type": "open_question",
        "difficulty": "dificil",
        "question": "En el Trabajo Práctico de Ventas de la cátedra, escriba la consulta SQL que resuelva la consigna: 'Obtener el ID, Nombre y Apellido de los clientes que hayan acumulado un total de compras superior a $50.000, ordenados de mayor a menor según el monto total'.",
        "options": [],
        "correct_answer": "SELECT c.id_cliente, c.nombre, c.apellido, SUM(v.total) AS total_comprado\nFROM Clientes c\nJOIN Ventas v ON c.id_cliente = v.id_cliente\nGROUP BY c.id_cliente, c.nombre, c.apellido\nHAVING SUM(v.total) > 50000\nORDER BY total_comprado DESC;",
        "explanation": "Criterio de evaluación: JOIN entre Clientes y Ventas, GROUP BY con todas las columnas no agregadas del SELECT (id, nombre, apellido), filtro en HAVING con SUM(v.total) > 50000, y ORDER BY descendente.",
        "hint1": "Tenés que agrupar por cliente y sumar el total de sus ventas.",
        "hint2": "El filtro de más de $50.000 va en el HAVING porque aplica sobre la función SUM().",
        "source_document": "TP_Ingeniería de Datos.pdf",
        "source_page": "Pág. 2 (Consigna 18)",
        "semantic_hash": "hash_q8_3_open_tp_ventas_18"
    }
]
