import pandas as pd
from src.db import ejecutar_consulta


def obtener_resumen_general() -> dict:
    """Devuelve los conteos principales de la base de datos."""
    sql = """
    SELECT
        (SELECT COUNT(*) FROM servicio) AS total_servicios,
        (SELECT COUNT(*) FROM indicador_servicio) AS total_indicadores,
        (SELECT COUNT(DISTINCT id_indicador) FROM dato_servicio) AS indicadores_con_datos,
        (SELECT COUNT(*) FROM dato_servicio) AS total_registros_servicio,
        (SELECT COUNT(*) FROM poblacion) AS registros_poblacion,
        (SELECT COUNT(*) FROM fuente_dato) AS total_fuentes;
    """
    df = ejecutar_consulta(sql)
    if df.empty:
        return {
            "total_servicios": 0,
            "total_indicadores": 0,
            "indicadores_con_datos": 0,
            "total_registros_servicio": 0,
            "registros_poblacion": 0,
            "total_fuentes": 0,
        }
    fila = df.iloc[0]
    return {clave: int(fila[clave]) for clave in df.columns}


def obtener_poblacion() -> pd.DataFrame:
    """Obtiene los registros historicos de poblacion ordenados por anio."""
    sql = """
    SELECT
        p.id_poblacion,
        m.nombre AS municipio,
        m.estado,
        a.anio,
        p.poblacion_total,
        f.institucion AS fuente_institucion,
        f.nombre_documento AS fuente_documento,
        f.url AS fuente_url
    FROM poblacion p
    INNER JOIN municipio m ON p.id_municipio = m.id_municipio
    INNER JOIN anio a ON p.id_anio = a.id_anio
    INNER JOIN fuente_dato f ON p.id_fuente = f.id_fuente
    ORDER BY a.anio ASC;
    """
    df = ejecutar_consulta(sql)
    if not df.empty:
        df["anio"] = pd.to_numeric(df["anio"], errors="coerce").astype("Int64")
        df["poblacion_total"] = pd.to_numeric(
            df["poblacion_total"], errors="coerce"
        ).astype("Int64")
    return df


def obtener_servicios() -> pd.DataFrame:
    """Obtiene los servicios urbanos y cuantos indicadores/registros tiene cada uno."""
    sql = """
    SELECT
        s.id_servicio,
        s.nombre AS servicio,
        s.descripcion,
        COUNT(DISTINCT i.id_indicador) AS total_indicadores,
        COUNT(DISTINCT ds.id_indicador) AS indicadores_con_datos,
        COUNT(ds.id_dato) AS total_registros
    FROM servicio s
    LEFT JOIN indicador_servicio i ON s.id_servicio = i.id_servicio
    LEFT JOIN dato_servicio ds ON i.id_indicador = ds.id_indicador
    GROUP BY s.id_servicio, s.nombre, s.descripcion
    ORDER BY s.id_servicio ASC;
    """
    df = ejecutar_consulta(sql)
    if not df.empty:
        for col in ["total_indicadores", "indicadores_con_datos", "total_registros"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    return df


def obtener_indicadores(id_servicio: int | None = None) -> pd.DataFrame:
    """Obtiene todos los indicadores definidos, indicando si tienen datos o no."""
    sql = """
    SELECT
        i.id_indicador,
        s.id_servicio,
        s.nombre AS servicio,
        i.nombre AS indicador,
        i.unidad,
        i.descripcion,
        COUNT(ds.id_dato) AS registros_disponibles
    FROM indicador_servicio i
    INNER JOIN servicio s ON i.id_servicio = s.id_servicio
    LEFT JOIN dato_servicio ds ON i.id_indicador = ds.id_indicador
    """
    params = ()
    if id_servicio is not None:
        sql += " WHERE s.id_servicio = %s"
        params = (int(id_servicio),)
    sql += """
    GROUP BY i.id_indicador, s.id_servicio, s.nombre, i.nombre, i.unidad, i.descripcion
    ORDER BY s.id_servicio ASC, i.id_indicador ASC;
    """
    df = ejecutar_consulta(sql, params)
    if not df.empty:
        df["registros_disponibles"] = (
            pd.to_numeric(df["registros_disponibles"], errors="coerce")
            .fillna(0)
            .astype(int)
        )
    return df


def obtener_datos_servicios(id_servicio: int | None = None) -> pd.DataFrame:
    """Obtiene los valores numericos registrados de los servicios urbanos."""
    sql = """
    SELECT
        ds.id_dato,
        s.id_servicio,
        s.nombre AS servicio,
        i.id_indicador,
        i.nombre AS indicador,
        i.unidad,
        a.anio,
        ds.valor,
        ds.observaciones,
        f.institucion AS fuente_institucion,
        f.nombre_documento AS fuente_documento,
        f.url AS fuente_url
    FROM dato_servicio ds
    INNER JOIN indicador_servicio i ON ds.id_indicador = i.id_indicador
    INNER JOIN servicio s ON i.id_servicio = s.id_servicio
    INNER JOIN anio a ON ds.id_anio = a.id_anio
    INNER JOIN fuente_dato f ON ds.id_fuente = f.id_fuente
    """
    params = ()
    if id_servicio is not None:
        sql += " WHERE s.id_servicio = %s"
        params = (int(id_servicio),)
    sql += " ORDER BY s.id_servicio ASC, i.id_indicador ASC, a.anio ASC;"

    df = ejecutar_consulta(sql, params)
    if not df.empty:
        df["anio"] = pd.to_numeric(df["anio"], errors="coerce").astype("Int64")
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    return df


def obtener_fuentes() -> pd.DataFrame:
    """Obtiene el catalogo completo de fuentes oficiales documentadas."""
    sql = """
    SELECT
        id_fuente,
        institucion,
        nombre_documento,
        url,
        fecha_consulta
    FROM fuente_dato
    ORDER BY id_fuente ASC;
    """
    return ejecutar_consulta(sql)


if __name__ == "__main__":
    print("=== Resumen general ===")
    print(obtener_resumen_general())
    print("\n=== Poblacion ===")
    print(obtener_poblacion()[["municipio", "anio", "poblacion_total"]])
    print("\n=== Servicios ===")
    print(obtener_servicios()[["servicio", "total_indicadores", "indicadores_con_datos", "total_registros"]])
