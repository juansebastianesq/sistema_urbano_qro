# Sistema de Análisis Urbano: Municipio de Querétaro

Plataforma web interactiva para consultar la evolución poblacional del municipio de Querétaro y analizar la disponibilidad de indicadores en seis servicios urbanos, conectada a una base de datos relacional MySQL en la nube.

**Aplicación publicada:** https://sistema-urbano-queretaro.streamlit.app/

## Secciones de la aplicación

1. **Inicio - Panel general:** indicadores principales del municipio y gráfica comparativa de cobertura por servicio urbano.
2. **Análisis poblacional:** evolución histórica censal, tasas de crecimiento y variación porcentual.
3. **Análisis de servicios urbanos:** consulta filtrada por servicio e indicador, señalando de forma transparente qué años tienen registros oficiales y cuáles no cuentan con dato disponible.
4. **Simulador de escenarios:** proyección ilustrativa de población y demanda proporcional de servicios (excluyendo porcentajes de cobertura), con exportación a CSV.
5. **Fuentes y metodología:** catálogo de fuentes oficiales con enlaces directos, inventario de los 17 indicadores y fórmulas utilizadas.

## Arquitectura y tecnologías

* **Base de datos:** MySQL 8 (8 tablas normalizadas: `municipio`, `anio`, `poblacion`, `servicio`, `indicador_servicio`, `dato_servicio`, `fuente_dato` y `proyeccion`), alojada en Aiven for MySQL con conexión SSL.
* **Procesamiento y análisis:** Python y Pandas.
* **Visualización:** Plotly.
* **Interfaz y despliegue:** Streamlit y Streamlit Community Cloud.

## Estructura del proyecto

```text
sistema_urbano_qro/
├── app.py                  # Punto de entrada y navegación principal
├── requirements.txt        # Dependencias del proyecto
└── src/
    ├── db.py               # Conexión segura a MySQL (local y nube con SSL)
    ├── queries.py          # Consultas SQL estructuradas
    └── views/
        ├── poblacion.py    # Vista de análisis poblacional
        ├── servicios.py    # Vista de análisis de servicios urbanos
        ├── simulador.py    # Vista del simulador de escenarios
        └── fuentes.py      # Vista de fuentes oficiales y metodología
```

## Ejecución local

1. Clona el repositorio y crea un entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Crea el archivo `.streamlit/secrets.toml` con tus credenciales de MySQL:
   ```toml
   [mysql]
   host = "localhost"
   port = 3306
   user = "TU_USUARIO"
   password = "TU_PASSWORD"
   database = "sistema_urbano_qro"
   ssl = false
   ```
3. Inicia la aplicación:
   ```bash
   streamlit run app.py
   ```

## Nota metodológica

Las secciones descriptivas muestran exclusivamente cifras oficiales cargadas en la base de datos sin rellenar valores faltantes. Únicamente el **Simulador de escenarios** genera estimaciones ilustrativas con fines didácticos.
