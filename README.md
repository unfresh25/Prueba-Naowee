# Prueba Técnica para Científico de Datos - Naowee

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Quarto](https://img.shields.io/badge/Quarto-Documentation-orange.svg)](https://quarto.org/)

Solución completa de la prueba técnica para el rol de Científico de Datos, que incluye análisis exploratorio de datos, visualizaciones interactivas, modelos predictivos de Machine Learning y una API REST dockerizada.

## Autor

**Jorge Borja**
- LinkedIn: [jorgeborjas25](https://www.linkedin.com/in/jorgeborjas25/)
- GitHub: [@unfresh25](https://github.com/unfresh25/Prueba-Naowee)

---

## Tabla de Contenidos

- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Casos de Estudio](#-casos-de-estudio)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [API REST](#-api-rest)
- [Documentación](#-documentación)
- [Resultados](#-resultados)

---

## Estructura del Proyecto

```
Prueba-Naowee/
├── case1/                      # Caso 1: Análisis FIFA
│   ├── fifa.py                 # Script principal
│   └── services/
│       ├── analysis.py         # Servicio de análisis de datos
│       └── results.py          # Servicio de cálculo de resultados
│
├── case2/                      # Caso 2: API de predicción
│   ├── app/
│   │   ├── main.py            # Aplicación FastAPI
│   │   ├── config.py          # Configuración
│   │   ├── models/            # Schemas Pydantic
│   │   ├── repositories/      # Capa de datos (CRUD simulado)
│   │   ├── routers/           # Endpoints de la API
│   │   └── services/          # Lógica de negocio
│   ├── models/                # Modelos ML entrenados (.pkl)
│   ├── test/                  # Tests y ejemplos
│   ├── Dockerfile             # Imagen Docker
│   ├── docker-compose.yml     # Orquestación Docker
│   └── requirements.txt       # Dependencias Python
│
├── preview/                    # Previews del sitio web
├── raw/                        # Scripts iniciales/borradores
├── .gitignore
└── Prueba Técnica para Científicos de Datos.pdf
```

---

## Casos de Estudio

### Caso 1: Análisis de la Copa Mundial Femenina de la FIFA (1991-2023)

**Objetivo:** Analizar tendencias históricas del torneo, identificar equipos dominantes y patrones de rendimiento.

**Datasets:**
- [world_cup_women.csv](https://raw.githubusercontent.com/daramireh/simonBolivarCienciaDatos/refs/heads/main/world_cup_women.csv)
- [matches_1991_2023.csv](https://raw.githubusercontent.com/daramireh/simonBolivarCienciaDatos/refs/heads/main/matches_1991_2023.csv)

**Preguntas clave:**
- ¿Cómo ha evolucionado el promedio de goles por partido?
- ¿Cuáles son las selecciones con mejor desempeño histórico?
- ¿Qué tendencias existen en equipos dominantes vs. de bajo rendimiento?

**Técnicas aplicadas:**
- Análisis exploratorio de datos (EDA)
- Limpieza y transformación de datos
- Cálculo de métricas de rendimiento (Win Rate, Goal Difference)
- Análisis de consistencia temporal
- Visualizaciones con Matplotlib

**Componentes:**
- `AnalysisService`: Análisis de estructura de datos, detección de nulos y duplicados
- `ResultsService`: Cálculo de estadísticas de equipos, goleadores y resultados por torneo

---

### Caso 2: Predicción de Desempeño Estudiantil en Matemáticas

**Objetivo:** Desarrollar modelos predictivos para identificar estudiantes con riesgo de bajo rendimiento académico.

**Dataset:**
- [Student_Performance.csv](https://raw.githubusercontent.com/daramireh/simonBolivarCienciaDatos/refs/heads/main/Student_Performance.csv)

**Preguntas clave:**
- ¿Qué factores influyen más en el rendimiento en matemáticas?
- ¿Existe correlación entre tiempo de estudio y calificación final?
- ¿Cómo afectan las actividades extracurriculares al desempeño?

**Análisis realizado:**
1. **Estructuras de datos:**
   - Diccionario de datos
   - Visualizaciones descriptivas
   - Transformaciones y feature engineering

2. **Análisis exploratorio:**
   - Estadística descriptiva
   - Pruebas de hipótesis (diferencias en Performance Index)
   - Clustering de estudiantes

3. **Modelos predictivos:**
   - **Regresión:** Predicción del Performance Index
   - **Clasificación:** Identificación de estudiantes de bajo rendimiento
   - Comparación de modelos (mínimo 3)
   - Métricas de evaluación y selección del mejor modelo

**API REST Dockerizada:**
- Framework: FastAPI
- Arquitectura: Principios SOLID aplicados
- CRUD simulado con diccionarios
- Endpoints de predicción y gestión de estudiantes
- Documentación automática (Swagger/Redoc)

---

## Tecnologías

### Lenguajes y Frameworks
- **Python 3.11**
- **FastAPI** - API REST moderna y rápida
- **Uvicorn** - Servidor ASGI
- **Quarto** - Documentación científica interactiva

### Machine Learning y Data Science
- **scikit-learn** - Modelos de ML
- **pandas** - Manipulación de datos
- **numpy** - Computación numérica
- **matplotlib** - Visualizaciones

### Infraestructura
- **Docker** - Contenedorización
- **Docker Compose** - Orquestación
- **joblib** - Serialización de modelos

### Desarrollo
- **Pydantic** - Validación de datos
- **python-multipart** - Manejo de formularios

---

## Instalación

### Prerrequisitos
- Python 3.11+
- Docker y Docker Compose (para la API)
- Quarto (opcional, para regenerar documentación)

### Opción 1: Instalación Local (Caso 1)

```bash
git clone https://github.com/unfresh25/Prueba-Naowee.git
cd Prueba-Naowee

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

cd case1
pip install pandas

python fifa.py
```

### Opción 2: Docker (Caso 2 - API)

```bash
cd case2

docker-compose up --build

# La API estará disponible en http://localhost:8000
```

### Opción 3: Entorno Virtual (Caso 2 - API)

```bash
cd case2

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Uso

### Caso 1: Análisis FIFA

```bash
cd case1
python fifa.py
```

El script generará:
- Resumen de datos y validaciones
- Tablas de resultados por torneo
- Estadísticas de goleadores
- Análisis de tendencias
- Rankings de equipos

### Caso 2: API de Predicción

#### Iniciar la API

```bash
cd case2
docker-compose up

cd case2
uvicorn app.main:app --reload
```

#### Acceder a la Documentación

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## API REST

### Endpoints Principales

#### Health Check
```http
GET /health
```

Respuesta:
```json
{
  "status": "healthy",
  "app_name": "Student Performance Prediction API",
  "version": "1.0.0",
  "models_loaded": true,
  "timestamp": "2025-12-18T07:00:00"
}
```

#### Predicción de Rendimiento

**Clasificación** (Bajo rendimiento: Sí/No)
```http
POST /api/v1/predictions/classification
Content-Type: application/json

{
  "hours_studied": 5,
  "previous_scores": 75,
  "extracurricular_activities": "Yes",
  "sleep_hours": 7,
  "sample_question_papers_practiced": 3
}
```

**Regresión** (Performance Index)
```http
POST /api/v1/predictions/regression
Content-Type: application/json

{
  "hours_studied": 5,
  "previous_scores": 75,
  "extracurricular_activities": "Yes",
  "sleep_hours": 7,
  "sample_question_papers_practiced": 3
}
```

#### Gestión de Estudiantes (CRUD)

```http
# Listar estudiantes
GET /api/v1/students

# Obtener estudiante
GET /api/v1/students/{student_id}

# Crear estudiante
POST /api/v1/students

# Actualizar estudiante
PUT /api/v1/students/{student_id}

# Eliminar estudiante
DELETE /api/v1/students/{student_id}
```

### Ejemplos con cURL

```bash
curl -X GET "http://localhost:8000/health"

curl -X POST "http://localhost:8000/api/v1/predictions/classification" \
  -H "Content-Type: application/json" \
  -d '{
    "hours_studied": 5,
    "previous_scores": 75,
    "extracurricular_activities": "Yes",
    "sleep_hours": 7,
    "sample_question_papers_practiced": 3
  }'

curl -X GET "http://localhost:8000/api/v1/students"
```

---

## Documentación

La documentación completa del proyecto está construida con **Quarto** y disponible en formato web interactivo. La puedes ver
[aquí](https://unfresh25.github.io/Prueba-Naowee/preview/)

### Contenido de la Documentación

- **Introducción:** Contexto y objetivos de la prueba
- **Caso 1:** Análisis completo de la Copa Mundial Femenina
- **Caso 2:**
  - Propuesta del caso
  - Análisis exploratorio de datos
  - Modelos predictivos y evaluación

---
