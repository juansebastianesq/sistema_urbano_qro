import pandas as pd
import streamlit as st


def mostrar_fuentes_metodologia(
    df_fuentes: pd.DataFrame,
    df_indicadores: pd.DataFrame,
    df_datos_servicios: pd.DataFrame,
):
    st.title("Fuentes y metodología")
    st.markdown(
        "Consulta el origen documental de cada registro cargado en el sistema, "
        "el estado de disponibilidad de todos los indicadores y los criterios "
        "metodológicos utilizados para el análisis y el simulador."
    )

    # 1. Fuentes oficiales
    st.subheader("1. Catálogo de fuentes oficiales")
    if df_fuentes.empty:
        st.warning("No hay fuentes registradas en la base de datos.")
    else:
        df_f = df_fuentes.copy()
        instituciones = ["Todas"] + sorted(
            df_f["institucion"].dropna().unique().tolist()
        )
        inst_elegida = st.selectbox(
            "Filtrar por institución:",
            options=instituciones,
        )
        if inst_elegida != "Todas":
            df_f = df_f[df_f["institucion"] == inst_elegida]

        tabla_fuentes = df_f[
            ["institucion", "nombre_documento", "fecha_consulta", "url"]
        ].rename(
            columns={
                "institucion": "Institución",
                "nombre_documento": "Documento o referencia",
                "fecha_consulta": "Fecha de consulta",
                "url": "Enlace oficial",
            }
        )
        st.dataframe(
            tabla_fuentes,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Enlace oficial": st.column_config.LinkColumn(
                    "Enlace oficial", display_text="Abrir enlace"
                ),
            },
        )

    st.divider()

    # 2. Inventario de indicadores y cobertura de anios
    st.subheader("2. Inventario de indicadores, unidades y años disponibles")
    if df_indicadores.empty:
        st.warning("No hay indicadores definidos en la base de datos.")
    else:
        anios_por_ind = {}
        if not df_datos_servicios.empty:
            df_tmp = df_datos_servicios.dropna(subset=["id_indicador", "anio"]).copy()
            df_tmp["anio"] = df_tmp["anio"].astype(int)
            for id_ind, grupo in df_tmp.groupby("id_indicador"):
                anios_ordenados = sorted(grupo["anio"].unique().tolist())
                anios_por_ind[int(id_ind)] = ", ".join(str(a) for a in anios_ordenados)

        df_inv = df_indicadores.copy()
        df_inv["anios_cargados"] = df_inv["id_indicador"].map(
            lambda x: anios_por_ind.get(int(x), "Sin datos cargados")
        )
        df_inv["estado"] = df_inv["registros_disponibles"].map(
            lambda n: "Con datos oficiales" if int(n) > 0 else "Información no disponible"
        )

        tabla_inv = df_inv[
            [
                "servicio",
                "indicador",
                "unidad",
                "estado",
                "anios_cargados",
                "descripcion",
            ]
        ].rename(
            columns={
                "servicio": "Servicio",
                "indicador": "Indicador",
                "unidad": "Unidad",
                "estado": "Estado",
                "anios_cargados": "Años registrados",
                "descripcion": "Descripción",
            }
        )
        st.dataframe(tabla_inv, use_container_width=True, hide_index=True)

    st.divider()

    # 3. Metodologia y transparencia
    st.subheader("3. Metodología y criterios de transparencia")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            **Datos observados vs. estimaciones**
            * Las secciones **Inicio**, **Análisis poblacional** y **Análisis de servicios urbanos** muestran exclusivamente cifras oficiales cargadas en la base de datos `sistema_urbano_qro`.
            * Cuando un año o indicador no cuenta con información oficial registrada, se marca como **no disponible**; el sistema nunca inventa ni rellena datos faltantes.
            * Únicamente la sección **Simulador de escenarios** genera cifras estimadas de carácter ilustrativo a partir de los parámetros elegidos por el usuario.
            """
        )
    with col2:
        st.markdown(
            """
            **Fórmulas utilizadas**
            * **Variación porcentual:** $((V_{\\text{final}} - V_{\\text{inicial}}) / V_{\\text{inicial}}) \\times 100$
            * **Tasa de Crecimiento Media Anual (TCMA):** $((P_{\\text{final}} / P_{\\text{inicial}})^{1/n} - 1) \\times 100$, donde $n$ es la diferencia en años.
            * **Simulador proporcional ilustrativo:** $V_{\\text{estimado}} = V_{\\text{base}} \\times (1 + r/100)$, donde $r$ es el porcentaje de crecimiento hipotético.
            """
        )

    st.info(
        "Arquitectura del sistema: Base de datos relacional en MySQL (8 tablas), "
        "procesamiento y limpieza con Python + Pandas, visualizaciones interactivas "
        "con Plotly e interfaz web en Streamlit."
    )
