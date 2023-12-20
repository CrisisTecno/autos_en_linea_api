from flask import Flask, request, jsonify
from flask import Blueprint
from config.database import connect_to_database
from utils.time import convert_milliseconds_to_datetime,convert_milliseconds_to_time_string

articulo_fl2 = Blueprint('articulo_post', __name__)

# @articulo_fl2.route('/articulo', methods=['POST'])
# async def crear_articulo():
#     try:
#         async with connect_to_database() as connection:
#             data = request.json
#             campos_requeridos = ['marca', 'modelo', 'categoria', 'ano', 
#                                  'precio', 'kilometraje', 'descripcion', 'enable', 'color']

#             if not all(campo in data for campo in campos_requeridos):
#                 return jsonify({"error": "Faltan campos requeridos"}), 400

#             async with connection.cursor() as cursor:
#                 sql = """INSERT INTO articulo (
#                              marca, modelo, categoria, ano, precio, 
#                              kilometraje, descripcion, enable, color
#                          ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#                 valores = (
#                     data['marca'],
#                     data['modelo'],
#                     data['categoria'],
#                     data['ano'],
#                     data['precio'],
#                     data['kilometraje'],
#                     data['descripcion'],
#                     data['enable'],
#                     data['color']
#                 )
#                 await cursor.execute(sql, valores)
#                 await connection.commit()
#                 rows_affected = cursor.rowcount

#             return jsonify({"success": True, "message": "Artículo creado exitosamente"}), 201

#     except Exception as e:
#         return jsonify({"error": f"Error en la base de datos: {e}"}), 500

@articulo_fl2.route('/articulo', methods=['POST'])
async def crear_articulo():
    try:
        async with connect_to_database() as connection:
            data = request.json
            campos_requeridos = ['ano', 'categoria', 'color', 
                                 'descripcion', 'enable', 'mainImage', 'marca', 
                                 'modelo','precio','expedition_date','created',
                                 'lastUpdate','lastInventoryUpdate','kilometraje']   
            if not all(campo in data for campo in campos_requeridos):
                return jsonify({"error": "Faltan campos requeridos"}), 400
                
            async with connection.cursor() as cursor:
                sql_articulo = """INSERT INTO articulo (
                                      ano, categoria, color, descripcion, enable, mainImage, 
                                      marca, modelo, precio, expedition_date, 
                                      created, lastUpdate, lastInventoryUpdate, kilometraje
                                  ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s)"""
                valores_articulo = (
                    data['ano'], 
                    data['categoria'], 
                    data['color'], 
                    data['descripcion'],
                    data['enable'], 
                    data['mainImage'],
                    data['marca'], 
                    data['modelo'],
                    data['precio'], 
                    convert_milliseconds_to_datetime(data['expedition_date']),
                    convert_milliseconds_to_datetime(data['created']),
                    convert_milliseconds_to_datetime(data['lastUpdate']), 
                    convert_milliseconds_to_datetime(data['lastInventoryUpdate']), 
                    data['kilometraje']
                )
                await cursor.execute(sql_articulo, valores_articulo)
                id_articulo = cursor.lastrowid

                if 'sucursal_id' in data:
                    sql_articulo_sucursal = """INSERT INTO articulo_sucursal (id_articulo, id_sucursal) VALUES (%s, %s)"""
                    await cursor.execute(sql_articulo_sucursal, (id_articulo, data['sucursal_id']))
                if 'especificaciones' in data:
                    for especificacion in data['especificaciones']:
                        sql_especificaciones = """INSERT INTO especificaciones (tipo, id_articulo) VALUES (%s, %s)"""
                        await cursor.execute(sql_especificaciones, (especificacion['tipo'], id_articulo))
                        id_especificacion = cursor.lastrowid

                        for clave, valor in especificacion['subespecificaciones'].items():
                            sql_subespecificaciones = """INSERT INTO subespecificaciones (clave, valor, id_especificacion) VALUES (%s, %s, %s)"""
                            await cursor.execute(sql_subespecificaciones, (clave, valor, id_especificacion))

                if 'imagenes' in data:
                    for imagen in data['imagenes']:
                        sql_images_articulo = """INSERT INTO images_articulo (url_image, descripcion, id_articulo) VALUES (%s, %s, %s)"""
                        await cursor.execute(sql_images_articulo, (imagen['url_image'], imagen['descripcion'], id_articulo))

                    await connection.commit()
                

            return jsonify({"success": True, "message": "Artículo creado exitosamente", "id_articulo": id_articulo}), 201

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
