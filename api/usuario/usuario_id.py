from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request

usuario_fl1=Blueprint('usuario_id', __name__)


async def get_usuario(connection, usuario_id):
    try:
        async with connection.cursor() as cursor:
            # Obtener información de la sucursal
            sql_usuario = """SELECT * FROM usuario WHERE id_usuario = %s"""
            await cursor.execute(sql_usuario, (usuario_id,))
            usuario_info = await cursor.fetchone()
            return usuario_info
    except Exception as e:
        print(f"Error obtaining sucursal info for ID {usuario_id}: {e}")
        return None
    
@usuario_fl1.route('/<string:usuario_id>', methods=['GET'])
async def get_usuario_by_id(usuario_id):
    async with connect_to_database() as con:
        try:
            usuario_by_id= await get_usuario(con,usuario_id)
            if usuario_by_id:
                return jsonify({"success": True, "data": usuario_by_id})
            else:
                return jsonify({"error": f"usuario with ID {usuario_id} not found"}), 404
        except Exception as e :
            return jsonify({"error":"Data Base erorr {}".format(e)})