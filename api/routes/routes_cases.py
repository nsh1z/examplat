from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

router = APIRouter(prefix="/api/cases", tags=["cases"])

CASES_DATA = [
    {
        "id": "case_algebra",
        "title": "Caso 1: Álgebra Relacional Formal (Las 16 Consultas de Cátedra)",
        "category": "Álgebra Relacional y Consultas Matemáticas",
        "description": "Resolución matemática rigurosa de la guía oficial de consultas sobre el esquema Almacenes, Artículos, Materiales y Proveedores, incluyendo selecciones, proyecciones, juntas, diferencias e división relacional.",
        "schema_ddl": """-- Esquema Formal de Álgebra Relacional (Cátedra)
Almacen (Nro, Responsable)
Articulo (Cod_art, descripcion, Precio)
Material (Cod_mat, Descripcion)
Proveedor (Cod_prov, Nombre, Domicilio, Ciudad)
Tiene (Nro, Cod_art)
Compuesto_por (Cod_art, Cod_mat)
Provisto_por (Cod_mat, Cod_prov)""",
        "total_queries": 16,
        "sample_queries": [
            {
                "num": 1,
                "prompt": "Listar los nombres de los proveedores de la ciudad de La Plata.",
                "solution": "Π_Nombre(σ_Ciudad = 'La Plata'(Proveedor))",
                "explanation": "Selección horizontal (σ) en la tabla Proveedor por Ciudad = 'La Plata' y proyección vertical (Π) del atributo Nombre."
            },
            {
                "num": 2,
                "prompt": "Listar los números de artículos cuyo precio sea inferior a $10.",
                "solution": "Π_Cod_art(σ_Precio < 10(Articulo))",
                "explanation": "Selección con predicado numérico Precio < 10 y proyección sobre la clave Cod_art."
            },
            {
                "num": 3,
                "prompt": "Listar los responsables de los almacenes.",
                "solution": "Π_Responsable(Almacen)",
                "explanation": "Proyección directa sobre la columna Responsable (elimina automáticamente duplicados según la teoría de conjuntos)."
            },
            {
                "num": 4,
                "prompt": "Listar los códigos de los materiales que provea el proveedor 10 y no los provea el proveedor 15.",
                "solution": "Π_Cod_mat(σ_Cod_prov = 10(Provisto_por)) - Π_Cod_mat(σ_Cod_prov = 15(Provisto_por))",
                "explanation": "Diferencia de conjuntos (-) entre la proyección de materiales provistos por el proveedor 10 y los provistos por el 15. Requiere unión-compatibilidad."
            },
            {
                "num": 7,
                "prompt": "Listar los almacenes que contienen los artículos A y los artículos B (ambos simultáneamente).",
                "solution": "Π_Nro(σ_Cod_art = 'A'(Tiene)) ∩ Π_Nro(σ_Cod_art = 'B'(Tiene))",
                "explanation": "Intersección formal (∩) entre los números de almacenes con artículo A y los almacenes con artículo B."
            },
            {
                "num": 15,
                "prompt": "Hallar el o los códigos de los artículos de mayor precio.",
                "solution": "Π_Cod_art(Articulo) - Π_A1.Cod_art(Articulo A1 ⋈_(A1.Precio < A2.Precio) Articulo A2)",
                "explanation": "Se resta del universo total de artículos aquellos para los cuales existe al menos otro artículo con precio mayor mediante junta autorreferencial."
            },
            {
                "num": 16,
                "prompt": "Listar los números de almacenes que tienen TODOS los artículos existentes en el catálogo.",
                "solution": "Tiene ÷ (Π_Cod_art(Articulo))",
                "explanation": "División relacional (÷) que resuelve el cuantificador universal 'para todo'."
            }
        ],
        "source_document": "Algebra Relacional.pdf"
    },
    {
        "id": "case_constructora",
        "title": "Caso 2: Modelado DER — Empresa Constructora de Edificios",
        "category": "Diagramas Entidad-Relación y Restricciones",
        "description": "Caso troncal de modelado de la cátedra: Personal asignado a Obras con Ficha de Actividad (fecha, hora, tarea), Profesionales externos asignados a Obras, Recursos asignados con Planilla de Uso (roturas, fechas) y Proveedores con Contratos de Alquiler de recursos.",
        "schema_ddl": """-- Entidades y Relaciones del Caso Constructora
Entidades Fuertes:
- PERSONAL (legajo, nombre, especialidad)
- OBRAS (cod_obra, direccion, fecha_inicio)
- TAREAS (id_tarea, descripcion)
- PROFESIONALES (matricula, nombre, especialidad)
- RECURSOS (id_recurso, tipo_recurso, propio_o_alquilado)
- PROVEEDORES (cuit, razon_social, telefono)

Relaciones con Atributos:
- FICHA_ACTIVIDAD (conecta Personal con Obras; atributos: fecha, hora, actividad)
- PLANILLA_USO (conecta Recursos con Obras; atributos: fecha_desde, fecha_hasta, sufrio_roturas)
- CONTRATO_ALQUILER (conecta Recursos con Proveedores; atributos: nro_contrato, monto, fecha_firma)""",
        "total_queries": 4,
        "sample_queries": [
            {
                "num": 1,
                "prompt": "¿Por qué los atributos 'fecha', 'hora' y 'actividad' deben residir en la relación 'Ficha de Actividad' y no dentro de la entidad Personal?",
                "solution": "Porque una persona puede trabajar en múltiples obras en distintas fechas y horarios. Si se pusieran en Personal, no se podrían registrar múltiples asistencias sin violar la 1NF o duplicar registros.",
                "explanation": "La cardinalidad N:M entre Personal y Obras exige que los atributos de cada ocurrencia pertenezcan a la relación de asignación."
            },
            {
                "num": 2,
                "prompt": "¿Cómo se modela la participación de Profesionales si una obra puede no contar con ningún profesional?",
                "solution": "Cardinalidad de participación: Obra (0, N) y Profesional (1, N) o (0, N). La participación mínima de la Obra es 0 (parcial).",
                "explanation": "El enunciado establece que solo se asignan profesionales cuando no existe personal propio especializado."
            }
        ],
        "source_document": "Diagramas de Entidad Relación y Modelo de Datos.pdf"
    },
    {
        "id": "case_mapeo_practico",
        "title": "Caso 3: Taller de Mapeo DER/EER a Esquema Relacional",
        "category": "Diseño Lógico y Reglas de Traducción",
        "description": "Aplicación rigurosa de los 8 pasos canónicos de mapeo: Entidades Fuertes, Entidades Débiles (Película/Copia), Relaciones 1:N (Empleado/Departamento), 1:1 (Empleado/Dirige con 3 métodos), M:N (Colabora en Proyecto), Multivaluados (Emails) y Recursivas (Jefe, Amistad).",
        "schema_ddl": """-- Esquema Relacional Resultante del Mapeo Sistemático
CREATE TABLE EMPLEADO (
    legajo INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    dni VARCHAR(15) UNIQUE NOT NULL,
    fec_nac DATE NOT NULL,
    legajo_jefe INT, -- Clave foránea recursiva 1:N
    nombre_depto VARCHAR(50) NOT NULL, -- Clave foránea 1:N
    FOREIGN KEY (legajo_jefe) REFERENCES EMPLEADO(legajo),
    FOREIGN KEY (nombre_depto) REFERENCES DEPARTAMENTO(nombre_depto)
);

CREATE TABLE PROYECTO (
    cod_proyecto INT PRIMARY KEY,
    presupuesto DECIMAL(12,2) NOT NULL
);

-- Mapeo de relación M:N (Paso 5)
CREATE TABLE COLABORA (
    legajo INT NOT NULL,
    cod_proyecto INT NOT NULL,
    horas INT DEFAULT 0,
    PRIMARY KEY (legajo, cod_proyecto),
    FOREIGN KEY (legajo) REFERENCES EMPLEADO(legajo),
    FOREIGN KEY (cod_proyecto) REFERENCES PROYECTO(cod_proyecto)
);

-- Mapeo de atributo multivaluado (Paso 6 - Opción 3 normalizada)
CREATE TABLE EMPLEADO_EMAIL (
    legajo INT NOT NULL,
    direccion_email VARCHAR(100) NOT NULL,
    PRIMARY KEY (legajo, direccion_email),
    FOREIGN KEY (legajo) REFERENCES EMPLEADO(legajo) ON DELETE CASCADE
);""",
        "total_queries": 4,
        "sample_queries": [
            {
                "num": 1,
                "prompt": "¿Por qué en la tabla COLABORA la clave primaria debe ser compuesta (legajo, cod_proyecto)?",
                "solution": "Porque un empleado colabora en muchos proyectos y un proyecto tiene muchos empleados (N:M). La combinación de ambas FKs identifica inequívocamente cada asignación.",
                "explanation": "Regla del Paso 5 de mapeo de relaciones binarias M:N (Pág. 41-42 de Clase nro 11)."
            },
            {
                "num": 2,
                "prompt": "Al mapear una relación reflexiva N:N de 'amistad' entre Personas, ¿por qué se requieren dos claves foráneas hacia la misma tabla?",
                "solution": "Porque cada fila representa un vínculo entre dos personas distintas que actúan en roles idénticos: Persona 1 y Persona 2.",
                "explanation": "Regla del Paso 8 (Pág. 53 de Clase nro 11): Tabla Amigo(DNI_Persona1, DNI_Persona2, anios)."
            }
        ],
        "source_document": "Clase nro 11 - Mássss DER.pdf"
    },
    {
        "id": "case_jerarquias_eer",
        "title": "Caso 4: Mapeo de Especializaciones EER (Las 4 Opciones)",
        "category": "Jerarquías de Herencia y Estrategias Relacionales",
        "description": "Comparación práctica de las 4 opciones oficiales para traducir jerarquías de herencia: Empleados con Técnicos, Secretarias y Licenciados. Evaluación de nulos, juntas requeridas y precondiciones de disyunción y completitud.",
        "schema_ddl": """-- Opción 1: Múltiples Tablas (Superclase y Subclases) - Universal
CREATE TABLE EMPLEADO (legajo INT PRIMARY KEY, nombre VARCHAR(100), fec_nac DATE);
CREATE TABLE TECNICO (legajo INT PRIMARY KEY, grd_experiencia INT, FOREIGN KEY (legajo) REFERENCES EMPLEADO(legajo));
CREATE TABLE SECRETARIA (legajo INT PRIMARY KEY, vel_escritura INT, FOREIGN KEY (legajo) REFERENCES EMPLEADO(legajo));
CREATE TABLE LICENCIADO (legajo INT PRIMARY KEY, especializacion VARCHAR(50), FOREIGN KEY (legajo) REFERENCES EMPLEADO(legajo));

-- Opción 2: Solo Subclases (Precondición: Total y Disyunta)
CREATE TABLE TECNICO_SOLO (legajo INT PRIMARY KEY, nombre VARCHAR(100), fec_nac DATE, grd_experiencia INT);
CREATE TABLE SECRETARIA_SOLO (legajo INT PRIMARY KEY, nombre VARCHAR(100), fec_nac DATE, vel_escritura INT);

-- Opción 3: Tabla Única con Discriminante (Precondición: Disyunción)
CREATE TABLE EMPLEADO_UNICO (legajo INT PRIMARY KEY, nombre VARCHAR(100), tipo_empleado CHAR(1), grd_experiencia INT, vel_escritura INT, especializacion VARCHAR(50));

-- Opción 4: Tabla Única con Banderas Booleanas (Apta para Solapamiento)
CREATE TABLE EMPLEADO_BOOLEANO (legajo INT PRIMARY KEY, nombre VARCHAR(100), es_tecnico BOOLEAN, es_secretaria BOOLEAN, es_licenciado BOOLEAN);""",
        "total_queries": 3,
        "sample_queries": [
            {
                "num": 1,
                "prompt": "¿En qué escenario es ESTRICTAMENTE PROHIBIDO utilizar la Opción 2 de mapeo?",
                "solution": "Cuando la especialización es PARCIAL (porque se perderían los empleados que no son ni técnicos ni secretarias) o cuando tiene SOLAPAMIENTO (porque se duplicarían los datos comunes del empleado en dos tablas diferentes).",
                "explanation": "La Opción 2 exige precondición estricta de Totalidad y Disyunción (t, d) según la diapositiva 56 de Clase nro 11."
            },
            {
                "num": 2,
                "prompt": "¿Qué desventaja principal tiene la Opción 3 (tabla única con atributo discriminante)?",
                "solution": "Genera una gran cantidad de valores nulos (NULL) en las columnas específicas de las subclases a las que no pertenece la tupla.",
                "explanation": "Si un empleado es Secretaria, sus columnas grd_experiencia y especializacion quedan forzosamente con valor NULL."
            }
        ],
        "source_document": "Clase nro 11 - Mássss DER.pdf"
    }
]

@router.get("")
def get_cases():
    return [{
        "id": c["id"],
        "title": c["title"],
        "category": c["category"],
        "description": c["description"],
        "total_queries": c["total_queries"],
        "source_document": c["source_document"]
    } for c in CASES_DATA]

@router.get("/{case_id}")
def get_case_detail(case_id: str):
    for c in CASES_DATA:
        if c["id"] == case_id:
            return c
    raise HTTPException(status_code=404, detail="Case not found")
