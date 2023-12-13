from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request
from .usuario_id import usuario_fl1
from .usuario_methods import usuario_fl2

usuario_fl = Blueprint('usuario', __name__)
usuario_fl.register_blueprint(usuario_fl1,)
usuario_fl.register_blueprint(usuario_fl2,)

async def process_usuario(connection):
    try:
        async with connection.cursor() as cursor:
            # Obtener registros de la tabla catalogo
            sql_sucursal = """SELECT id_usuario,
              nombres, apellidos, direccion, gerente,url_logo,
              url_link_web,direccion,
              num_telefono,created,lastUpdate,
              id_sucursal, correo_electronico,coordenadas
                FROM usuario;"""
            await cursor.execute(sql_sucursal)
            usuario_results = await cursor.fetchall()
            
            return usuario_results
    finally:
        connection.close()


    
@usuario_fl.route('/', methods=['GET'])
async def get_pedidos_proveedor():
    async with connect_to_database() as connection:
        try:
            # Obtener información de los pedidos del proveedor
            usuarios = await process_usuario(connection)
            return jsonify({"success": True, "data": usuarios})
        except Exception as e:
            return jsonify({"error": "Database error: {}".format(e)}), 500