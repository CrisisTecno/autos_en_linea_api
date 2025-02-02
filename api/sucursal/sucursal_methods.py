from flask import Flask, request, jsonify
from flask import Blueprint
from config.database import connect_to_database
from utils.time import unix_to_datetime,convert_milliseconds_to_datetime,timedelta_to_milliseconds,convert_milliseconds_to_time_string
from api.distribuidor.distribuidor_methods import procesar_articulo
from datetime import datetime
from utils.serializer import resultados_a_json, convertir_a_datetime

sucursal_fl2 = Blueprint('sucursal_methods', __name__)

# @sucursal_fl2.route('/sucursal', methods=['POST'])
# def crear_sucursal():
#     try:
#         with connect_to_database() as connection:
#             data = request.json
#             campos_requeridos = ['direccion', 'telefono', 'nombre', 'gerente', 
#                                  'contacto', 'correo_electronico', 'url_logo', 'coordenadas', 
#                                  'horarios_de_atencion']
            
#             if not all(campo in data for campo in campos_requeridos):
#                 return jsonify({"error": "Faltan campos requeridos"}), 400
                
#             with connection.cursor() as cursor:
#                 sql = """INSERT INTO sucursal (
#                              direccion, telefono, nombre, gerente, contacto, 
#                              correo_electronico, url_logo, coordenadas, horarios_de_atencion
#                          ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
#                 valores = (
#                     data['direccion'],
#                     data['telefono'],
#                     data['nombre'],
#                     data['gerente'],
#                     data['contacto'],
#                     data['correo_electronico'],
#                     data['url_logo'],
#                     data['coordenadas'],
#                     data['horarios_de_atencion']
#                 )
#                 cursor.execute(sql, valores)
#                 connection.commit()

#             return jsonify({"success": True, "message": "Sucursal creada exitosamente"}), 201

#     except Exception as e:
#         return jsonify({"error": f"Error en la base de datos: {e}"}), 500

