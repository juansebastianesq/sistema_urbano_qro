from pathlib import Path
import tomllib
import mysql.connector
import pandas as pd


def cargar_config_db() -> dict:
    """Lee las credenciales de MySQL desde st.secrets o .streamlit/secrets.toml."""
    try:
        import streamlit as st

        if "mysql" in st.secrets:
            return dict(st.secrets["mysql"])
    except Exception:
        pass

    ruta_secrets = Path(__file__).resolve().parent.parent / ".streamlit" / "secrets.toml"
    if not ruta_secrets.exists():
        raise FileNotFoundError(
            "No se encontro .streamlit/secrets.toml ni st.secrets['mysql']."
        )

    with open(ruta_secrets, "rb") as archivo:
        datos = tomllib.load(archivo)
    return dict(datos["mysql"])


def obtener_conexion():
    """Abre y devuelve una conexion a MySQL (local o nube con SSL)."""
    cfg = cargar_config_db()
    opciones = {
        "host": cfg["host"],
        "port": int(cfg.get("port", 3306)),
        "user": cfg["user"],
        "password": cfg["password"],
        "database": cfg["database"],
        "connection_timeout": 15,
    }
    if cfg.get("ssl", False):
        opciones["ssl_disabled"] = False
        opciones["ssl_verify_cert"] = False
    return mysql.connector.connect(**opciones)


def ejecutar_consulta(sql: str, params=None) -> pd.DataFrame:
    """Ejecuta una consulta SELECT y devuelve un DataFrame de Pandas."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        filas = cursor.fetchall()
        return pd.DataFrame(filas)
    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    df = ejecutar_consulta("SHOW TABLES;")
    print("Conexion exitosa. Tablas encontradas:")
    print(df)
