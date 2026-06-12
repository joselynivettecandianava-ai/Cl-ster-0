import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

# ==========================
# CONEXION MONGODB ATLAS
# ==========================
URI = st.secrets["MONGO_URI"]
@st.cache_resource
def init_connection():
    return MongoClient(URI)
try:
    cliente = init_connection()
    db = cliente["test"]
    productos = db["productos"]
    clientes = db["clientes"]
    ventas = db["ventas"]
except Exception as e:
    st.error("Error al conectar con MongoDB: {e}")
# ==========================
# CONFIGURACION PAGINA
# ==========================
st.set_page_config(page_title="Tienda de Maquillaje", layout="wide")

st.title("💄 Sistema Tienda de Maquillaje")
st.write("Administración de Productos, Clientes y Ventas")

tab_productos, tab_clientes, tab_ventas = st.tabs(
    ["💄 Productos", "👩 Clientes", "🛒 Ventas"]
)

# =====================================================
# PRODUCTOS
# =====================================================
with tab_productos:

    st.header("Productos")

    p_ver, p_agregar, p_editar, p_eliminar = st.tabs(
        ["Ver", "Agregar", "Editar", "Eliminar"]
    )

    # VER
    with p_ver:

        docs = list(productos.find())

        if docs:
            for doc in docs:
                st.write(doc)
        else:
            st.info("No hay productos registrados")

    # AGREGAR
    with p_agregar:

        st.subheader("Agregar Producto")

        with st.form("form_producto"):

            idp = st.number_input("ID", min_value=1, step=1)

            nombre = st.text_input("Nombre")

            precio = st.number_input("Precio", min_value=0.0)

            stock = st.number_input("Stock", min_value=0)

            descripcion = st.text_area("Descripción")

            categoria = st.text_input("Categoría")

            proveedor = st.text_input("Proveedor")

            fecha_cad = st.date_input("Fecha Caducidad")

            guardar = st.form_submit_button("Guardar")

            if guardar:

                productos.insert_one({
                    "id": int(idp),
                    "nombre": nombre,
                    "precio": precio,
                    "stock": int(stock),
                    "descripcion": descripcion,
                    "categoria": categoria,
                    "proveedor": proveedor,
                    "fecha_caducidad": str(fecha_cad)
                })

                st.success("Producto agregado")
                st.rerun()

    # EDITAR
    with p_editar:

        docs = list(productos.find())

        if docs:

            opciones = {
                f"{x['id']} - {x['nombre']}": x
                for x in docs
            }

            seleccionado = st.selectbox(
                "Selecciona Producto",
                opciones.keys()
            )

            prod = opciones[seleccionado]

            nombre = st.text_input(
                "Nombre",
                value=prod.get("nombre", "")
            )

            precio = st.number_input(
                "Precio",
                value=float(prod.get("precio", 0))
            )

            stock = st.number_input(
                "Stock",
                value=int(prod.get("stock", 0))
            )

            descripcion = st.text_area(
                "Descripción",
                value=prod.get("descripcion", "")
            )

            categoria = st.text_input(
                "Categoría",
                value=prod.get("categoria", "")
            )

            proveedor = st.text_input(
                "Proveedor",
                value=prod.get("proveedor", "")
            )

            if st.button("Actualizar Producto"):

                productos.update_one(
                    {"_id": prod["_id"]},
                    {
                        "$set": {
                            "nombre": nombre,
                            "precio": precio,
                            "stock": int(stock),
                            "descripcion": descripcion,
                            "categoria": categoria,
                            "proveedor": proveedor
                        }
                    }
                )

                st.success("Producto actualizado")
                st.rerun()

    # ELIMINAR
    with p_eliminar:

        docs = list(productos.find())

        if docs:

            opciones = {
                f"{x['id']} - {x['nombre']}": x
                for x in docs
            }

            seleccionado = st.selectbox(
                "Producto a eliminar",
                opciones.keys(),
                key="del_producto"
            )

            prod = opciones[seleccionado]

            if st.button("Eliminar Producto"):

                productos.delete_one(
                    {"_id": prod["_id"]}
                )

                st.success("Producto eliminado")
                st.rerun()

