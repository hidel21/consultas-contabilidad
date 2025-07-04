# 📊 Generador de Reportes

Aplicación desarrollada en **Streamlit** para generar reportes dinámicos en formato Excel a partir de datos almacenados en una base de datos **PostgreSQL**. Está orientada a tres tipos principales de reportes utilizados por Bera Motorcycles:

- **Placas por Cliente (CINTAS)**
- **Facturación con Seriales (SENIAT)**
- **Despachos (SENIAT)**

---

## 🚀 Características

- Interfaz sencilla e interactiva con Streamlit.
- Conexión segura a PostgreSQL usando variables de entorno.
- Exportación directa a archivos `.xlsx`.
- Filtros por fechas, localidades y parámetros específicos de negocio.
- Integración con SQLAlchemy y Pandas.

---

## 🛠️ Requisitos

- Python 3.8+
- PostgreSQL
- Acceso a los datos con las tablas mencionadas en los reportes
- Archivo `.env` con credenciales de conexión

---

## 🔐 Variables de entorno (.env)

Debes crear un archivo `.env` con las siguientes variables:

```env
PG_USER=tu_usuario
PG_PASSWORD=tu_contraseña
PG_HOST=localhost
PG_PORT=5432
PG_DB=nombre_de_tu_base_de_datos
```

> ⚠️ Recuerda que este archivo está en `.gitignore` y **no debe subirse al repositorio**.

---

## 📦 Instalación


# Clonar el repositorio
```
git clone https://github.com/tuusuario/nombre-proyecto.git
```
cd nombre-proyecto

# Crear entorno virtual
```
python -m venv venv
```
source venv/bin/activate  # o venv\Scripts\activate en Windows

# Instalar dependencias
```
pip install -r requirements.txt
```

---

## ▶️ Uso

```bash
streamlit run app.py
```

La aplicación abrirá una interfaz web donde puedes seleccionar el tipo de reporte, aplicar filtros y descargar los resultados en Excel.

---

## 📁 Estructura del proyecto

```
.
├── app.py             # Script principal de Streamlit
├── .env               # Variables de conexión (no se sube al repo)
├── .gitignore         # Ignora archivos como .env y __pycache__
└── requirements.txt   # Dependencias del proyecto
```

---

## 📌 Reportes disponibles

### 1. Placas por Cliente (CINTAS)

Busca por número de cinta y muestra las placas facturadas por cliente.

### 2. Facturación con Seriales (SENIAT)

Consulta todas las facturas emitidas en un rango de fechas, por localidad (`PLM`, `PG8`, `BR1-PLM`, `BR2`).

### 3. Despachos (SENIAT)

Muestra los productos despachados en una fecha determinada, agrupados por zona.

---

## 🧪 Tecnologías utilizadas

* Python
* Streamlit
* Pandas
* SQLAlchemy
* psycopg2
* openpyxl
* python-dotenv

---

## 👨‍💻 Autor

**Hidelberg Efren Martinez Espitia**
Desarrollador Backend | Odoo | Python | PostgreSQL
[GitHub](https://github.com/hidel21)

