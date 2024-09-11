# Paycode Dashboard

## Descripción
Este proyecto es un dashboard desarrollado para Paycode. Proporciona una interfaz visual interactiva para analizar datos transaccionales, información de clientes y métricas clave del negocio. 

## Características
* Visualización de métricas clave como clientes activos, adquirentes activos, tasa de churn y volumen transaccional.
* Gráficos interactivos que muestran:
  - Distribución de comercios por zona
  - Transacciones a lo largo del tiempo
  - Volumen transaccional por banco emisor
  - Monto total transaccionado por comercio o por MCC
  - Días desde la última transacción por cliente 
  - Distribución de tipos de tarjeta (débito/crédito)
* Filtros dinámicos para analizar datos y volumen transaccional por nombre de cliente, MCC, estado activo y año.
* Tabla de datos filtrable con información detallada de clientes.

## Tecnologías Utilizadas
* Python 3
* Dash
* Plotly
* Pandas
* MySQL Connector
* Dash Bootstrap Components

## Estructura del Proyecto
* app.py: Archivo principal que contiene la lógica de la aplicación Dash.
* data_analysis.py: Módulo para la conexión a la base de datos y las funciones para jalar datos de la BD.
* queries.py: Contiene las SQL queries utilizadas en el proyecto (en data_analysis.py)
* config.py: Archivo de configuración para la conexión a la base de datos (no incluido en el repositorio por seguridad).
* packages.md: Lista de dependencias/packages del proyecto.

## Uso
Para iniciar la aplicación, ejecuta:
python app.py
La aplicación iniciará en http://localhost:8050 (o el puerto que se configure).