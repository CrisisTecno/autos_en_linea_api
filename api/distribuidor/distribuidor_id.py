from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request

distribuidor_fl1=Blueprint('distribuidor_id', __name__)


async def process_distribuidor_por_id(connection, id_distribuidor):
    try:
        async with connection.cursor() as cursor:
            sql_distribuidor = "SELECT * FROM distribuidor WHERE id_distribuidor = %s"
            await cursor.execute(sql_distribuidor, (id_distribuidor,))
            distribuidor = await cursor.fetchone()

            if distribuidor:
                sql_sucursales = """
                    SELECT s.* FROM sucursal s
                    JOIN distribuidor_sucursal ds ON s.id_sucursal = ds.id_sucursal
                    WHERE ds.id_distribuidor = %s
                """
                await cursor.execute(sql_sucursales, (id_distribuidor,))
                sucursales = await cursor.fetchall()
                distribuidor['sucursales'] = sucursales

            return distribuidor
    finally:
        connection.close()


    
@distribuidor_fl1.route('/<int:distribuidor_id>', methods=['GET'])
async def get_distribuidor_by_id(distribuidor_id):
    async with connect_to_database() as con:
        try:
            distribuidor_by_id= await process_distribuidor_por_id(con,distribuidor_id)
            if distribuidor_by_id:
                return jsonify({"success": True, "data": distribuidor_by_id})
            else:
                return jsonify({"error": f"distribuidor with ID {distribuidor_id} not found"}), 404
        except Exception as e :
            return jsonify({"error":"Data Base erorr {}".format(e)})