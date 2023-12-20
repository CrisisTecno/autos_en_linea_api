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


    
@usuario_fl.route('/', methods=['GET'])
async def get_pedidos_proveedor():
    async with connect_to_database() as connection:
        try:
            usuarios = await process_usuario(connection)
            return jsonify({"success": True, "data": usuarios})
        except Exception as e:
            return jsonify({"error": "Database error: {}".format(e)}), 500