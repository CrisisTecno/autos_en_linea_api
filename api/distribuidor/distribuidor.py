from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request
from .distribuidor_id import distribuidor_fl1
from .distribuidor_methods import distribuidor_fl2
# from api.sucursal.sucursal_id import get_sucursal_for_distribuidor

distribuidor_fl = Blueprint('distribuidor', __name__)
distribuidor_fl.register_blueprint(distribuidor_fl1,)
distribuidor_fl.register_blueprint(distribuidor_fl2,)

async def process_distribuidor(connection):
    try:
        async with connection.cursor() as cursor:
            sql_distribuidor = "SELECT * FROM distribuidor"
            await cursor.execute(sql_distribuidor)
            distribuidores = await cursor.fetchall()

            for distribuidor in distribuidores:
                id_distribuidor = distribuidor['id_distribuidor']
                sql_sucursales = """
                    SELECT s.* FROM sucursal s
                    JOIN distribuidor_sucursal ds ON s.id_sucursal = ds.id_sucursal
                    WHERE ds.id_distribuidor = %s
                """
                await cursor.execute(sql_sucursales, (id_distribuidor,))
                sucursales = await cursor.fetchall()
                distribuidor['sucursales'] = sucursales

            return distribuidores
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