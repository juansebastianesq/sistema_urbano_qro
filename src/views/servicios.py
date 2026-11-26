import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def mostrar_analisis_servicios(
    df_servicios: pd.DataFrame,
    cargar_indicadores_fn,
    cargar_datos_servicios_fn,
):
    st.title("Análisis de servicios urbanos")
    st.markdown(
        "Selecciona uno de los seis servicios urbanos para consultar sus indicadores "
        "disponibles, visualizar los datos históricos y verificar qué indicadores "
        "aún no cuentan con información oficial registrada."
    )

    if df_servicios.empty:
        st.warning("No hay servicios registrados en la base de datos.")
        return

    # Selector de servicio urbano
    nombres_servicios = df_servicios["servicio"].tolist()
    servicio_elegido = st.selectbox(
        "Selecciona un servicio urbano:",
        options=nombres_servicios,
    )

    fila_servicio = df_servicios[df_servicios["servicio"] == servicio_elegido].iloc[0]
    id_servicio = int(fila_servicio["id_servicio"])
    descripcion_servicio = fila_servicio["descripcion"] or "Sin descripción registrada."

    st.info(f"**{servicio_elegido}:** {descripcion_servicio}")

    df_indicadores = cargar_indicadores_fn(id_servicio)
    df_datos = cargar_datos_servicios_fn(id_servicio)

    total_ind = len(df_indicadores)
    con_datos_df = df_indicadores[df_indicadores["registros_disponibles"] > 0]
    sin_datos_df = df_indicadores[df_indicadores["registros_disponibles"] == 0]

    # Tarjetas resumen del servicio seleccionado
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Indicadores definidos", total_ind)
    with col2:
        st.metric("Con datos registrados", len(con_datos_df))
    with col3:
        st.metric("Sin datos disponibles", len(sin_datos_df))
    with col4:
        st.metric("Registros totales", len(df_datos))

    st.divider()

    # Seccion 1: Visualizacion de indicadores con datos
    st.subheader("Indicadores con datos disponibles")
    if df_datos.empty or con_datos_df.empty:
        st.warning(
            f"Actualmente no hay mediciones numéricas cargadas para **{servicio_elegido}**. "
            "El sistema no genera ni inventa valores faltantes."
        )
    else:
        df_datos_limpio = df_datos.dropna(subset=["anio", "valor"]).copy()
        df_datos_limpio["anio"] = df_datos_limpio["anio"].astype(int)
        df_datos_limpio["valor"] = df_datos_limpio["valor"].astype(float)

        indicadores_con_datos = con_datos_df["indicador"].tolist()
        indicador_elegido = st.selectbox(
            "Elige un indicador para graficar:",
            options=indicadores_con_datos,
        )

        df_ind = (
            df_datos_limpio[df_datos_limpio["indicador"] == indicador_elegido]
            .sort_values("anio")
            .reset_index(drop=True)
        )
        unidad = df_ind["unidad"].iloc[0] if not df_ind.empty else ""

        # Metricas rapidas del indicador elegido
        if len(df_ind) >= 2:
            primero = df_ind.iloc[0]
            ultimo = df_ind.iloc[-1]
            cambio = float(ultimo["valor"]) - float(primero["valor"])
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(
                    label=f"Valor en {int(primero['anio'])}",
                    value=f"{primero['valor']:,.2f}",
                    help=f"Unidad: {unidad}",
                )
            with m2:
                st.metric(
                    label=f"Valor en {int(ultimo['anio'])}",
                    value=f"{ultimo['valor']:,.2f}",
                    delta=f"{cambio:+,.2f} ({unidad})",
                )
            with m3:
                st.metric(
                    label="Unidad de medida",
                    value=unidad,
                )
        elif len(df_ind) == 1:
            unico = df_ind.iloc[0]
            m1, m2 = st.columns(2)
            with m1:
                st.metric(
                    label=f"Valor registrado ({int(unico['anio'])})",
                    value=f"{unico['valor']:,.2f}",
                )
            with m2:
                st.metric(
                    label="Unidad de medida",
                    value=unidad,
                )

        # Grafica interactiva en Plotly respetando la unidad del indicador
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=df_ind["anio"].astype(str),
                y=df_ind["valor"],
                name=indicador_elegido,
                marker_color="#0284C7",
                text=df_ind["valor"].map(lambda v: f"{v:,.2f}"),
                textposition="outside",
                hovertemplate=(
                    "<b>Año %{x}</b><br>"
                    f"{indicador_elegido}: %{{y:,.2f}} {unidad}<extra></extra>"
                ),
            )
        )
        if len(df_ind) >= 2:
            fig.add_trace(
                go.Scatter(
                    x=df_ind["anio"].astype(str),
                    y=df_ind["valor"],
                    mode="lines+markers",
                    name="Evolución",
                    line=dict(color="#0F172A", width=2.5),
                    marker=dict(size=8),
                    hoverinfo="skip",
                )
            )

        max_val = float(df_ind["valor"].max()) if not df_ind.empty else 1.0
        limite_superior = max_val * 1.2 if max_val > 0 else 10
        if unidad.strip().lower() == "porcentaje" and limite_superior < 110:
            limite_superior = 110

        fig.update_layout(
            title=f"{indicador_elegido} ({unidad})",
            xaxis_title="Año",
            yaxis_title=unidad,
            yaxis=dict(range=[0, limite_superior]),
            margin=dict(t=55, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Tabla completa de todos los registros del servicio seleccionado
        st.markdown("**Registros oficiales cargados para este servicio**")
        tabla_datos = df_datos_limpio[
            [
                "indicador",
                "anio",
                "valor",
                "unidad",
                "observaciones",
                "fuente_institucion",
                "fuente_url",
            ]
        ].rename(
            columns={
                "indicador": "Indicador",
                "anio": "Año",
                "valor": "Valor",
                "unidad": "Unidad",
                "observaciones": "Observaciones",
                "fuente_institucion": "Fuente",
                "fuente_url": "Enlace",
            }
        )

        st.dataframe(
            tabla_datos,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Valor": st.column_config.NumberColumn(format="%.2f"),
                "Enlace": st.column_config.LinkColumn("Enlace", display_text="Ver fuente"),
            },
        )

    st.divider()

    # Seccion 2: Transparencia sobre indicadores sin datos cargados
    st.subheader("Indicadores definidos sin datos cargados todavía")
    if sin_datos_df.empty:
        st.success(
            f"Todos los indicadores definidos para **{servicio_elegido}** "
            "cuentan con al menos un registro oficial en la base de datos."
        )
    else:
        st.caption(
            "Los siguientes indicadores existen en el diseño de la base de datos, "
            "pero aún no tienen cifras oficiales registradas:"
        )
        tabla_sin_datos = sin_datos_df[
            ["indicador", "unidad", "descripcion"]
        ].rename(
            columns={
                "indicador": "Indicador",
                "unidad": "Unidad esperada",
                "descripcion": "Descripción",
            }
        )
        st.dataframe(tabla_sin_datos, use_container_width=True, hide_index=True)
