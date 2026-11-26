from pathlib import Path
import tomllib
import mysql.connector
import pandas as pd


def _obtener_config_db() -> dict:
    """Lee las credenciales de MySQL desde Streamlit secrets o el archivo local."""
    try:
        import streamlit as st
        if "mysql" in st.secrets:
            return dict(st.secrets["mysql"])
    except Exception:
        pass

    ruta_secrets = Path(__file__).resolve().parent.parent / ".streamlit" / "secrets.toml"
    if not ruta_secrets.exists():
        raise FileNotFoundError(
            "No se encontro .streamlit/secrets.toml ni secretos configurados."
        )

    with open(ruta_secrets, "rb") as archivo:
        datos = tomllib.load(archivo)
    return dict(datos["mysql"])


def obtener_conexion():
    """Abre y devuelve una conexion activa a MySQL."""
    cfg = _obtener_config_db()
    parametros = {
        "host": cfg["host"],
        "port": int(cfg.get("port", 3306)),
        "user": cfg["user"],
        "password": cfg["password"],
        "database": cfg["database"],
    }
    if cfg.get("ssl_ca"):
        parametros["ssl_ca"] = cfg["ssl_ca"]
    return mysql.connector.connect(**parametros)


def ejecutar_consulta(sql: str, params: tuple | None = None) -> pd.DataFrame:
    """Ejecuta una consulta SELECT y devuelve el resultado como DataFrame de Pandas."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(sql, params or ())
            filas = cursor.fetchall()
            return pd.DataFrame(filas)
        finally:
            cursor.close()
    finally:
        conexion.close()


if __name__ == "__main__":
    df_servicios = ejecutar_consulta("SELECT * FROM servicio;")
    print("Conexion exitosa a MySQL desde Python + Pandas.")
    print(df_servicios)
