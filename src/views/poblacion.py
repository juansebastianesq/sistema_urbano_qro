import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def mostrar_analisis_poblacional(df_poblacion: pd.DataFrame):
    st.title("Análisis poblacional")
    st.markdown(
        "Explora la evolución demográfica registrada del municipio de Querétaro "
        "y compara el crecimiento entre los años censales disponibles."
    )

    if df_poblacion.empty:
        st.warning("No hay registros de población disponibles en la base de datos.")
        return

    df = df_poblacion.dropna(subset=["anio", "poblacion_total"]).copy()
    df["anio"] = df["anio"].astype(int)
    df["poblacion_total"] = df["poblacion_total"].astype(int)
    df = df.sort_values("anio").reset_index(drop=True)

    anios_disponibles = df["anio"].tolist()

    # Selector de consulta por anio individual o comparacion de periodos
    st.subheader("Comparación entre periodos")
    if len(anios_disponibles) >= 2:
        col_sel1, col_sel2 = st.columns(2)
        with col_sel1:
            anio_inicio = st.selectbox(
                "Año base (inicial):",
                options=anios_disponibles,
                index=0,
            )
        with col_sel2:
            anio_fin = st.selectbox(
                "Año de comparación (final):",
                options=anios_disponibles,
                index=len(anios_disponibles) - 1,
            )

        pob_inicio = int(df.loc[df["anio"] == anio_inicio, "poblacion_total"].iloc[0])
        pob_fin = int(df.loc[df["anio"] == anio_fin, "poblacion_total"].iloc[0])

        diferencia = pob_fin - pob_inicio
        variacion_pct = (diferencia / pob_inicio) * 100 if pob_inicio > 0 else 0.0
        anios_transcurridos = anio_fin - anio_inicio

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                label=f"Población en {anio_inicio}",
                value=f"{pob_inicio:,}",
            )
        with col2:
            st.metric(
                label=f"Población en {anio_fin}",
                value=f"{pob_fin:,}",
            )
        with col3:
            signo = "+" if diferencia >= 0 else ""
            st.metric(
                label="Cambio absoluto",
                value=f"{signo}{diferencia:,} hab.",
                delta=f"{signo}{variacion_pct:.2f}%",
            )
        with col4:
            if anios_transcurridos > 0 and pob_inicio > 0 and pob_fin > 0:
                tasa_anual = ((pob_fin / pob_inicio) ** (1 / anios_transcurridos) - 1) * 100
                st.metric(
                    label="Tasa anual promedio (TCMA)",
                    value=f"{tasa_anual:.2f}%",
                    help="Tasa de Crecimiento Media Anual calculada entre los dos años elegidos.",
                )
            else:
                st.metric(
                    label="Tasa anual promedio (TCMA)",
                    value="N/A",
                    help="Selecciona un año final mayor al año base para calcular la tasa anual.",
                )

        if anio_inicio >= anio_fin:
            st.info(
                "Para ver el crecimiento cronológico y la tasa anual promedio, "
                "elige un año final mayor al año base."
            )
    else:
        unica_fila = df.iloc[0]
        st.metric(
            label=f"Población registrada ({int(unica_fila['anio'])})",
            value=f"{int(unica_fila['poblacion_total']):,}",
        )
        st.info("Se necesitan al menos dos años registrados para comparar periodos.")

    st.divider()

    # Grafica interactiva de evolucion poblacional
    st.subheader("Evolución histórica registrada")
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df["anio"].astype(str),
            y=df["poblacion_total"],
            name="Población total",
            marker_color="#1D4ED8",
            text=df["poblacion_total"].map(lambda x: f"{x:,}"),
            textposition="outside",
            hovertemplate="<b>Año %{x}</b><br>Población: %{y:,} habitantes<extra></extra>",
        )
    )
    if len(df) >= 2:
        fig.add_trace(
            go.Scatter(
                x=df["anio"].astype(str),
                y=df["poblacion_total"],
                mode="lines+markers",
                name="Tendencia",
                line=dict(color="#0F172A", width=3),
                marker=dict(size=9),
                hoverinfo="skip",
            )
        )

    max_pob = int(df["poblacion_total"].max())
    fig.update_layout(
        title="Población total registrada en el municipio de Querétaro",
        xaxis_title="Año censal",
        yaxis_title="Habitantes",
        yaxis=dict(range=[0, max_pob * 1.18], tickformat=","),
        legend_title="Serie",
        margin=dict(t=60, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Tabla detallada con trazabilidad de fuentes
    st.subheader("Detalle de registros y fuentes oficiales")
    tabla = df[
        [
            "municipio",
            "estado",
            "anio",
            "poblacion_total",
            "fuente_institucion",
            "fuente_documento",
            "fuente_url",
        ]
    ].rename(
        columns={
            "municipio": "Municipio",
            "estado": "Estado",
            "anio": "Año",
            "poblacion_total": "Población total",
            "fuente_institucion": "Institución",
            "fuente_documento": "Documento fuente",
            "fuente_url": "Enlace oficial",
        }
    )

    st.dataframe(
        tabla,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Población total": st.column_config.NumberColumn(format="%d"),
            "Enlace oficial": st.column_config.LinkColumn("Enlace oficial", display_text="Abrir fuente"),
        },
    )

    st.caption(
        "Solo se muestran los años con registro oficial cargado en la base de datos; "
        "los años intermedios no censales no se interpolan ni se inventan en esta sección."
    )
