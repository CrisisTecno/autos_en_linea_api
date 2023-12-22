from flask import Flask, request, jsonify
from flask import Blueprint
from config.database import connect_to_database
from utils.time import convert_milliseconds_to_datetime,convert_milliseconds_to_time_string
from api.distribuidor.distribuidor_methods import procesar_articulo
from datetime import datetime

sucursal_fl2 = Blueprint('sucursal_methods', __name__)

# @sucursal_fl2.route('/sucursal', methods=['POST'])
# async def crear_sucursal():
#     try:
#         async with connect_to_database() as connection:
#             data = request.json
#             campos_requeridos = ['direccion', 'telefono', 'nombre', 'gerente', 
#                                  'contacto', 'correo_electronico', 'url_logo', 'coordenadas', 
#                                  'horarios_de_atencion']
            
#             if not all(campo in data for campo in campos_requeridos):
#                 return jsonify({"error": "Faltan campos requeridos"}), 400
                
#             async with connection.cursor() as cursor:
#                 sql = """INSERT INTO sucursal (
#                              direccion, telefono, nombre, gerente, contacto, 
#                              correo_electronico, url_logo, coordenadas, horarios_de_atencion
#                          ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
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
#                 await cursor.execute(sql, valores)
#                 await connection.commit()

#             return jsonify({"success": True, "message": "Sucursal creada exitosamente"}), 201

#     except Exception as e:
#         return jsonify({"error": f"Error en la base de datos: {e}"}), 500

