from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request
from .distribuidor_id import distribuidor_fl1
# from api.sucursal.sucursal_id import get_sucursal_for_distribuidor

distribuidor_fl = Blueprint('distribuidor', __name__)
distribuidor_fl.register_blueprint(distribuidor_fl1,)
async def process_distribuidor(connection):
    try:
        async with connection.cursor() as cursor:
            # Obtener registros de la tabla catalogo
            sql_distribuidor = """SELECT id_usuario,
              nombres, apellidos, direccion, gerente,url_logo,url_link_web,direccion,
              num_telefono,created,lastUpdate,
              id_sucursal, correo_electronico
                FROM usuario
                WHERE rol = 'Distribuidor';"""
            await cursor.execute(sql_distribuidor)
            distribuidor_results = await cursor.fetchall()
            # Procesar cada registro de distribuidor
            for distribuidor_record in distribuidor_results:
                # Obtener información de las sucursales vinculadas al distribuidor
                id_usuario = distribuidor_record['id_usuario']
                sql_sucursales = """SELECT sucursal.*
                                    FROM sucursal
                                    JOIN distribuidor_sucursal ON sucursal.id_sucursal = distribuidor_sucursal.id_sucursal
                                    WHERE distribuidor_sucursal.id_usuario = %s"""
                await cursor.execute(sql_sucursales, (id_usuario,))
                sucursal_list = await cursor.fetchall()

                # Agregar la lista de sucursales como un atributo adicional
                distribuidor_record['sucursal_list'] = sucursal_list
            return distribuidor_results
    finally:
        connection.close()


    
@distribuidor_fl.route('/', methods=['GET'])
async def get_distribuidor():
    async with connect_to_database() as connection:
        try:
            # Obtener información de los pedidos del proveedor
            distribuidor = await process_distribuidor(connection)
            return jsonify({"success": True, "data": distribuidor})
        except Exception as e:
            return jsonify({"error": "Database error: {}".format(e)}), 500