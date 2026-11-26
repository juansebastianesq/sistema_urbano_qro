import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def mostrar_simulador(df_poblacion: pd.DataFrame, df_datos_servicios: pd.DataFrame):
    st.title("Simulador de escenarios")
    st.markdown(
        "Explora cómo un crecimiento poblacional hipotético en el municipio de Querétaro "
        "podría incrementar la población total y la demanda ilustrativa de un servicio urbano."
    )

    if df_poblacion.empty:
        st.warning(
            "No hay registros de población disponibles en la base de datos para ejecutar el simulador."
        )
        return

    df_pob = df_poblacion.dropna(subset=["anio", "poblacion_total"]).copy()
    df_pob["anio"] = df_pob["anio"].astype(int)
    df_pob["poblacion_total"] = df_pob["poblacion_total"].astype(int)
    df_pob = df_pob.sort_values("anio").reset_index(drop=True)

    # Preparar indicadores numericos escalables (se excluyen porcentajes de cobertura)
    df_ref = pd.DataFrame()
    if not df_datos_servicios.empty:
        df_tmp = df_datos_servicios.dropna(subset=["anio", "valor"]).copy()
        df_tmp["anio"] = df_tmp["anio"].astype(int)
        df_tmp["valor"] = df_tmp["valor"].astype(float)
        es_porcentaje = (
            df_tmp["unidad"].fillna("").str.lower().str.contains("porcentaje|%")
        )
        df_escalables = df_tmp[~es_porcentaje].copy()
        if not df_escalables.empty:
            # Se toma el dato oficial mas reciente de cada indicador como referencia
            df_ref = (
                df_escalables.sort_values("anio")
                .groupby(["servicio", "indicador", "unidad"], as_index=False)
                .last()
                .sort_values(["servicio", "indicador"])
                .reset_index(drop=True)
            )

    st.subheader("1. Configura los parámetros del escenario")

    col_cfg1, col_cfg2, col_cfg3 = st.columns([1.4, 1.2, 1.0])

    with col_cfg1:
        opciones_pob = [
            f"{int(fila['anio'])} — {int(fila['poblacion_total']):,} habitantes"
            for _, fila in df_pob.iterrows()
        ]
        indice_pob = st.selectbox(
            "Población base (dato censal observado):",
            options=range(len(opciones_pob)),
            format_func=lambda i: opciones_pob[i],
            index=len(opciones_pob) - 1,
        )
        fila_pob_base = df_pob.iloc[indice_pob]
        anio_base = int(fila_pob_base["anio"])
        pob_base = int(fila_pob_base["poblacion_total"])

    with col_cfg2:
        crecimiento_pct = st.slider(
            "Crecimiento poblacional hipotético (%):",
            min_value=0,
            max_value=50,
            value=15,
            step=1,
            help="Porcentaje acumulado hipotético respecto a la población base elegida.",
        )

    with col_cfg3:
        anio_default = max(2030, anio_base + 10)
        anio_proyectado = st.number_input(
            "Año futuro de referencia:",
            min_value=anio_base + 1,
            max_value=2060,
            value=anio_default,
            step=1,
        )

    # Selector del servicio/indicador de referencia
    fila_serv_ref = None
    if not df_ref.empty:
        etiquetas_ref = [
            f"{fila['servicio']} — {fila['indicador']} (base {int(fila['anio'])})"
            for _, fila in df_ref.iterrows()
        ]
        indice_ref = st.selectbox(
            "Servicio e indicador de referencia para estimar demanda:",
            options=range(len(etiquetas_ref)),
            format_func=lambda i: etiquetas_ref[i],
        )
        fila_serv_ref = df_ref.iloc[indice_ref]
        st.caption(
            "Nota técnica: solo se muestran indicadores de volumen o demanda (no porcentajes "
            "de cobertura), ya que escalar un porcentaje proporcionalmente podría superar el 100%."
        )
    else:
        st.info(
            "Por ahora no hay indicadores de volumen/demanda cargados para simular; "
            "se calculará únicamente la proyección poblacional."
        )

    # Calculos del escenario
    factor = 1.0 + (crecimiento_pct / 100.0)
    pob_estimada = round(pob_base * factor)
    pob_adicional = pob_estimada - pob_base
    anios_horizonte = int(anio_proyectado) - anio_base
    tcma_implicita = (
        ((pob_estimada / pob_base) ** (1.0 / anios_horizonte) - 1.0) * 100.0
        if anios_horizonte > 0 and pob_base > 0
        else 0.0
    )

    st.divider()
    st.subheader("2. Resultados del escenario simulado")

    if fila_serv_ref is not None:
        valor_base_serv = float(fila_serv_ref["valor"])
        unidad_serv = str(fila_serv_ref["unidad"])
        nombre_serv = str(fila_serv_ref["servicio"])
        nombre_ind = str(fila_serv_ref["indicador"])
        anio_serv = int(fila_serv_ref["anio"])

        demanda_estimada = valor_base_serv * factor
        demanda_adicional = demanda_estimada - valor_base_serv

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric(
                label=f"Población estimada ({int(anio_proyectado)})",
                value=f"{pob_estimada:,} hab.",
                delta=f"+{pob_adicional:,} hab. (+{crecimiento_pct}%)",
            )
        with m2:
            st.metric(
                label="Tasa anual implícita (TCMA)",
                value=f"{tcma_implicita:.2f}%",
                help=f"Ritmo anual equivalente en un horizonte de {anios_horizonte} años.",
            )
        with m3:
            st.metric(
                label=f"Referencia actual ({anio_serv})",
                value=f"{valor_base_serv:,.2f}",
                help=f"{nombre_ind} ({unidad_serv})",
            )
        with m4:
            st.metric(
                label="Demanda estimada",
                value=f"{demanda_estimada:,.2f}",
                delta=f"+{demanda_adicional:,.2f} {unidad_serv}",
            )
    else:
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(
                label=f"Población base ({anio_base})",
                value=f"{pob_base:,} hab.",
            )
        with m2:
            st.metric(
                label=f"Población estimada ({int(anio_proyectado)})",
                value=f"{pob_estimada:,} hab.",
                delta=f"+{pob_adicional:,} hab. (+{crecimiento_pct}%)",
            )
        with m3:
            st.metric(
                label="Tasa anual implícita (TCMA)",
                value=f"{tcma_implicita:.2f}%",
            )

    # Graficas comparativas lado a lado
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        fig_pob = go.Figure(
            data=[
                go.Bar(
                    x=[f"Base ({anio_base})", f"Escenario ({int(anio_proyectado)})"],
                    y=[pob_base, pob_estimada],
                    marker_color=["#64748B", "#1D4ED8"],
                    text=[f"{pob_base:,}", f"{pob_estimada:,}"],
                    textposition="outside",
                    hovertemplate="<b>%{x}</b><br>%{y:,} habitantes<extra></extra>",
                )
            ]
        )
        fig_pob.update_layout(
            title="Comparación de población (habitantes)",
            yaxis_title="Habitantes",
            yaxis=dict(range=[0, max(pob_base, pob_estimada) * 1.2], tickformat=","),
            margin=dict(t=55, b=40),
        )
        st.plotly_chart(fig_pob, use_container_width=True)

    with col_graf2:
        if fila_serv_ref is not None:
            fig_serv = go.Figure(
                data=[
                    go.Bar(
                        x=[f"Referencia ({anio_serv})", f"Escenario (+{crecimiento_pct}%)"],
                        y=[valor_base_serv, demanda_estimada],
                        marker_color=["#64748B", "#0284C7"],
                        text=[f"{valor_base_serv:,.2f}", f"{demanda_estimada:,.2f}"],
                        textposition="outside",
                        hovertemplate=(
                            f"<b>%{{x}}</b><br>%{{y:,.2f}} {unidad_serv}<extra></extra>"
                        ),
                    )
                ]
            )
            fig_serv.update_layout(
                title=f"Demanda ilustrativa: {nombre_ind}",
                yaxis_title=unidad_serv,
                yaxis=dict(
                    range=[0, max(valor_base_serv, demanda_estimada) * 1.2],
                    tickformat=",",
                ),
                margin=dict(t=55, b=40),
            )
            st.plotly_chart(fig_serv, use_container_width=True)
        else:
            st.info("Agrega indicadores de volumen/demanda en la base para graficar su proyección.")

    # Tabla descargable del escenario
    filas_resumen = [
        {
            "Concepto": "Población del municipio",
            "Año base": anio_base,
            "Valor base": float(pob_base),
            "Crecimiento aplicado (%)": crecimiento_pct,
            "Año proyectado": int(anio_proyectado),
            "Valor estimado": float(pob_estimada),
            "Incremento": float(pob_adicional),
            "Unidad": "Habitantes",
        }
    ]
    if fila_serv_ref is not None:
        filas_resumen.append(
            {
                "Concepto": f"{nombre_serv} — {nombre_ind}",
                "Año base": anio_serv,
                "Valor base": round(valor_base_serv, 2),
                "Crecimiento aplicado (%)": crecimiento_pct,
                "Año proyectado": int(anio_proyectado),
                "Valor estimado": round(demanda_estimada, 2),
                "Incremento": round(demanda_adicional, 2),
                "Unidad": unidad_serv,
            }
        )

    df_resumen = pd.DataFrame(filas_resumen)
    st.markdown("**Resumen del escenario calculado**")
    st.dataframe(df_resumen, use_container_width=True, hide_index=True)

    csv_bytes = df_resumen.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Descargar escenario en CSV",
        data=csv_bytes,
        file_name=f"escenario_qro_{anio_base}_a_{int(anio_proyectado)}_{crecimiento_pct}pct.csv",
        mime="text/csv",
    )

    st.warning(
        "**Aviso metodológico:** Demostración simplificada que supone que la demanda cambia "
        "proporcionalmente a la población. No es un pronóstico oficial ni un cálculo definitivo "
        "de capacidad de infraestructura."
    )
