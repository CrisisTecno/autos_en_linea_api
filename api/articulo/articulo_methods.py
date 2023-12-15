from flask import Flask, request, jsonify
from flask import Blueprint
from config.database import connect_to_database

articulo_fl2 = Blueprint('articulo_post', __name__)

@articulo_fl2.route('/articulo', methods=['POST'])
async def crear_articulo():
    try:
        async with connect_to_database() as connection:
            data = request.json
            campos_requeridos = ['marca', 'modelo', 'categoria', 'ano', 
                                 'precio', 'kilometraje', 'descripcion', 'enable', 'color']

            if not all(campo in data for campo in campos_requeridos):
                return jsonify({"error": "Faltan campos requeridos"}), 400

            async with connection.cursor() as cursor:
                sql = """INSERT INTO articulo (
                             marca, modelo, categoria, ano, precio, 
                             kilometraje, descripcion, enable, color
                         ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                valores = (
                    data['marca'],
                    data['modelo'],
                    data['categoria'],
                    data['ano'],
                    data['precio'],
                    data['kilometraje'],
                    data['descripcion'],
                    data['enable'],
                    data['color']
                )
                await cursor.execute(sql, valores)
                await connection.commit()
                rows_affected = cursor.rowcount

            return jsonify({"success": True, "message": "Artículo creado exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500

@articulo_fl2.route('/articulo/<int:id_articulo>', methods=['PUT'])
async def actualizar_articulo(id_articulo):
    try:
        async with connect_to_database() as connection:
            data = request.json
            campos_permitidos = ['marca', 'modelo', 'categoria', 'ano', 'precio', 
                                 'kilometraje', 'descripcion', 'enable', 'color']

            if not any(campo in data for campo in campos_permitidos):
                return jsonify({"error": "Se requiere al menos un campo para actualizar"}), 400

            async with connection.cursor() as cursor:
                sql_update = "UPDATE articulo SET "
                valores = []

                for campo in campos_permitidos:
                    if campo in data:
                        sql_update += f"{campo} = %s, "
                        valores.append(data[campo])

                sql_update = sql_update.rstrip(', ')
                sql_update += " WHERE id_articulo = %s"
                valores.append(id_articulo)

                await cursor.execute(sql_update, valores)
                await connection.commit()

            return jsonify({"success": True, "message": f"Artículo con ID {id_articulo} actualizado exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


@articulo_fl2.route('/articulo/<int:id_articulo>', methods=['DELETE'])
async def eliminar_articulo(id_articulo):
    try:
        async with connect_to_database() as connection:
            async with connection.cursor() as cursor:
                sql_delete = "DELETE FROM articulo WHERE id_articulo = %s"
                await cursor.execute(sql_delete, (id_articulo,))
                await connection.commit()

            return jsonify({"success": True, "message": f"articulo con ID {id_articulo} eliminado exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
