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
```
* **Detección y aislamiento de valores nulos:** Durante la validación inicial del DataFrame, el script permitió identificar 11 registros con valores faltantes en la columna `Codigo_Postal` (correspondientes a la ciudad de Burlington). Esto se aisló en DataFrames específicos para su posterior imputación y corrección automática:

<img width="1183" height="955" alt="fotito 2" src="https://github.com/user-attachments/assets/082423f5-0534-499f-8b3d-ebbe40b181cf" />

---
### 2. Enriquecimiento y Transformación (Excel / Power Query)
Una vez exportado el archivo limpio desde Python, trabajé sobre el Excel para asegurar la correcta estructuración y formato de las celdas (moneda, fechas y tipos de datos), incorporando nuevas columnas calculadas hacia la derecha de la matriz (Año, Mes, Bimestre y Días de Envío) que facilitaron la agregación de datos para el reporte.

<img width="1891" height="1003" alt="fotito (agrego columnas)" src="https://github.com/user-attachments/assets/4b6c64f6-e017-4968-85db-daaeb850d0cb" />

### 3. Visualización y Dashboard (Looker Studio)
Con la base de datos totalmente depurada y enriquecida, diseñé un reporte interactivo en Looker Studio estructurado a través de un menú principal (Índice) que se divide en tres vistas analíticas principales:

* **Dashboard de Ventas:** Evolución temporal, composición de la facturación por categorías y comportamiento por bimestres.

* **Dashboard de Clientes:** Mapa de calor geográfico, distribución por regiones, evolución de la base activa y segmentación de cuentas principales.

* **Dashboard de Productos:** Unidades vendidas por categoría, tiempos de envío y distribución logística.

<img width="1600" height="900" alt="Dashboard" src="https://github.com/user-attachments/assets/cde9968a-6c00-44ce-86fc-67467160cf43" />

### 🔗 Enlace al Dashboard Interactivo
👉 **Hacer clic aquí para ver el Dashboard completo en Looker Studio**:https://datastudio.google.com/reporting/e79dd49d-d532-40f6-8af0-afcea7d978ff

### Principales Hallazgos (Insights)
* **Ventas:** Crecimiento anual sostenido con una marcada concentración de la facturación en el último cuatrimestre (51,6%), liderado por la categoría Furniture (48%). Se detectó una leve desaceleración en el ticket promedio.

* **Clientes:** Base activa en constante crecimiento (+8,66% interanual) con una cartera saludable y baja dependencia de cuentas grandes (el Top 1 representa solo el 2,2%).

* **Productos y Logística:** El método de envío Standard Class concentra la mayor cantidad de entregas con un promedio de 5 días, identificando picos de demanda importantes en los bimestres finales del año.

### Conclusiones y Recomendaciones de Negocio
* **Optimización de Stock:** Reforzar inventarios y campañas publicitarias antes del 5° y 6° bimestre para soportar el pico de demanda.

* **Estrategia de Fidelización:** Proteger al Top 10 de cuentas con un programa VIP y expandir esfuerzos de captación en regiones de menor volumen comercial (como la región South).

* **Venta Cruzada:** Impulsar promociones combinadas entre la categoría líder (Furniture) y las demás líneas de productos para equilibrar las ventas en el primer cuatrimestre.










