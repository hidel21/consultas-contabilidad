import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from io import BytesIO
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Crear engine SQLAlchemy
def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DB')}"
    )

# Ejecutar consulta SQL
def run_query(query, params=None):
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn, params=params)
    return df

# Generar archivo Excel desde DataFrame
def generate_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output

# Configuración de la app
st.set_page_config(page_title="Reportes Bera", layout="centered")
st.title("📊 Generador de Reportes - Bera Motorcycles")

# Selector de tipo de reporte
option = st.selectbox("Selecciona el tipo de reporte", [
    "Placas por Cliente (CINTAS)",
    "Facturación con Seriales (SENIAT)",
    "Despachos (SENIAT)"
])

# Reporte: Placas por Cliente (CINTAS)
if option == "Placas por Cliente (CINTAS)":
    cinta = st.text_input("🔍 Número de Cinta", value="0005890")

    if st.button("Generar Reporte"):
        query = """
        SELECT
            T5.name AS NroFactura,
            T3.name AS Placa,
            T6.name AS Cliente,
            T6.vat AS Rif,
            T6.street AS Direccion,
            T6.phone AS Telefono,
            T6."x_studio_char_field_FHICm" AS Responsable,
            T7.name AS Ciudad
        FROM cintas_bera T1
        JOIN stock_lot T2 ON T1.id = T2.cinta_id
        JOIN stock_lot T3 ON T2.matricula_id = T3.id
        JOIN cintas_bera_line T4 ON T2.id = T4.lot_id
        JOIN account_move T5 ON T4.invoice_id = T5.id
        JOIN res_partner T6 ON T5.partner_id = T6.id
        JOIN res_country_state T7 ON T6.state_id = T7.id
        WHERE T1.name = %s
        ORDER BY T3.name;
        """
        df = run_query(query, (cinta,))
        st.dataframe(df)
        file_name = f"Placas_por_Cliente_CINTA_{cinta}.xlsx"
        st.download_button("⬇️ Descargar Excel", data=generate_excel(df), file_name=file_name)

# Reporte: Facturación con Seriales (SENIAT)
elif option == "Facturación con Seriales (SENIAT)":
    col1, col2 = st.columns(2)
    with col1:
        fecha_inicio = st.date_input("📅 Fecha inicio")
    with col2:
        fecha_fin = st.date_input("📅 Fecha fin")

    localidad = st.selectbox("🏙️ Localidad", ["PLM", "PG8", "BR1-PLM","BR2"])

    if st.button("Generar Reporte"):
        # Determinar longitud de prefijo según localidad
        if localidad == "BR1-PLM":
            sql_prefix = "LEFT(T1.name, 7) = %s"
        else:
            sql_prefix = "LEFT(T1.name, 3) = %s"

        query = f"""
        SELECT
            T1.name AS NroFactura,
            T1.invoice_date AS Fecha,
            T4.vat AS Rif,
            T1.invoice_partner_display_name AS Cliente,
            T2.name AS Producto,
            T2.price_unit_ref AS PrecioBs,
            T3.name AS Chasis,
            T3.serial_motor AS Motor
        FROM account_move T1
        JOIN account_move_line T2 ON T1.id = T2.move_id
        JOIN stock_lot T3 ON T2.stock_lot_id = T3.id
        JOIN res_partner T4 ON T2.partner_id = T4.id
        WHERE 
            T1.invoice_date BETWEEN %s AND %s
            AND T1.invoice_type_account = 'facturado'
            AND {sql_prefix}
            AND T2.price_unit > 0
        ORDER BY T1.name;
        """

        df = run_query(query, (
            fecha_inicio.strftime("%Y-%m-%d"),
            fecha_fin.strftime("%Y-%m-%d"),
            localidad
        ))
        st.dataframe(df)
        file_name = f"Facturacion_SENIAT_{localidad}_{fecha_inicio.strftime('%Y%m%d')}_{fecha_fin.strftime('%Y%m%d')}.xlsx"
        st.download_button("⬇️ Descargar Excel", data=generate_excel(df), file_name=file_name)

# Reporte: Despachos (SENIAT)
elif option == "Despachos (SENIAT)":
    fecha = st.date_input("📦 Fecha de Despacho")
    localidad = st.selectbox("🏙️ Localidad", ["PLM", "PG8"])

    if st.button("Generar Reporte"):
        query = """
        SELECT
            T1.name AS Despacho,
            T1.date_done AS Fecha,
            T2.vat AS Rif,
            T2.name AS Cliente,
            T4.name_for_setu AS Producto,
            T5.name AS Chasis,
            T5.serial_motor AS Motor,
            T7.name AS Zona
        FROM stock_picking T1
        JOIN res_partner T2 ON T1.partner_id = T2.id
        JOIN stock_move_line T3 ON T1.id = T3.picking_id
        JOIN product_product T4 ON T3.product_id = T4.id
        JOIN stock_lot T5 ON T3.lot_id = T5.id
        JOIN guide_consolidate_line T6 ON T1.id = T6.picking_id
        JOIN res_country_state T7 ON T6.zona = T7.id
        WHERE 
            T1.date_done BETWEEN %s AND %s
            AND T1.dispatch_status = 'dispatched'
            AND LEFT(T1.name, 3) = %s
        ORDER BY T1.name;
        """
        date_start = fecha.strftime("%Y-%m-%d 00:00:01")
        date_end = fecha.strftime("%Y-%m-%d 23:59:59")
        df = run_query(query, (date_start, date_end, localidad))
        st.dataframe(df)
        file_name = f"Despachos_SENIAT_{localidad}_{fecha.strftime('%Y-%m-%d')}.xlsx"
        st.download_button("⬇️ Descargar Excel", data=generate_excel(df), file_name=file_name)
