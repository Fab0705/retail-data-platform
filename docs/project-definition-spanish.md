# PROBLEMA DE NEGOCIO
Una empresa de retail con presencia en múltiples países necesita entender su desempeño comercial y analizar cómo este se relaciona con el contexto macroeconómico de cada región. Actualmente, los datos transaccionales están aislados y carecen de una fuente centralizada, automatizada y confiable que los integre con indicadores económicos externos para facilitar la toma de decisiones directivas.

# OBJETIVOS
* Desarrollar una plataforma de datos (Data Platform) de extremo a extremo que consolide los datos transaccionales sintéticos de retail con indicadores económicos reales provenientes de la API del Banco Mundial.
* Transformar, validar y almacenar esta información en un modelo analítico relacional (Star Schema) alojado en PostgreSQL.
* Exponer los datos modelados a través de Power BI para habilitar el análisis comercial y económico.

# PREGUNTAS DE NEGOCIO
**Comerciales:**
* ¿Cuál es el ingreso total (revenue) a lo largo del tiempo?
* ¿Qué productos generan la mayor cantidad de ingresos?
* ¿Qué países y tiendas tienen el mejor rendimiento?
* ¿Cuál es el valor promedio de la orden (Average Order Value)?

**De Clientes:**
* ¿Cuántos clientes se mantienen activos?
* ¿Cuál es el ingreso generado por cliente?
* ¿Qué segmentos de clientes generan el mayor valor para el negocio?

**Contexto Económico:**
* ¿Cómo varía el entorno económico (ej. PIB, inflación, desempleo) por país a lo largo del tiempo?
* ¿Coinciden las tendencias de crecimiento en ventas con los cambios en los indicadores macroeconómicos externos?

# ALCANCE
* Generación programática de datos transaccionales sintéticos (ventas, clientes, productos, tiendas) usando Python.
* Extracción automatizada de datos económicos utilizando la API del Banco Mundial, implementando paginación.
* Desarrollo de un pipeline ETL en Python que incluya limpieza, normalización y validación de reglas de negocio (Data Quality).
* Diseño e implementación de un modelo dimensional (Star Schema con tablas Fact y Dim) en PostgreSQL.
* Desarrollo de lógica para cargas incrementales (upserts) en la base de datos.
* Creación de un modelo semántico y dashboard interactivo en Power BI.

# FUERA DE ALCANCE
* Procesamiento y analítica de datos en tiempo real (streaming). El sistema operará mediante cargas por lotes (batch processing) planificadas.
* Desarrollo de modelos predictivos o algoritmos de Machine Learning.
* Construcción de aplicaciones web o interfaces de usuario transaccionales para la captura manual de datos.

# SALIDAS ESPERADAS
* Un repositorio de GitHub estructurado profesionalmente, incluyendo documentación de arquitectura técnica (diagramas) y decisiones (DECISIONS.md).
* Una base de datos PostgreSQL desplegada localmente mediante Docker, poblada con datos consistentes.
* Scripts modulares en Python con pruebas unitarias e integración continua básica.
* Un reporte en Power BI con vistas ejecutivas separadas para rendimiento comercial y contexto económico.