@sucursal_fl2.route('/sucursal', methods=['POST'])
def crear_sucursal():
    try:
        with connect_to_database() as connection:
            data = request.json
           
            campos_requeridos = ['direccion', 'nombre', 'gerente', 
                                 'contacto', 'correo_electronico', 'url_logo', 'coordenadas', 
                                 'horarioAtencion','created','lastUpdate','id_distribuidor']
            
            if not all(campo in data for campo in campos_requeridos) or not all(dia in data['horarioAtencion'] for dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']):
                return jsonify({"error": "Faltan campos requeridos"}), 400
            
            with connection.cursor() as cursor:

                sql_sucursal = """INSERT INTO sucursal (
                                      direccion, nombre, gerente, contacto, 
                                      correo_electronico, url_logo, coordenadas,created,lastUpdate
                                  )OUTPUT INSERTED.id_sucursal VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                valores_sucursal = (
                    data['direccion'],
                    data['nombre'],
                    data['gerente'],
                    data['contacto'],
                    data['correo_electronico'],
                    data['url_logo'],
                    data['coordenadas'],
                    unix_to_datetime(data['created']),
                    unix_to_datetime(data['lastUpdate'])
                    # data['id_distribuidor']
                )
                cursor.execute(sql_sucursal, valores_sucursal)

                id_sucursal = cursor.fetchone()[0] 
                if 'id_distribuidor' in data:
                    sql_distribuidor_sucursal = """INSERT INTO distribuidor_sucursal (id_distribuidor, id_sucursal)
                                                VALUES (?, ?)"""
                    valores_distribuidor_sucursal = (data['id_distribuidor'], id_sucursal)
                    cursor.execute(sql_distribuidor_sucursal, valores_distribuidor_sucursal)

                for dia, horarios in data['horarioAtencion'].items():
                    sql_horarios = """INSERT INTO horarios_sucursal (id_sucursal, day, [open], [close]) 
                                      VALUES (?, ?, ?, ?)"""
                    valores_horarios = (id_sucursal, dia, 
                    convert_milliseconds_to_time_string(horarios['open']),
                    convert_milliseconds_to_time_string( horarios['close']))
                    cursor.execute(sql_horarios, valores_horarios)
                if 'imagenes' in data:
                    for imagen in data['imagenes']:
                        sql_images_articulo = """INSERT INTO images_sucursal (url_image, descripcion, id_sucursal) VALUES (?, ?, ?)"""
                        cursor.execute(sql_images_articulo, (imagen['url_image'], imagen['descripcion'], id_sucursal))
                        connection.commit()

                connection.commit()

            return jsonify({"success": True, "message": "Sucursal creada exitosamente","ID SUCURSAL":id_sucursal}), 201

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
#/
@sucursal_fl2.route('/sucursal/<int:id_sucursal>', methods=['PUT'])
def actualizar_sucursal(id_sucursal):
    try:
        with connect_to_database() as connection:
            data = request.json
            campos_permitidos = ['contacto', 'coordenadas', 
                                 'correo_electronico', 'direccion', 'gerente', 
                                   
                                 'nombre','id_distribuidor'
                                 'sucursal_images','telefono','url_logo','horarios_sucursal']
            
            if not any(campo in data for campo in campos_permitidos):
                return jsonify({"error": "Se requiere al menos un campo para actualizar"}), 400

            with connection.cursor() as cursor:
                sql_update = "UPDATE sucursal SET "
                valores = []
                existee=False
                for campo in campos_permitidos:
                    if campo in data and campo!='horarioAtencion':
                        valor = data[campo]
                        existee=True
                        if campo in ['created', 'lastUpdate']:
                            valor = unix_to_datetime(valor)
                        sql_update += f"{campo} = ?, "
                        valores.append(valor)
                if existee:
                    sql_update = sql_update.rstrip(', ')
                    sql_update += " WHERE id_sucursal = ?"
                    valores.append(id_sucursal)
            
                    cursor.execute(sql_update, valores)

                # if 'horarioAtencion' in data:
                #     for dia, horarios in data['horarioAtencion'].items():
                #         sql_horarios = """UPDATE horarios_sucursal 
                #                           SET open = ?, close = ? 
                #                           WHERE id_sucursal = ? AND day = ?"""
                #         valores_horarios = (timedelta_to_milliseconds(horarios['open']),
                #                             timedelta_to_milliseconds(horarios['close']),
                #                             id_sucursal, dia)
                #         cursor.execute(sql_horarios, valores_horarios)

                # if 'imagenes' in data:
                #     sql_eliminar_imagenes = "DELETE FROM images_sucursal WHERE id_sucursal = ?"
                #     cursor.execute(sql_eliminar_imagenes, (id_sucursal,))

                #     for imagen in data['imagenes']:
                #         sql_insertar_imagen = """INSERT INTO images_sucursal (url_image, descripcion, id_sucursal) 
                #                                  VALUES (?, ?, ?)"""
                #         cursor.execute(sql_insertar_imagen, (imagen['url_image'], imagen['descripcion'], id_sucursal))   
                if 'horarioAtencion' in data:
                    
                    for dia, horarios in data['horarioAtencion'].items():
                        print(dia)
                        print(horarios)
                        print(horarios['open'])
                        open_time = convert_milliseconds_to_time_string(horarios['open'])
                        close_time = convert_milliseconds_to_time_string(horarios['close'])
                        sql_update_horarios = """UPDATE horarios_sucursal
                                                SET [open] = ?, [close] = ?
                                                WHERE id_sucursal = ? AND day = ?"""
                        cursor.execute(sql_update_horarios, (open_time, close_time, id_sucursal, dia))
                connection.commit()

            return jsonify({"success": True, "message": f"Sucursal con ID {id_sucursal} actualizada exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500



@sucursal_fl2.route('/sucursal/<int:id_sucursal>', methods=['DELETE'])
def eliminar_sucursal(id_sucursal):
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                sql_delete_distribuidor_sucursal = "DELETE FROM distribuidor_sucursal WHERE id_sucursal = ?"
                cursor.execute(sql_delete_distribuidor_sucursal, (id_sucursal,))

                sql_delete_images_sucursal = "DELETE FROM images_sucursal WHERE id_sucursal = ?"
                cursor.execute(sql_delete_images_sucursal, (id_sucursal,))

                sql_delete_articulo_sucursal = "DELETE FROM articulo_sucursal WHERE id_sucursal = ?"
                cursor.execute(sql_delete_articulo_sucursal, (id_sucursal,))

                sql_delete_horarios_sucursal = "DELETE FROM horarios_sucursal WHERE id_sucursal = ?"
                cursor.execute(sql_delete_horarios_sucursal, (id_sucursal,))

                sql_delete_usuario_sucursal = "DELETE FROM usuario_sucursal WHERE id_sucursal = ?"
                cursor.execute(sql_delete_usuario_sucursal, (id_sucursal,))

                sql_delete_sucursal = "DELETE FROM sucursal WHERE id_sucursal = ?"
                cursor.execute(sql_delete_sucursal, (id_sucursal,))

                connection.commit()

            return jsonify({"success": True, "message": f"Sucursal con ID {id_sucursal} y registros relacionados eliminados exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500

    
@sucursal_fl2.route('/<int:id_sucursal>/imagen', methods=['POST'])
def agregar_imagen_sucursal(id_sucursal):
    try:
        with connect_to_database() as connection:
            data = request.json
            campos_requeridos = ['url_image', 'descripcion']

            if not all(isinstance(articulo, dict) and all(campo in articulo for campo in campos_requeridos) for articulo in data):
                return jsonify({"error": "Faltan campos requeridos o formato incorrecto"}), 400

            with connection.cursor() as cursor:
                sql = """INSERT INTO images_sucursal (url_image, descripcion, id_sucursal) 
                         VALUES (?, ?, ?)"""
                for articulo in data:
                    valores = (articulo['url_image'], articulo['descripcion'], id_sucursal)
                    cursor.execute(sql, valores)

                cursor.execute(sql, valores)
                connection.commit()

            return jsonify({"success": True, "message": "Imagen agregada a la sucursal exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


@sucursal_fl2.route('/<int:id_sucursal>/articulos', methods=['GET'])
def obtener_autos_por_sucursal(id_sucursal):
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                sql = """
                    SELECT a.* FROM articulo a
                    JOIN articulo_sucursal as_rel ON a.id_articulo = as_rel.id_articulo
                    WHERE as_rel.id_sucursal = ?
                """
                cursor.execute(sql, (id_sucursal,))
                autos = resultados_a_json(cursor)

                if not autos:
                    return jsonify({"error": f"No se encontraron articulos para la sucursal con ID {id_sucursal}"}), 404

                return jsonify({"success": True, "articulos": autos}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


@sucursal_fl2.route('/<int:id_sucursal>/articulos', methods=['GET'])
def obtener_articulos_por_distribuidor(id_sucursal):
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                sql_query = """
                    SELECT a.*
                    FROM articulo a
                    JOIN articulo_sucursal asu ON a.id_articulo = asu.id_articulo
                    WHERE ds.id_sucursal = ?;
                """
                cursor.execute(sql_query, (id_sucursal,))
                articulos = resultados_a_json(cursor)

                articulos_procesados = []
                for articulo_record in articulos:
                    articulo_procesado = procesar_articulo(cursor, articulo_record['id_articulo'])
                    articulos_procesados.append(articulo_procesado)

                return jsonify({"success": True, "articulos": articulos_procesados}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


    
@sucursal_fl2.route('/<int:id_sucursal>/usuarios', methods=['GET'])
def obtener_usuarios_por_distribuidor(id_sucursal):
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                
                sql = """SELECT 
                u.id_usuario, u.id_usuario_firebase, u.rol,
                u.nombres, u.apellidos, u.correo_electronico, u.num_telefono,
                u.url_logo, u.coordenadas, u.created, u.lastUpdate,
                s.id_sucursal, d.id_distribuidor
            FROM usuario u
            LEFT JOIN usuario_sucursal s ON u.id_usuario = s.id_usuario
            LEFT JOIN usuario_distribuidor d ON u.id_usuario = d.id_usuario
            WHERE s.id_sucursal = ?;"""
                cursor.execute(sql, (id_sucursal,))
                usuarios = resultados_a_json(cursor)

                    
                if not usuarios:
                    return jsonify({"error": f"No se encontraron usuarios para el distribuidor con ID {id_sucursal}"}), 404

                return jsonify({"success": True, "usuarios": usuarios}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


# @sucursal_fl2.route('/<int:id_sucursal>/usuarios', methods=['GET'])
# def obtener_usuarios_por_sucursal(id_sucursal):
#     try:
#         with connect_to_database() as connection:
#             with connection.cursor() as cursor:
#                 sql = """
#                     SELECT * FROM usuario
#                     WHERE id_sucursal = ?
#                 """
#                 cursor.execute(sql, (id_sucursal,))
#                 usuarios = cursor.fetchall()

#                 if not usuarios:
#                     return jsonify({"error": f"No se encontraron usuarios para la sucursal con ID {id_sucursal}"}), 404

#                 return jsonify({"success": True, "usuarios": usuarios}), 200

#     except Exception as e:
#         return jsonify({"error": f"Error en la base de datos: {e}"}), 500