from flask import Blueprint, request, jsonify
from config.database import connect_to_database

articulo_fl3 = Blueprint('articulo_fl3', __name__)

@articulo_fl3.route('/imagen_articulo', methods=['POST'])
def insertar_imagen_articulo():
    try:
        with connect_to_database() as connection:
            data = request.json
            campos_requeridos = ['url_image', 'descripcion', 'id_articulo']

            if not all(isinstance(articulo, dict) and all(campo in articulo for campo in campos_requeridos) for articulo in data):
                return jsonify({"error": "Faltan campos requeridos o formato incorrecto"}), 400

            with connection.cursor() as cursor:
                sql = """INSERT INTO images_articulo (url_image, descripcion, id_articulo) 
                         VALUES (?, ?, ?)"""
                for articulo in data:
                    valores = (articulo['url_image'], articulo['descripcion'], articulo['id_articulo'])
                    cursor.execute(sql, valores)

                cursor.execute(sql, valores)
                connection.commit()

            return jsonify({"success": True, "message": "Imagen de artículo insertada exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
