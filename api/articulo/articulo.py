from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request
from .articulo_id import articulo_fl1
from .articulo_methods import articulo_fl2


articulo_fl = Blueprint('articulo', __name__)

articulo_fl.register_blueprint(articulo_fl1,)
articulo_fl.register_blueprint(articulo_fl2,)

async def get_articulos(connection):
    try:
        async with connection.cursor() as cursor:
            # Obtener registros de la tabla catalogo
            sql_articulo = """SELECT * FROM articulo"""
            await cursor.execute(sql_articulo)
            articulo_results = await cursor.fetchall()
            return articulo_results
    finally:
        connection.close()


    
@articulo_fl.route('/', methods=['GET'])
async def get_articulos_all():
    async with connect_to_database() as connection:
        try:
            # Obtener información de los pedidos del proveedor
            articulo = await get_articulos(connection)
            return jsonify({"success": True, "data": articulo})
        except Exception as e:
            return jsonify({"error": "Database error: {}".format(e)}), 500