@sucursal_fl2.route('/sucursal', methods=['POST'])
async def crear_sucursal():
    try:
        async with connect_to_database() as connection:
            data = request.json
            print(data)
            # Verificar la presencia de todos los campos, incluyendo los horarios
            campos_requeridos = ['direccion', 'nombre', 'gerente', 
                                 'contacto', 'correo_electronico', 'url_logo', 'coordenadas', 
                                 'horarioAtencion','created','lastUpdate','id_distribuidor']
            if not all(campo in data for campo in campos_requeridos) or not all(dia in data['horarioAtencion'] for dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']):
                print("Campos en la solicitud:", data.keys())
                print("Días en horarioAtencion:", data['horarioAtencion'].keys() if 'horarioAtencion' in data else "No está presente")
                return jsonify({"error": "Faltan campos requeridos"}), 400
            print(convert_milliseconds_to_datetime(data['created']))
            print(convert_milliseconds_to_datetime(data['lastUpdate']))
            async with connection.cursor() as cursor:
                # Insertar datos de la sucursal
                sql_sucursal = """INSERT INTO sucursal (
                                      direccion, nombre, gerente, contacto, 
                                      correo_electronico, url_logo, coordenadas,created,lastUpdate
                                  ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                valores_sucursal = (
                    data['direccion'],
                    data['nombre'],
                    data['gerente'],
                    data['contacto'],
                    data['correo_electronico'],
                    data['url_logo'],
                    data['coordenadas'],
                    convert_milliseconds_to_datetime(data['created']),
                    convert_milliseconds_to_datetime(data['lastUpdate'])
                    # data['id_distribuidor']
                )
                await cursor.execute(sql_sucursal, valores_sucursal)

                id_sucursal = cursor.lastrowid 

                sql_distribuidor_sucursal = """INSERT INTO distribuidor_sucursal (id_distribuidor, id_sucursal)
                                               VALUES (%s, %s)"""
                valores_distribuidor_sucursal = (data['id_distribuidor'], id_sucursal)
                await cursor.execute(sql_distribuidor_sucursal, valores_distribuidor_sucursal)

                for dia, horarios in data['horarioAtencion'].items():
                    sql_horarios = """INSERT INTO horarios_sucursal (id_sucursal, day, open, close) 
                                      VALUES (%s, %s, %s, %s)"""
                    valores_horarios = (id_sucursal, dia, 
                    convert_milliseconds_to_time_string(horarios['open']),
                    convert_milliseconds_to_time_string( horarios['close']))
                    await cursor.execute(sql_horarios, valores_horarios)
                if 'imagenes' in data:
                    for imagen in data['imagenes']:
                        sql_images_articulo = """INSERT INTO images_sucursal (url_image, descripcion, id_sucursal) VALUES (%s, %s, %s)"""
                        await cursor.execute(sql_images_articulo, (imagen['url_image'], imagen['descripcion'], id_sucursal))
                        await connection.commit()

                await connection.commit()

            return jsonify({"success": True, "message": "Sucursal creada exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500

@sucursal_fl2.route('/sucursal/<int:id_sucursal>', methods=['PUT'])
async def actualizar_sucursal(id_sucursal):
    try:
        async with connect_to_database() as connection:
            data = request.json
            campos_permitidos = ['contacto', 'coordenadas', 
                                 'correo_electronico', 'direccion', 'gerente', 
                                   
                                 'nombre',
                                 'sucursal_images','telefono','url_logo','horarios_sucursal']
            
            if not any(campo in data for campo in campos_permitidos):
                return jsonify({"error": "Se requiere al menos un campo para actualizar"}), 400

            async with connection.cursor() as cursor:
                sql_update = "UPDATE sucursal SET "
                valores = []

                for campo in campos_permitidos:
                    if campo in data:
                        sql_update += f"{campo} = %s, "
                        valores.append(data[campo])

                # sql_update += "lastUpdate = %s WHERE id_sucursal = %s"
                # valores.append(convert_milliseconds_to_datetime(data.get('lastUpdate', int(datetime.now().timestamp() * 1000))))
                # valores.append(id_sucursal)

                last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                sql_update += "lastUpdate = %s WHERE id_sucursal = %s"
                valores.append(last_update)
                valores.append(id_sucursal)

                await cursor.execute(sql_update, valores)

                if 'horarioAtencion' in data:
                    for dia, horarios in data['horarioAtencion'].items():
                        sql_horarios = """UPDATE horarios_sucursal 
                                          SET open = %s, close = %s 
                                          WHERE id_sucursal = %s AND day = %s"""
                        valores_horarios = (convert_milliseconds_to_time_string(horarios['open']),
                                            convert_milliseconds_to_time_string(horarios['close']),
                                            id_sucursal, dia)
                        await cursor.execute(sql_horarios, valores_horarios)

                if 'imagenes' in data:
                    sql_eliminar_imagenes = "DELETE FROM images_sucursal WHERE id_sucursal = %s"
                    await cursor.execute(sql_eliminar_imagenes, (id_sucursal,))

                    for imagen in data['imagenes']:
                        sql_insertar_imagen = """INSERT INTO images_sucursal (url_image, descripcion, id_sucursal) 
                                                 VALUES (%s, %s, %s)"""
                        await cursor.execute(sql_insertar_imagen, (imagen['url_image'], imagen['descripcion'], id_sucursal))   

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


@sucursal_fl2.route('/<int:id_sucursal>/articulos', methods=['GET'])
async def obtener_articulos_por_distribuidor(id_sucursal):
    try:
        async with connect_to_database() as connection:
            async with connection.cursor() as cursor:
                sql_query = """
                    SELECT a.*
                    FROM articulo a
                    JOIN articulo_sucursal asu ON a.id_articulo = asu.id_articulo
                    WHERE ds.id_sucursal = %s;
                """
                await cursor.execute(sql_query, (id_sucursal,))
                articulos = await cursor.fetchall()

                articulos_procesados = []
                for articulo_record in articulos:
                    articulo_procesado = await procesar_articulo(cursor, articulo_record['id_articulo'])
                    articulos_procesados.append(articulo_procesado)

                return jsonify({"success": True, "articulos": articulos_procesados}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


    
@sucursal_fl2.route('/<int:id_sucursal>/usuarios', methods=['GET'])
async def obtener_usuarios_por_distribuidor(id_sucursal):
    try:
        async with connect_to_database() as connection:
            async with connection.cursor() as cursor:
              
                sql = """
                    SELECT apellidos,coordenadas,correo_electronico,created,id_sucursal,id_sucursal
                    id_usuario,id_usuario_firebase,lastUpdate,nombres,num_telefono,rol,url_logo  FROM usuario
                    WHERE id_sucursal = %s
                """
                await cursor.execute(sql, (id_sucursal,))
                usuarios = await cursor.fetchall()
                print(usuarios)
                for user in usuarios:
                    for key in ['created', 'lastUpdate']:
                        if user[key]:
                            user[key] = int(user[key].timestamp() * 1000)
                    
                if not usuarios:
                    return jsonify({"error": f"No se encontraron usuarios para el distribuidor con ID {id_sucursal}"}), 404

                return jsonify({"success": True, "usuarios": usuarios}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


# @sucursal_fl2.route('/<int:id_sucursal>/usuarios', methods=['GET'])
# async def obtener_usuarios_por_sucursal(id_sucursal):
#     try:
#         async with connect_to_database() as connection:
#             async with connection.cursor() as cursor:
#                 sql = """
#                     SELECT * FROM usuario
#                     WHERE id_sucursal = %s
#                 """
#                 await cursor.execute(sql, (id_sucursal,))
#                 usuarios = await cursor.fetchall()

#                 if not usuarios:
#                     return jsonify({"error": f"No se encontraron usuarios para la sucursal con ID {id_sucursal}"}), 404

#                 return jsonify({"success": True, "usuarios": usuarios}), 200

#     except Exception as e:
#         return jsonify({"error": f"Error en la base de datos: {e}"}), 500