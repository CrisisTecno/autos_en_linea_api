from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request

catalogo_fl = Blueprint('catalogo', __name__)

async def process_catalogo_with_sucursal(connection):
    try:
        async with connection.cursor() as cursor:
            # Obtener registros de la tabla catalogo
            sql_catalogo = """SELECT id_catalogo, sucursal_id, auto_id, created, lastUpdate, lastInventoryUpdate, especificaciones, main_image, descripcion
                              FROM catalogo"""
            await cursor.execute(sql_catalogo)
            catalogo_results = await cursor.fetchall()

            # Procesar cada registro de la tabla catalogo
            for catalogo_record in catalogo_results:
                # Obtener información de la sucursal para cada registro
                auto_id=catalogo_record['auto_id']
                sucursal_id = catalogo_record['sucursal_id']
                auto_info=await get_auto(connection, auto_id)
                sucursal_info = await get_sucursal(connection, sucursal_id)
                # Agregar la información de la sucursal como un atributo adicional
                catalogo_record['sucursal_info'] = sucursal_info
                catalogo_record['auto_info'] = auto_info

            return catalogo_results
    finally:
        connection.close()

async def get_sucursal(connection, sucursal_id):
    try:
        async with connection.cursor() as cursor:
            # Obtener información de la sucursal
            sql_sucursal = """SELECT nombre FROM sucursal WHERE id_sucursal = %s"""
            await cursor.execute(sql_sucursal, (sucursal_id,))
            sucursal_info = await cursor.fetchone()

            return sucursal_info
    except Exception as e:
        print(f"Error obtaining sucursal info for ID {sucursal_id}: {e}")
        return None

async def get_auto(connection, auto_id):
    try:
        async with connection.cursor() as cursor:
            # Obtener información de la sucursal
            sql_auto = """SELECT marca, modelo,categoria_de_auto,anio,precio,kilometraje FROM auto WHERE id_auto = %s"""
            await cursor.execute(sql_auto, (auto_id,))
            sucursal_info = await cursor.fetchone()

            return sucursal_info
    except Exception as e:
        print(f"Error obtaining sucursal info for ID {auto_id}: {e}")
        return None
 


    
@catalogo_fl.route('/', methods=['GET'])
async def get_pedidos_proveedor():
    async with connect_to_database() as connection:
        try:
            # Obtener información de los pedidos del proveedor
            usuarios = await process_catalogo_with_sucursal(connection)
            return jsonify({"success": True, "data": usuarios})
        except Exception as e:
            return jsonify({"error": "Database error: {}".format(e)}), 500