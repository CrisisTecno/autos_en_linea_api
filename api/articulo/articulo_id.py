from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request

articulo_fl1=Blueprint('articulo_id', __name__)


async def get_articulo(connection, articulo_id):
    try:
        async with connection.cursor() as cursor:
            # Obtener información de la sucursal
            sql_articulo = """SELECT  * FROM articulo WHERE id_articulo = %s"""
            await cursor.execute(sql_articulo, (articulo_id,))
            articulo_info = await cursor.fetchone()
            return articulo_info
    except Exception as e:
        print(f"Error obtaining sucursal info for ID {articulo_id}: {e}")
        return None
    
@articulo_fl1.route('/<int:articulo_id>', methods=['GET'])
async def get_articulo_by_id(articulo_id):
    async with connect_to_database() as con:
        try:
            articulo_by_id= await get_articulo(con,articulo_id)
            if articulo_by_id:
                return jsonify({"success": True, "data": articulo_by_id})
            else:
                return jsonify({"error": f"articulo with ID {articulo_id} not found"}), 404
        except Exception as e :
            return jsonify({"error":"Data Base erorr {}".format(e)})