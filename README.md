# 🎓 Plataforma de Estudio & Práctica — Ingeniería de Datos I

Plataforma educativa interactiva, moderna y adaptativa para la preparación del examen de **Ingeniería de Datos I** (Cátedra: Lic. Gustavo E. Escandell, Ing. Melinda Selles, Ing. Charles Maldonado y Gustavo Arenas), basada **exclusivamente en las 5 presentaciones oficiales de diapositivas**.

---

## 🌐 Despliegue en Vercel

Este repositorio está pre-configurado para desplegarse de manera inmediata en **Vercel**:
- **Frontend:** React + Vite + TypeScript + Tailwind CSS (empaquetado estático optimizado en CDN).
- **Backend API:** Python FastAPI Serverless Functions en `api/index.py`.
- **Base de Datos:** SQLite pre-sembrada con 38 temas, 43 conceptos y 38 preguntas, con replicación automática a `/tmp/plataforma.db` en entornos serverless.
- **Apunte Oficial:** PDF de 22 páginas disponible para descarga directa en `/Material_de_Estudio_Ingenieria_de_Datos_I.pdf`.

### Pasos para desplegar en Vercel:
1. Conectá el repositorio GitHub `nsh1z/examplat` en tu cuenta de Vercel ([vercel.com/new](https://vercel.com/new)).
2. Hacé clic en **Deploy** (los valores predeterminados de Vite y Python se detectan automáticamente sin necesidad de cambiar ninguna variable ni el directorio raíz).
3. ¡Listo! Tu plataforma estará online en tu dominio de Vercel.

---

## 🚀 Ejecución Local

### Opción A (Lanzador automático en Windows)
Hacé doble clic en:
```cmd
iniciar.bat
```
o ejecutá en PowerShell:
```powershell
python run.py
```
El lanzador iniciará el servidor backend y la interfaz web en:
👉 **[http://localhost:8000](http://localhost:8000)**

### Opción B (Desarrollo Frontend con Vite)
```bash
# Instalar dependencias
npm install

# Compilar para producción
npm run build

# Iniciar servidor de desarrollo local
npm run dev
```

---

## 📚 Temario Oficial Calibrado (6 Unidades Académicas)

1. **Unidad 1: Fundamentos de Bases de Datos & Arquitectura SGBD**
   * *Fuente:* `Clase nro 1 Ingeniería de Datos 1.pdf`
   * Dato vs Información, evolución de archivos (secuencial, directo, indexado y fórmulas de tiempo medio de acceso), SGBD, ACID, arquitectura ANSI/SPARC de 3 niveles, ciclo de los 14 pasos de una consulta, modelos de datos y roles (DBA vs DA).

2. **Unidad 2: Modelado Conceptual con DER Clásico**
   * *Fuente:* `Diagramas de Entidad Relación y Modelo de Datos.pdf`
   * Niveles de abstracción, entidades fuertes y débiles, atributos, cardinalidades y razones de participación ($1:1, 1:N, N:M$), reglas gramaticales del grafo DER y resolución del caso Constructora.

3. **Unidad 3: Modelo EER Extendido y Jerarquías**
   * *Fuente:* `Clase nro 11 - Mássss DER.pdf`
   * Superclases, subclases, herencia de atributos, especialización vs generalización, restricciones de disyunción ($d$ vs $o$) y completitud (total vs parcial).

4. **Unidad 4: El Modelo Relacional & Reglas de Codd**
   * *Fuente:* `El Modelo Relacional.pdf`
   * Fundamentos de E. F. Codd (1970), dominios, tuplas, relaciones, grado y cardinalidad, propiedades de las tablas, teoría de claves (superclave, candidata, primaria, alternativa, foránea), semántica de $NULL$, reglas de integridad y análisis de las 12 Reglas de Codd.

5. **Unidad 5: Álgebra Relacional Formal**
   * *Fuente:* `Algebra Relacional.pdf`
   * Operadores unarios ($\sigma, \pi, \rho$), binarios de conjuntos ($\cup, \cap, -, \times$) con unión-compatibilidad, derivados ($\bowtie_\theta, \bowtie, \div$) y **resolución de las 16 consultas formales** del esquema Almacenes-Proveedores.

6. **Unidad 6: Metodología de Mapeo DER/EER a Esquema Relacional**
   * *Fuente:* `Clase nro 11 - Mássss DER.pdf` y `El Modelo Relacional.pdf`
   * Algoritmo de traducción canónico: Reglas 1 a 8 y las 4 Opciones para jerarquías EER (Opción A: Superclase + Subclases, Opción B: Solo Subclases, Opción C: Tabla Única con Discriminante, Opción D: Tabla Única con Banderas Booleanas).

---

## 🛠️ Tecnologías Utilizadas

- **Frontend:** React 18, TypeScript, Vite 5, Tailwind CSS, Lucide Icons, KaTeX (renderizado matemático $\LaTeX$).
- **Backend Serverless:** Python 3.10+, FastAPI, Pydantic, SQLite3, Uvicorn.
- **Algoritmos de Estudio:** SuperMemo-2 (SM-2) para repetición espaciada, sistema anti-repetición con hashing semántico.
- **Plataforma de Despliegue:** Vercel (Edge CDN + Serverless Functions).
