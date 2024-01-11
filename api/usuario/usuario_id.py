from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request

usuario_fl1=Blueprint('usuario_id', __name__)


def get_usuario(connection, usuario_id):
    try:
        with connection.cursor() as cursor:
            sql_usuario = """SELECT * FROM usuario WHERE id_usuario = """
            cursor.execute(sql_usuario, (usuario_id,))
            usuario_info = cursor.fetchone()

            if usuario_info:
                for key in ['created', 'lastUpdate']: 
                    if usuario_info[key]:
                        usuario_info[key] = int(usuario_info[key].timestamp() * 1000)

            return usuario_info
    except Exception as e:
        print(f"Error obtaining user info for ID {usuario_id}: {e}")
        return None
    
def get_usuario_by_id_fire(connection, usuario_id):
    try:
        with connection.cursor() as cursor:
            sql_usuario = """SELECT * FROM usuario WHERE id_usuario_firebase = """
            cursor.execute(sql_usuario, (usuario_id,))
            usuario_info = cursor.fetchone()

            if usuario_info:
                for key in ['created', 'lastUpdate']: 
                    if usuario_info[key]:
                        usuario_info[key] = int(usuario_info[key].timestamp() * 1000)
      
            return usuario_info
    except Exception as e:
        print(f"Error obtaining user info for ID {usuario_id}: {e}")
        return None

    
@usuario_fl1.route('/<int:id_usuario>', methods=['GET'])
def get_usuario_by_id(id_usuario):
    with connect_to_database() as con:
        try:
            usuario_by_id= get_usuario(con,id_usuario)
            if usuario_by_id:
                return jsonify({"success": True, "data": usuario_by_id})
            else:
                return jsonify({"error": f"usuario with ID {id_usuario} not found"}), 404
        except Exception as e :
            return jsonify({"error":"Data Base erorr {}".format(e)})
        
@usuario_fl1.route('/idf/<string:id_usuario_firebase>', methods=['GET'])
def get_usuario_by_id_firebase(id_usuario_firebase):
    with connect_to_database() as con:
        try:
            usuario_by_id= get_usuario_by_id_fire(con,id_usuario_firebase)
            if usuario_by_id:
                return jsonify({"success": True, "data": usuario_by_id})
            else:
                return jsonify({"error": f"usuario with ID {id_usuario_firebase} not found"}), 404
        except Exception as e :
            return jsonify({"error":"Data Base erorr {}".format(e)})