from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request

auto_fl1=Blueprint('auto_id', __name__)


async def get_auto(connection, auto_id):
    try:
        async with connection.cursor() as cursor:
            # Obtener información de la sucursal
            sql_auto = """SELECT disponibilidad, marca, modelo,categoria_de_auto,anio,precio,especificaciones,sucursal_id,
            kilometraje FROM auto WHERE id_auto = %s"""
            await cursor.execute(sql_auto, (auto_id,))
            auto_info = await cursor.fetchone()
            return auto_info
    except Exception as e:
        print(f"Error obtaining sucursal info for ID {auto_id}: {e}")
        return None
    
@auto_fl1.route('/<int:auto_id>', methods=['GET'])
async def get_auto_by_id(auto_id):
    async with connect_to_database() as con:
        try:
            auto_by_id= await get_auto(con,auto_id)
            if auto_by_id:
                return jsonify({"success": True, "data": auto_by_id})
            else:
                return jsonify({"error": f"Auto with ID {auto_id} not found"}), 404
        except Exception as e :
            return jsonify({"error":"Data Base erorr {}".format(e)})