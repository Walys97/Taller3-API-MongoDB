# Taller 3 — APIs Públicas, MongoDB y EDA

Proyecto del curso **Bases de Datos para Ciencia de Datos** (Universidad de Antioquia).
Autora: **Walys Vera Herrera**.

Simula un flujo de Ciencia de Datos real en tres etapas:

1. **Extracción**: se consume una API pública.
2. **Almacenamiento**: los datos se guardan crudos (raw) en MongoDB.
3. **Análisis**: se leen desde MongoDB y se hace un análisis exploratorio en Jupyter Notebook.

## API utilizada

**Art Institute of Chicago** — https://api.artic.edu/api/v1/artworks

Es una API pública y gratuita del museo Art Institute of Chicago. No requiere llave de acceso
y expone más de 130.000 obras de arte. De cada obra devuelve un JSON anidado con más de 70
campos: título, artista, año de creación, lugar de origen, departamento, dimensiones y más.

Para este taller se descargan **200 obras** (2 páginas de 100), por encima del mínimo de 100
que pide el enunciado.

## Estructura del repositorio

```text
ingesta.py        Script de extracción desde la API y carga RAW en MongoDB
analisis.ipynb    Notebook con la lectura desde MongoDB y el análisis exploratorio
requirements.txt  Librerías necesarias
.gitignore        Archivos excluidos del control de versiones
README.md         Este archivo
```

## Requisitos previos

- Python 3.10 o superior
- MongoDB Community Server corriendo en local (`mongodb://localhost:27017`)
- MongoDB Compass (opcional, para visualizar los datos)

## Cómo ejecutarlo

1. Clonar el repositorio y entrar a la carpeta:

   ```bash
   git clone https://github.com/Walys97/Taller3-API-MongoDB.git
   cd Taller3-API-MongoDB
   ```

2. Crear el entorno virtual e instalar las librerías:

   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1      # Windows
   source .venv/bin/activate       # Mac / Linux
   pip install -r requirements.txt
   ```

3. Ejecutar la ingesta (crea `taller3_db.raw_data` y guarda las 200 obras):

   ```bash
   python ingesta.py
   ```

   Salida esperada:

   ```text
   Descargando pagina 1 de 2...
   Descargando pagina 2 de 2...
   Documentos guardados o actualizados: 200
   Total en taller3_db.raw_data: 200
   ```

4. Abrir el notebook y ejecutar todas las celdas:

   ```bash
   jupyter notebook analisis.ipynb
   ```

## Qué hace cada archivo

### `ingesta.py` — Fases 1 y 2

- Pide las obras a la API con `requests` (2 páginas de 100 registros).
- Se conecta a MongoDB con `pymongo`.
- Crea la base **`taller3_db`** y la colección **`raw_data`**.
- Guarda el JSON **sin modificar** y usa el `id` de la API como **`_id`** del documento,
  de modo que volver a ejecutar el script no duplica datos (`replace_one` con `upsert`).

### `analisis.ipynb` — Fase 3

- Lee la colección desde MongoDB y arma un DataFrame con **7 variables**:
  `id`, `title`, `artist_title`, `place_of_origin`, `date_start`, `department_title`
  e `is_public_domain`.
- Inspección básica: `head()`, `info()` y conteo de valores nulos.
- **5 insights numéricos** sobre la colección.
- **3 gráficos**: torta por departamento, barras por lugar de origen e histograma del
  año de creación.
  ## Resultados principales

A partir de las 200 obras analizadas:

1. El conjunto tiene **200 obras** de **117 artistas distintos**.
2. La artista con más obras es **Georgia O'Keeffe**, con 12 obras.
3. El departamento con más obras es **Painting and Sculpture of Europe**: 48 obras (24% del total).
4. El año de creación promedio es **1816**; la obra más antigua es del año **883 a.C.** y la más reciente de **2020**.
5. **107 obras (53.5%)** son de dominio público y 93 no lo son.

La colección está dominada por el arte europeo y estadounidense: **Estados Unidos** es el
lugar de origen más frecuente con **80 obras (40%)**, seguido de Francia con 27. El histograma
muestra que la mayoría de las piezas se crearon entre **1880 y 2000**, con un pico entre 1900 y 1925.