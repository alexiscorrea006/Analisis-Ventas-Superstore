# 📊 Análisis de Rendimiento Comercial y Geográfico (Super Store)

## Introducción

En este proyecto, desarrollé una solución integral de análisis de datos y Business Intelligence para evaluar el historial de ventas de Superstore —obtenido de un repositorio público de datos de la industria minorista—. 

El propósito central fue procesar este volumen masivo de transacciones comerciales, identificar patrones de estacionalidad y tendencia, y estructurar un flujo completo que abarcó: la detección y corrección de valores nulos e inconsistencias mediante **Python (Pandas)**, la transformación y enriquecimiento del dataset utilizando **Power Query y Excel**, y finalmente el desarrollo de un panel de control interactivo en **Looker Studio (Data Studio)** dividido en vistas de Ventas, Clientes y Productos para optimizar la toma de decisiones comerciales y de inventario.

---

## Tecnologías y Habilidades
* **Tecnologías:** Python (Pandas, NumPy), Excel, Power Query, Looker Studio, GitHub.
* **Habilidades:** Limpieza de datos (Data Cleaning), tratamiento de nulos, estructuración de bases de datos, análisis exploratorio (EDA), visualización de datos y diseño de paneles de control (Dashboards).

---

## Inspiración
Buscaba potenciar mis habilidades analíticas enfrentándome a un escenario real de negocio con miles de registros transaccionales. Quería responder preguntas clave sobre el rendimiento comercial: ¿Cuáles son las regiones y ciudades más rentables? ¿Cómo se comporta la demanda a lo largo del año? ¿Qué categorías de productos y tipos de envío dominan las operaciones para poder proponer mejoras estratégicas basadas en datos?

---

## Identificación de Requisitos y Metodología (ETL)

Para lograr un análisis confiable, estructuré el proyecto en las siguientes etapas técnicas detalladas:

### 1. Extracción y Limpieza de Datos con Python
Antes de llevar la información al dashboard, utilicé un script en **Python (Pandas y NumPy)** para cargar la base de datos cruda, eliminar duplicados, limpiar espacios en blanco en los campos de texto, unificar formatos de fecha y solucionar valores nulos (como los códigos postales faltantes en ciertas ciudades).

* **Script de Python utilizado:**
```python
import pandas as pd
import numpy as np

# 1. Cargar datos
ruta = r"C:\Users\Win10\Desktop\Esscritorio\Portafolio\Base de datos _ SuperStore.xlsx"
df = pd.read_excel(ruta)

# 2. Limpieza de nombres de columnas
df.columns = df.columns.str.strip().str.replace(' ', '_')

# 3. Formatos de datos
df['Fecha_de_pedido'] = pd.to_datetime(df['Fecha_de_pedido'])
df['Fecha_de_envio'] = pd.to_datetime(df['Fecha_de_envio'])
df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce')

# 4. Limpieza de texto y duplicados
df = df.drop_duplicates()

columnas_texto = ['Cliente', 'Segmento', 'Pais', 'Ciudad', 'Estado', 'Region', 'Categoria', 'Sub-Categoria']
for col in columnas_texto:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# 5. Creación de variables (Tiempo/Bimestres)
df['Año_Pedido'] = df['Fecha_de_pedido'].dt.year
df['Mes_Numero'] = df['Fecha_de_pedido'].dt.month
df['Mes_Nombre'] = df['Fecha_de_pedido'].dt.strftime('%B')
df['Bimestre'] = np.ceil(df['Fecha_de_pedido'].dt.month / 2).astype(int)
df['Dias_Envio'] = (df['Fecha_de_envio'] - df['Fecha_de_pedido']).dt.days

# 6. Imputación del Código Postal como entero (int)
df.loc[df['Ciudad'] == 'Burlington', 'Codigo_Postal'] = 5401
df['Codigo_Postal'] = df['Codigo_Postal'].astype('Int64')

# 7. Exportar el DataFrame corregido a Excel
ruta_salida = r"C:\Users\Win10\Desktop\Esscritorio\Portafolio\Base_de_datos_corregida.xlsx"
df.to_excel(ruta_salida, index=False)
