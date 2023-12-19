import datetime
from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request
from .sucursal_id import sucursal_fl1
from .sucursal_methods import sucursal_fl2
from .images_sucursal import images_sucursal_fl2
sucursal_fl = Blueprint('sucursal', __name__)


sucursal_fl.register_blueprint(sucursal_fl1)
sucursal_fl.register_blueprint(sucursal_fl2)
sucursal_fl.register_blueprint(images_sucursal_fl2)

async def process_sucursal(connection):
    try:
        async with connection.cursor() as cursor:
            sql_sucursal = """SELECT * FROM sucursal;"""
            await cursor.execute(sql_sucursal)
            sucursal_results = await cursor.fetchall()

            for sucursal_record in sucursal_results:

                for key, value in sucursal_record.items():
                    if isinstance(value, datetime.datetime):
                        sucursal_record[key] = int(value.timestamp() * 1000)
                id_sucursal = sucursal_record['id_sucursal']

                sql_sucursales_imagenes = """SELECT * FROM images_sucursal
                                             WHERE id_sucursal = %s;"""
                await cursor.execute(sql_sucursales_imagenes, (id_sucursal,))
                sucursal_images = await cursor.fetchall()
                sucursal_record['sucursal_images'] = sucursal_images

                sql_articulos = """SELECT articulo.ano,articulo.categoria, articulo.color,articulo.created,articulo.descripcion,
                articulo.enable,articulo.id_articulo,
                articulo.kilometraje,articulo.lastInventoryUpdate,articulo.lastUpdate,articulo.mainImage,
                articulo.marca,articulo.modelo,articulo.precio
                FROM articulo 
                                   JOIN articulo_sucursal ON articulo.id_articulo = articulo_sucursal.id_articulo
                                   WHERE articulo_sucursal.id_sucursal = %s;"""
                await cursor.execute(sql_articulos, (id_sucursal,))
                articulos_list = await cursor.fetchall()
                for articulos in articulos_list:
                    for key, value in articulos.items():
                        if isinstance(value, datetime.datetime):
                            articulos[key] = int(value.timestamp() * 1000)

                sucursal_record['sucursal_articulos'] = articulos_list

            return sucursal_results
    finally:
        connection.close()



    
@sucursal_fl.route('/', methods=['GET'])
async def get_sucursal_all():
    async with connect_to_database() as connection:
        try:
            # Obtener información de los pedidos del proveedor
            sucursales = await process_sucursal(connection)
            return jsonify({"success": True, "data": sucursales})
        except Exception as e:
            return jsonify({"error": "Database error: {}".format(e)}), 500