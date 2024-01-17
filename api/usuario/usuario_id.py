from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request
from utils.serializer import resultados_a_json, convertir_a_datetime
from datetime import datetime

usuario_fl1=Blueprint('usuario_id', __name__)


def get_usuario(connection, usuario_id):
    try:
        with connection.cursor() as cursor:
            sql_usuario ="""SELECT 
                u.id_usuario, u.id_usuario_firebase, u.rol,
                u.nombres, u.apellidos, u.correo_electronico, u.num_telefono,
                u.url_logo, u.coordenadas, u.created, u.lastUpdate,
                s.id_sucursal, d.id_distribuidor
            FROM usuario u
            LEFT JOIN usuario_sucursal s ON u.id_usuario = s.id_usuario
            LEFT JOIN usuario_distribuidor d ON u.id_usuario = d.id_usuario 
            WHERE u.id_usuario = ?;"""
            
            cursor.execute(sql_usuario, (usuario_id,))
            usuario_info = resultados_a_json(cursor, unico_resultado=True)


            return usuario_info

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    
def get_usuario_by_id_fire(connection, usuario_id):
    try:
        with connection.cursor() as cursor:
            sql_usuario ="""SELECT 
                u.id_usuario, u.id_usuario_firebase, u.rol,
                u.nombres, u.apellidos, u.correo_electronico, u.num_telefono,
                u.url_logo, u.coordenadas, u.created, u.lastUpdate,
                s.id_sucursal, d.id_distribuidor
            FROM usuario u
            LEFT JOIN usuario_sucursal s ON u.id_usuario = s.id_usuario
            LEFT JOIN usuario_distribuidor d ON u.id_usuario = d.id_usuario 
            WHERE u.id_usuario_firebase = ?;"""
            cursor.execute(sql_usuario, (usuario_id,))
            usuario_info = resultados_a_json(cursor, unico_resultado=True)
            
 
      
            return usuario_info
    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500

    
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