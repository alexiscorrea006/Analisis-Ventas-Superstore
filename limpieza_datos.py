# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 13:36:48 2026

@author: Win10
"""

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

# Opcional: Asegurar que toda la columna sea de tipo entero (rellenando si existiera algún otro nulo residual)
df['Codigo_Postal'] = df['Codigo_Postal'].astype('Int64')

# 7. Exportar el DataFrame corregido a Excel
ruta_salida = r"C:\Users\Win10\Desktop\Esscritorio\Portafolio\Base_de_datos_corregida.xlsx"
df.to_excel(ruta_salida, index=False)

print("¡Archivo exportado con éxito con el código postal como entero!")
