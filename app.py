import plotly.graph_objects as go
import streamlit as st
from src.queries import (
    obtener_datos_servicios,
    obtener_fuentes,
    obtener_indicadores,
    obtener_poblacion,
    obtener_resumen_general,
    obtener_servicios,
)
from src.views.fuentes import mostrar_fuentes_metodologia
from src.views.poblacion import mostrar_analisis_poblacional
from src.views.servicios import mostrar_analisis_servicios
from src.views.simulador import mostrar_simulador

st.set_page_config(
    page_title="Sistema de Analisis Urbano - Queretaro",
    page_icon="🏙️",
    layout="wide",
)


@st.cache_data(ttl=300)
def cargar_resumen():
    return obtener_resumen_general()


@st.cache_data(ttl=300)
def cargar_poblacion():
    return obtener_poblacion()


@st.cache_data(ttl=300)
def cargar_servicios():
    return obtener_servicios()


@st.cache_data(ttl=300)
def cargar_indicadores(id_servicio=None):
    return obtener_indicadores(id_servicio)


@st.cache_data(ttl=300)
def cargar_datos_servicios(id_servicio=None):
    return obtener_datos_servicios(id_servicio)


@st.cache_data(ttl=300)
def cargar_fuentes():
    return obtener_fuentes()


def mostrar_inicio():
    st.title("Sistema de Análisis Urbano: Municipio de Querétaro")
    st.markdown(
        "Plataforma interactiva para explorar la evolución poblacional del municipio "
        "de Querétaro y su relación con la disponibilidad de datos en seis servicios urbanos."
    )

    resumen = cargar_resumen()
    df_poblacion = cargar_poblacion()
    df_servicios = cargar_servicios()

    ultimo_anio = None
    ultima_pob = None
    delta_pob = None
    if not df_poblacion.empty:
        ultima_fila = df_poblacion.iloc[-1]
        ultimo_anio = int(ultima_fila["anio"])
        ultima_pob = int(ultima_fila["poblacion_total"])
        if len(df_poblacion) >= 2:
            penultima_fila = df_poblacion.iloc[-2]
            pob_anterior = int(penultima_fila["poblacion_total"])
            anio_anterior = int(penultima_fila["anio"])
            if pob_anterior > 0:
                crecimiento_pct = ((ultima_pob - pob_anterior) / pob_anterior) * 100
                delta_pob = f"+{crecimiento_pct:.1f}% vs {anio_anterior}"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label=f"Población registrada ({ultimo_anio})" if ultimo_anio else "Población",
            value=f"{ultima_pob:,}" if ultima_pob is not None else "Sin dato",
            delta=delta_pob,
        )
    with col2:
        st.metric(
            label="Servicios urbanos",
            value=resumen["total_servicios"],
        )
    with col3:
        st.metric(
            label="Indicadores con datos",
            value=f"{resumen['indicadores_con_datos']} / {resumen['total_indicadores']}",
        )
    with col4:
        st.metric(
            label="Registros y fuentes",
            value=f"{resumen['total_registros_servicio']} datos",
            delta=f"{resumen['total_fuentes']} fuentes oficiales",
            delta_color="off",
        )

    st.divider()

    st.subheader("Panorama de los servicios urbanos")
    if df_servicios.empty:
        st.warning("No hay servicios registrados en la base de datos.")
        return

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name="Indicadores definidos",
            x=df_servicios["servicio"],
            y=df_servicios["total_indicadores"],
            marker_color="#94A3B8",
        )
    )
    fig.add_trace(
        go.Bar(
            name="Indicadores con dato disponible",
            x=df_servicios["servicio"],
            y=df_servicios["indicadores_con_datos"],
            marker_color="#1D4ED8",
        )
    )
    fig.update_layout(
        barmode="group",
        title="Cobertura de indicadores por servicio urbano",
        xaxis_title="Servicio urbano",
        yaxis_title="Cantidad de indicadores",
        legend_title="Estado",
        margin=dict(t=50, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)

    tabla_servicios = df_servicios.rename(
        columns={
            "servicio": "Servicio urbano",
            "descripcion": "Descripción",
            "total_indicadores": "Indicadores definidos",
            "indicadores_con_datos": "Indicadores con datos",
            "total_registros": "Registros cargados",
        }
    )[
        [
            "Servicio urbano",
            "Descripción",
            "Indicadores definidos",
            "Indicadores con datos",
            "Registros cargados",
        ]
    ]
    st.dataframe(tabla_servicios, use_container_width=True, hide_index=True)

    st.info(
        "Nota de transparencia: el sistema muestra exclusivamente los registros "
        "documentados en la base de datos. Cuando un indicador o año no cuenta con "
        "información oficial cargada, se indica explícitamente sin estimar cifras."
    )


def main():
    st.sidebar.title("Navegación")
    st.sidebar.caption("Municipio de Querétaro")

    seccion = st.sidebar.radio(
        "Selecciona una sección:",
        [
            "Inicio - Panel general",
            "Análisis poblacional",
            "Análisis de servicios urbanos",
            "Simulador de escenarios",
            "Fuentes y metodología",
        ],
    )

    try:
        if seccion == "Inicio - Panel general":
            mostrar_inicio()
        elif seccion == "Análisis poblacional":
            mostrar_analisis_poblacional(cargar_poblacion())
        elif seccion == "Análisis de servicios urbanos":
            mostrar_analisis_servicios(
                cargar_servicios(),
                cargar_indicadores,
                cargar_datos_servicios,
            )
        elif seccion == "Simulador de escenarios":
            mostrar_simulador(
                cargar_poblacion(),
                cargar_datos_servicios(),
            )
        elif seccion == "Fuentes y metodología":
            mostrar_fuentes_metodologia(
                cargar_fuentes(),
                cargar_indicadores(),
                cargar_datos_servicios(),
            )
    except Exception as exc:
        st.error(
            "No fue posible conectar con la base de datos MySQL. "
            "Verifica que el servicio esté activo y que las credenciales sean correctas."
        )
        st.exception(exc)


if __name__ == "__main__":
    main()
