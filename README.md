# Aplicación Flask para Análisis de Proceso de Jerarquía Analítica (AHP)

Esta aplicación Flask permite a los usuarios resolver problemas de AHP mediante tres métodos diferentes: **Autovalores**, **Método de Aproximación** y **Media Geométrica**. Los usuarios pueden cargar archivos CSV con criterios y alternativas, seleccionar el método de resolución y ver los resultados en una interfaz gráfica profesional y responsive.

Puedes acceder en la web a [AHP Solver](https://thisisjosepablo3.pythonanywhere.com/), sin la necesidad de clonar este repositorio. De todos modos explicaré cómo hacerlo.
## Características

- **Carga de archivos CSV** para criterios y alternativas.
- **Selección del método de resolución AHP**: Autovalores, Método de Aproximación, o Media Geométrica.
- **Resultados**: muestra el ranking de alternativas y, si el método seleccionado es Autovalores, también la información de consistencia (CI, RI y CR).
- **Interfaz gráfica responsive** y moderna construida con Bootstrap y estilos personalizados en CSS.

## Requisitos Previos

1. **Python 3.x**: Asegúrate de tener instalado Python 3.x en tu sistema.
2. **Instalación de dependencias**: Instala Flask y Pandas, necesarios para ejecutar la aplicación.

### Instalación de Dependencias

```bash
pip install flask pandas
```

## Estructura del Proyecto

```
AHP-Flask-App/
│
├── app.py                 # Archivo principal de la aplicación Flask
├── templates/
│   ├── index.html         # Plantilla de carga de archivos y selección de método
│   └── result.html        # Plantilla para mostrar los resultados del análisis
├── README.md              # Archivo de documentación (este archivo)
└── requirements.txt       # Lista de dependencias (opcional)
```

## Instrucciones de Uso

1. **Clona el repositorio** y navega al directorio del proyecto.

2. **Ejecuta la aplicación** con el siguiente comando:

   ```bash
   python app.py
   ```

3. **Abre un navegador web** y accede a `http://127.0.0.1:5000`.

4. **Cargar los archivos CSV**:
   - En la pantalla inicial, selecciona los archivos CSV para los criterios y las alternativas. Los archivos deben tener el siguiente formato:
     - **Criterios**: debe contener una matriz de comparación de criterios en formato CSV.
     - **Alternativas**: debe contener una matriz de comparación de alternativas en formato CSV.

5. **Seleccionar el método de resolución**:
   - Elige entre **Autovalores**, **Método de Aproximación**, y **Media Geométrica**.

6. **Ver los resultados**:
   - Al hacer clic en "Calcular", la aplicación mostrará el ranking de alternativas.
   - Si seleccionaste el método **Autovalores**, también verás una tabla con la información de consistencia (CI, RI y CR) para verificar la validez del análisis.

## Explicación del Código

### `app.py`

Este archivo contiene la lógica principal de la aplicación:

- **Rutas**:
  - `/`: Renderiza `index.html`, la página de carga de archivos y selección de método.
  - `/calculate`: Procesa los archivos CSV, ejecuta el método AHP seleccionado y renderiza `result.html` con los resultados.

- **Clase `AHP`**:
  - Define tres métodos de resolución de AHP:
    - `calcular_autovalores()`: Utiliza el método de autovalores.
    - `calcular_aproximacion()`: Utiliza el método de aproximación.
    - `calcular_media_geometrica()`: Utiliza el método de media geométrica.
  - Cada método retorna el ranking de alternativas (`ranking`) y la información de consistencia (`info_matrix`) en el mismo formato.

### `templates/index.html`

Página de inicio que permite a los usuarios cargar archivos CSV y seleccionar el método de resolución. Los elementos principales incluyen:

- **Formulario** para cargar archivos `criterios.csv` y `alternativas.csv`.
- **Selector de método** (`<select>`), donde los usuarios pueden elegir entre Autovalores, Método de Aproximación y Media Geométrica.
- **Estilos**: Usa Bootstrap para una apariencia profesional y responsive, además de estilos personalizados en CSS.

### `templates/result.html`

Página de resultados que muestra el ranking de alternativas y, si el método seleccionado es Autovalores, también la tabla de información de consistencia.

- **Condición Jinja**: Usa `{% if method == 'autovalores' %}` para mostrar la tabla de información de consistencia solo si el método seleccionado es "autovalores".
- **Ranking de Alternativas**: Se presenta como una lista, con los nombres y valores de las alternativas.
- **Información de Consistencia**: Incluye la CI (Índice de Consistencia), RI (Índice de Aleatoriedad) y CR (Ratio de Consistencia) para verificar la coherencia de las comparaciones.

## Ejemplo de Formato de los Archivos CSV

### `criterios.csv`

| Criterio 1 | Criterio 2 | Criterio 3 |
|------------|------------|------------|
| 1          | 3          | 0.5        |
| 0.33       | 1          | 2          |
| 2          | 0.5        | 1          |

### `alternativas.csv`

| Alternativa 1 | Alternativa 2 | Alternativa 3 |
|---------------|---------------|---------------|
| 1             | 4             | 0.25          |
| 0.25          | 1             | 3             |
| 4             | 0.33          | 1             |

> **Nota**: Asegúrate de que las matrices de comparación sean cuadradas.

## Personalización y Estilos

Esta aplicación utiliza Bootstrap para estilos básicos y responsividad. Los elementos clave en el diseño incluyen:

- **Selector de método**: Un `<select>` en `index.html` permite al usuario elegir el método deseado.
- **Tabla de resultados**: En `result.html`, una tabla muestra el ranking y la información de consistencia de manera clara y organizada.
- **Estilos Responsives**: El diseño se adapta a diferentes tamaños de pantalla gracias a Bootstrap y un contenedor central con un ancho máximo adecuado.

## Ejemplo de Resultados

Un ejemplo de los resultados generados podría ser:

```plaintext
Ranking de Alternativas:
1. Alternativa 2: 0.4646
2. Alternativa 1: 0.3039
3. Alternativa 3: 0.2314

Información de Consistencia (solo si el método es Autovalores):
| Matriz    | Autovalor | CI      | RI    | CR      |
|-----------|-----------|---------|-------|---------|
| C         | 5.53      | 0.51    | 0.9   | 0.57    |
| AC1       | 3.56      | 0.28    | 0.58  | 0.48    |
| AC2       | 3.11      | 0.06    | 0.58  | 0.10    |
| AC3       | 3.05      | 0.03    | 0.58  | 0.05    |
| AC4       | 3.09      | 0.05    | 0.58  | 0.08    |
```

## Contribuir

Si deseas contribuir a esta aplicación, puedes enviar un pull request o abrir un issue para discutir posibles mejoras.

