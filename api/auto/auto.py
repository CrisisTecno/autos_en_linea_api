from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request
from .auto_id import auto_fl1
auto_fl = Blueprint('auto', __name__)

auto_fl.register_blueprint(auto_fl1,)

async def get_autos(connection):
    try:
        async with connection.cursor() as cursor:
            # Obtener registros de la tabla catalogo
            sql_auto = """SELECT id_auto,disponibilidad,
            marca, modelo,categoria_de_auto,anio,precio,especificaciones,sucursal_id,
            kilometraje FROM auto"""
            await cursor.execute(sql_auto)
            auto_results = await cursor.fetchall()
            return auto_results
    finally:
        connection.close()


    
@auto_fl.route('/', methods=['GET'])
async def get_autos_all():
    async with connect_to_database() as connection:
        try:
            # Obtener información de los pedidos del proveedor
            auto = await get_autos(connection)
            return jsonify({"success": True, "data": auto})
        except Exception as e:
            return jsonify({"error": "Database error: {}".format(e)}), 500