from flask import Flask, request, jsonify
from flask import Blueprint
from config.database import connect_to_database

sucursal_fl2 = Blueprint('sucursal_methods', __name__)

@sucursal_fl2.route('/sucursal', methods=['POST'])
async def crear_sucursal():
    try:
        async with connect_to_database() as connection:
            data = request.json
            campos_requeridos = ['direccion', 'telefono', 'nombre', 'gerente', 
                                 'contacto', 'correo_electronico', 'url_logo', 'coordenadas', 
                                 'horarios_de_atencion']
            
            if not all(campo in data for campo in campos_requeridos):
                return jsonify({"error": "Faltan campos requeridos"}), 400
                
            async with connection.cursor() as cursor:
                sql = """INSERT INTO sucursal (
                             direccion, telefono, nombre, gerente, contacto, 
                             correo_electronico, url_logo, coordenadas, horarios_de_atencion
                         ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                valores = (
                    data['direccion'],
                    data['telefono'],
                    data['nombre'],
                    data['gerente'],
                    data['contacto'],
                    data['correo_electronico'],
                    data['url_logo'],
                    data['coordenadas'],
                    data['horarios_de_atencion']
                )
                await cursor.execute(sql, valores)
                await connection.commit()

            return jsonify({"success": True, "message": "Sucursal creada exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


@sucursal_fl2.route('/sucursal/<int:id_sucursal>', methods=['PUT'])
async def actualizar_sucursal(id_sucursal):
    try:
        async with connect_to_database() as connection:
            data = request.json
            campos_permitidos = ['direccion', 'telefono', 'nombre', 'gerente', 'contacto', 'correo_electronico', 'url_logo', 'coordenadas', 'horarios_de_atencion','lastUpdate','created']
            
            if not any(campo in data for campo in campos_permitidos):
                return jsonify({"error": "Se requiere al menos un campo para actualizar"}), 400

            async with connection.cursor() as cursor:
                sql_update = "UPDATE sucursal SET "
                valores = []

                for campo in campos_permitidos:
                    if campo in data:
                        sql_update += f"{campo} = %s, "
                        valores.append(data[campo])

                sql_update = sql_update.rstrip(', ')
                sql_update += " WHERE id_sucursal = %s"
                valores.append(id_sucursal)

                await cursor.execute(sql_update, valores)
                await connection.commit()

            return jsonify({"success": True, "message": f"Sucursal con ID {id_sucursal} actualizada exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500



@sucursal_fl2.route('/sucursal/<int:id_sucursal>', methods=['DELETE'])
async def eliminar_sucursal(id_sucursal):
    try:
        async with connect_to_database() as connection:
            async with connection.cursor() as cursor:
                sql_delete = "DELETE FROM sucursal WHERE id_sucursal = %s"
                await cursor.execute(sql_delete, (id_sucursal,))
                await connection.commit()

            return jsonify({"success": True, "message": f"Sucursal con ID {id_sucursal} eliminada exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    
@sucursal_fl2.route('/<int:id_sucursal>/imagen', methods=['POST'])
async def agregar_imagen_sucursal(id_sucursal):
    try:
        async with connect_to_database() as connection:
            data = request.json
            campos_requeridos = ['url_image', 'descripcion']

            if not all(campo in data for campo in campos_requeridos):
                return jsonify({"error": "Faltan campos requeridos"}), 400

            async with connection.cursor() as cursor:
                sql = """INSERT INTO images_sucursal (url_image, descripcion, id_sucursal) 
                         VALUES (%s, %s, %s)"""
                valores = (
                    data['url_image'],
                    data['descripcion'],
                    id_sucursal  
                )
                await cursor.execute(sql, valores)
                await connection.commit()

            return jsonify({"success": True, "message": "Imagen agregada a la sucursal exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500

@sucursal_fl2.route('/<int:id_sucursal>/articulos', methods=['GET'])
async def obtener_autos_por_sucursal(id_sucursal):
    try:
        async with connect_to_database() as connection:
            async with connection.cursor() as cursor:
                sql = """
                    SELECT a.* FROM articulo a
                    JOIN articulo_sucursal as_rel ON a.id_articulo = as_rel.id_articulo
                    WHERE as_rel.id_sucursal = %s
                """
                await cursor.execute(sql, (id_sucursal,))
                autos = await cursor.fetchall()

                if not autos:
                    return jsonify({"error": f"No se encontraron articulos para la sucursal con ID {id_sucursal}"}), 404

                return jsonify({"success": True, "articulos": autos}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500



@sucursal_fl2.route('/<int:id_sucursal>/usuarios', methods=['GET'])
async def obtener_usuarios_por_sucursal(id_sucursal):
    try:
        async with connect_to_database() as connection:
            async with connection.cursor() as cursor:
                sql = """
                    SELECT * FROM usuario
                    WHERE id_sucursal = %s
                """
                await cursor.execute(sql, (id_sucursal,))
                usuarios = await cursor.fetchall()

                if not usuarios:
                    return jsonify({"error": f"No se encontraron usuarios para la sucursal con ID {id_sucursal}"}), 404

                return jsonify({"success": True, "usuarios": usuarios}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
