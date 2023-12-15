from flask import Flask, request, jsonify
from flask import Blueprint
from config.database import connect_to_database

usuario_fl2 = Blueprint('usuario_post', __name__)

@usuario_fl2.route('/usuario', methods=['POST'])
async def crear_usuario():
    try:
        async with connect_to_database() as connection:
            data = request.json
            campos_requeridos = ['id_usuario', 'rol', 'nombres', 'apellidos', 'correo_electronico', 'num_telefono']
            
            if not all(campo in data for campo in campos_requeridos):
                return jsonify({"error": "Faltan campos requeridos"}), 400
                
            async with connection.cursor() as cursor:
                sql = """INSERT INTO usuario (
                             id_usuario, rol, nombres, apellidos, 
                             correo_electronico, num_telefono, url_logo, 
                             coordenadas, id_sucursal, id_distribuidor, created, lastUpdate
                         ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"""
                valores = (
                    data['id_usuario'],
                    data['rol'],
                    data['nombres'],
                    data['apellidos'],
                    data['correo_electronico'],
                    data['num_telefono'],
                    data.get('url_logo', ''),
                    data.get('coordenadas', ''),
                    data.get('id_sucursal'),
                    data.get('id_distribuidor')
                )
                await cursor.execute(sql, valores)
                await connection.commit()

            return jsonify({"success": True, "message": "Usuario creado exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    

@usuario_fl2.route('/usuario/<string:id_usuario>', methods=['PUT'])
async def actualizar_usuario(id_usuario):
    try:
        async with connect_to_database() as connection:
            data = request.json
            campos_permitidos = ['rol', 'nombres', 'apellidos', 'correo_electronico',
                                 'num_telefono', 'url_logo', 'coordenadas', 'id_sucursal', 'id_distribuidor']
            
            if not any(campo in data for campo in campos_permitidos):
                return jsonify({"error": "Se requiere al menos un campo para actualizar"}), 400
                
            async with connection.cursor() as cursor:
                sql_update = "UPDATE usuario SET "
                valores = []

                for campo in campos_permitidos:
                    if campo in data:
                        sql_update += f"{campo} = %s, "
                        valores.append(data[campo])

                sql_update = sql_update.rstrip(', ')
                sql_update += " WHERE id_usuario = %s"
                valores.append(id_usuario)

                await cursor.execute(sql_update, valores)
                await connection.commit()

            return jsonify({"success": True, "message": f"Usuario con ID {id_usuario} actualizado exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    

@usuario_fl2.route('/usuario/<string:id_usuario>', methods=['DELETE'])
async def eliminar_usuario(id_usuario):
    try:
        async with connect_to_database() as connection:
            async with connection.cursor() as cursor:
                sql_delete = "DELETE FROM usuario WHERE id_usuario = %s"
                await cursor.execute(sql_delete, (id_usuario,))
                await connection.commit()

            return jsonify({"success": True, "message": f"Usuario con ID {id_usuario} eliminado exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


@usuario_fl2.route('/usuario_existe', methods=['GET'])
async def usuario_existe_por_telefono():
    num_telefono = request.args.get('num_telefono')
    if not num_telefono:
        return jsonify({"error": "Número de teléfono requerido"}), 400

    try:
        async with connect_to_database() as connection:
            async with connection.cursor() as cursor:
                print(num_telefono)
                sql = "SELECT COUNT(*) FROM usuario WHERE num_telefono = %s"
                await cursor.execute(sql, (num_telefono,))
                result = await cursor.fetchone()
             
                existe = result['COUNT(*)'] > 0

            return jsonify({"existe": existe}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