# =====================================================
# CLIENTES
# =====================================================
with tab_clientes:

    st.header("Clientes")

    c_ver, c_agregar, c_editar, c_eliminar = st.tabs(
        ["Ver", "Agregar", "Editar", "Eliminar"]
    )

    # VER
    with c_ver:

        docs = list(clientes.find())

        if docs:
            for doc in docs:
                st.write(doc)

    # AGREGAR
    with c_agregar:

        with st.form("form_cliente"):

            idc = st.number_input(
                "ID Cliente",
                min_value=1,
                step=1
            )

            nombre = st.text_input("Nombre Cliente")

            edad = st.number_input(
                "Edad",
                min_value=1
            )

            telefono = st.text_input("Teléfono")

            correo = st.text_input("Correo")

            direccion = st.text_input("Dirección")

            genero = st.selectbox(
                "Género",
                ["Femenino", "Masculino"]
            )

            fecha_registro = st.date_input(
                "Fecha Registro"
            )

            guardar = st.form_submit_button(
                "Guardar Cliente"
            )

            if guardar:

                clientes.insert_one({
                    "id": int(idc),
                    "nombre": nombre,
                    "edad": int(edad),
                    "telefono": telefono,
                    "correo": correo,
                    "direccion": direccion,
                    "genero": genero,
                    "fecha_registro": str(fecha_registro)
                })

                st.success("Cliente agregado")
                st.rerun()

    # EDITAR
    with c_editar:

        docs = list(clientes.find())

        if docs:

            opciones = {
                f"{x['id']} - {x['nombre']}": x
                for x in docs
            }

            seleccionado = st.selectbox(
                "Selecciona Cliente",
                opciones.keys()
            )

            cli = opciones[seleccionado]

            nombre = st.text_input(
                "Nombre",
                value=cli.get("nombre", "")
            )

            edad = st.number_input(
                "Edad",
                value=int(cli.get("edad", 0))
            )

            telefono = st.text_input(
                "Teléfono",
                value=cli.get("telefono", "")
            )

            correo = st.text_input(
                "Correo",
                value=cli.get("correo", "")
            )

            direccion = st.text_input(
                "Dirección",
                value=cli.get("direccion", "")
            )

            genero = st.text_input(
                "Género",
                value=cli.get("genero", "")
            )

            if st.button("Actualizar Cliente"):

                clientes.update_one(
                    {"_id": cli["_id"]},
                    {
                        "$set": {
                            "nombre": nombre,
                            "edad": int(edad),
                            "telefono": telefono,
                            "correo": correo,
                            "direccion": direccion,
                            "genero": genero
                        }
                    }
                )

                st.success("Cliente actualizado")
                st.rerun()

    # ELIMINAR
    with c_eliminar:

        docs = list(clientes.find())

        if docs:

            opciones = {
                f"{x['id']} - {x['nombre']}": x
                for x in docs
            }

            seleccionado = st.selectbox(
                "Cliente a eliminar",
                opciones.keys(),
                key="cliente_eliminar"
            )

            cli = opciones[seleccionado]

            if st.button("Eliminar Cliente"):

                clientes.delete_one(
                    {"_id": cli["_id"]}
                )

                st.success("Cliente eliminado")
                st.rerun()

# =====================================================
# VENTAS
# =====================================================
with tab_ventas:

    st.header("Ventas")

    v_ver, v_agregar, v_editar, v_eliminar = st.tabs(
        ["Ver", "Agregar", "Editar", "Eliminar"]
    )

    # VER
    with v_ver:

        docs = list(ventas.find())

        if docs:
            for doc in docs:
                st.write(doc)

    # AGREGAR
    with v_agregar:

        with st.form("form_venta"):

            idv = st.number_input(
                "ID Venta",
                min_value=1,
                step=1
            )

            cliente_nombre = st.text_input(
                "Cliente"
            )

            producto_nombre = st.text_input(
                "Producto"
            )

            cantidad = st.number_input(
                "Cantidad",
                min_value=1
            )

            precio = st.number_input(
                "Precio",
                min_value=0.0
            )

            fecha = st.date_input("Fecha")

            metodo_pago = st.selectbox(
                "Método Pago",
                [
                    "Efectivo",
                    "Tarjeta",
                    "Transferencia"
                ]
            )

            guardar = st.form_submit_button(
                "Guardar Venta"
            )

            if guardar:

                ventas.insert_one({
                    "id": int(idv),
                    "cliente": cliente_nombre,
                    "producto": producto_nombre,
                    "cantidad": int(cantidad),
                    "precio": precio,
                    "total": cantidad * precio,
                    "fecha": str(fecha),
                    "metodo_pago": metodo_pago
                })

                st.success("Venta registrada")
                st.rerun()

    # EDITAR
    with v_editar:

        docs = list(ventas.find())

        if docs:

            opciones = {
                f"{x['id']} - {x['cliente']}": x
                for x in docs
            }

            seleccionado = st.selectbox(
                "Selecciona Venta",
                opciones.keys()
            )

            ven = opciones[seleccionado]

            cliente_nombre = st.text_input(
                "Cliente",
                value=ven.get("cliente", "")
            )

            producto_nombre = st.text_input(
                "Producto",
                value=ven.get("producto", "")
            )

            cantidad = st.number_input(
                "Cantidad",
                value=int(ven.get("cantidad", 1))
            )

            precio = st.number_input(
                "Precio",
                value=float(ven.get("precio", 0))
            )

            metodo_pago = st.text_input(
                "Método Pago",
                value=ven.get("metodo_pago", "")
            )

            if st.button("Actualizar Venta"):

                ventas.update_one(
                    {"_id": ven["_id"]},
                    {
                        "$set": {
                            "cliente": cliente_nombre,
                            "producto": producto_nombre,
                            "cantidad": int(cantidad),
                            "precio": precio,
                            "total": cantidad * precio,
                            "metodo_pago": metodo_pago
                        }
                    }
                )

                st.success("Venta actualizada")
                st.rerun()

    # ELIMINAR
    with v_eliminar:

        docs = list(ventas.find())

        if docs:

            opciones = {
                f"{x['id']} - {x['cliente']}": x
                for x in docs
            }

            seleccionado = st.selectbox(
                "Venta a eliminar",
                opciones.keys(),
                key="venta_eliminar"
            )

            ven = opciones[seleccionado]

            if st.button("Eliminar Venta"):

                ventas.delete_one(
                    {"_id": ven["_id"]}
                )

                st.success("Venta eliminada")
                st.rerun()
