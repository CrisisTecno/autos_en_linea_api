from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request
from .usuario_id import usuario_fl1
from .usuario_methods import usuario_fl2
import datetime

usuario_fl = Blueprint('usuario', __name__)
usuario_fl.register_blueprint(usuario_fl1,)
usuario_fl.register_blueprint(usuario_fl2,)

async def process_usuario(connection):
    try:
        async with connection.cursor() as cursor:
            sql_sucursal = """SELECT * FROM usuario;"""
            await cursor.execute(sql_sucursal)
            usuario_results = await cursor.fetchall()
            
            for usuario_record in usuario_results:
                for key, value in usuario_record.items():
                    if isinstance(value, datetime.datetime):
                        usuario_record[key] = int(value.timestamp() * 1000)
            return usuario_results
    finally:
        connection.close()

@usuario_fl2.route('/favoritos/<string:id_usuario>', methods=['GET'])
async def obtener_todos_autos_favoritos_usuario(id_usuario): 
    try:
        async with connect_to_database() as connection:
            async with connection.cursor() as cursor:
                sql = """
                    SELECT articulo.*, favoritos.enable as favorite FROM articulo
                    JOIN favoritos ON articulo.id_articulo = favoritos.id_articulo
                """
                await cursor.execute(sql)
                autos_favoritos = await cursor.fetchall()
                if not autos_favoritos:
                    return jsonify({"error": f"No se encontraron autos favoritos para el usuario con ID {id_usuario}"}), 404



                return jsonify({"success": True, "autos_favoritos": autos_favoritos}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    

    
@usuario_fl.route('/', methods=['GET'])
async def get_pedidos_proveedor():
    async with connect_to_database() as connection:
        try:
            usuarios = await process_usuario(connection)
            return jsonify({"success": True, "data": usuarios})
        except Exception as e:
            return jsonify({"error": "Database error: {}".format(e)}), 500