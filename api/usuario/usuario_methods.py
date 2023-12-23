from flask import Flask, request, jsonify
from flask import Blueprint
from config.database import connect_to_database

usuario_fl2 = Blueprint('usuario_post', __name__)

@usuario_fl2.route('/usuario', methods=['POST'])
async def crear_usuario():
    try:
        async with connect_to_database() as connection:
            data = request.json
            campos_requeridos = [
                                 'rol', 'nombres', 'apellidos',
                                   'correo_electronico', 'num_telefono']
            
            if not all(campo in data for campo in campos_requeridos):
                return jsonify({"error": "Faltan campos requeridos"}), 400
                
            async with connection.cursor() as cursor:
                sql = """INSERT INTO usuario (
                             rol, nombres, apellidos, 
                             correo_electronico, num_telefono, url_logo, 
                             coordenadas, id_sucursal, id_distribuidor, created, lastUpdate, id_usuario_firebase
                         ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %s)"""
                valores = (
                    data['rol'],
                    data['nombres'],
                    data['apellidos'],
                    data['correo_electronico'],
                    data['num_telefono'],
                    data.get('url_logo', ''),
                    data.get('coordenadas', ''),
                    data.get('id_sucursal'),
                    data.get('id_distribuidor'),
                    data.get('id_usuario_firebase','')
                )
                await cursor.execute(sql, valores)
                await connection.commit()

            return jsonify({"success": True, "message": "Usuario creado exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    
@usuario_fl2.route('/usuario/<int:id_usuario>', methods=['PUT'])
async def actualizar_usuario(id_usuario):
    try:
        async with connect_to_database() as connection:
            data = request.json
            campos_permitidos = ['rol', 'nombres', 'apellidos', 'correo_electronico',
                                 'num_telefono', 'url_logo', 'coordenadas', 
                                 'id_sucursal', 'id_distribuidor', 'id_usuario_firebase']
            
            cambios = []
            valores = []
            for campo in campos_permitidos:
                if campo in data:
                    cambios.append(f"{campo} = %s")
                    valores.append(data[campo])

            if not cambios:
                return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

            cambios.append("lastUpdate = CURRENT_TIMESTAMP")
            
            sql_update = "UPDATE usuario SET " + ", ".join(cambios) + " WHERE id_usuario = %s"
            valores.append(id_usuario)
            
            async with connection.cursor() as cursor:
                await cursor.execute(sql_update, valores)
                await connection.commit()

            return jsonify({"success": True, "message": f"Usuario con ID {id_usuario} actualizado exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    
# @usuario_fl2.route('/usuario/<string:id_usuario>', methods=['PUT'])
# async def actualizar_usuario(id_usuario):
#     try:
#         async with connect_to_database() as connection:
#             data = request.json
#             campos_permitidos = ['rol', 'nombres', 'apellidos', 'correo_electronico',
#                                  'num_telefono', 'url_logo', 'coordenadas', 'id_sucursal', 'id_distribuidor']
            
#             if not any(campo in data for campo in campos_permitidos):
#                 return jsonify({"error": "Se requiere al menos un campo para actualizar"}), 400
                
#             async with connection.cursor() as cursor:
#                 sql_update = "UPDATE usuario SET "
#                 valores = []

#                 for campo in campos_permitidos:
#                     if campo in data:
#                         sql_update += f"{campo} = %s, "
#                         valores.append(data[campo])

#                 sql_update = sql_update.rstrip(', ')
#                 sql_update += " WHERE id_usuario = %s"
#                 valores.append(id_usuario)
                
#                 await cursor.execute(sql_update, valores)
#                 await connection.commit()

#             return jsonify({"success": True, "message": f"Usuario con ID {id_usuario} actualizado exitosamente"}), 200

#     except Exception as e:
#         return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    

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
                print(result)
                existe = result['COUNT(*)'] > 0
                id_usuario = None
                if existe:
                    sql_firebase = "SELECT id_usuario FROM usuario WHERE num_telefono = %s"
                    await cursor.execute(sql_firebase, (num_telefono,))
                    result_firebase = await cursor.fetchone()
                    id_usuario = result_firebase['id_usuario'] if result_firebase else None
                else:
                    id_usuario="No Existe"
                print(result['COUNT(*)'])
            return jsonify({"existe": existe, "id_usuario": id_usuario}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


# @usuario_fl2.route('/<string:id_usuario>/favoritos', methods=['GET'])
# async def obtener_autos_favoritos_usuario(id_usuario): 
#     try:
#         async with connect_to_database() as connection:
#             async with connection.cursor() as cursor:
#                 sql = """
#                     SELECT 
#                         articulo.*, 
#                         favoritos.enable as favorite,
#                         especificaciones.id_especificacion,
#                         especificaciones.tipo,
#                         images_articulo.url_image,
#                         images_articulo.descripcion as img_descripcion
#                     FROM 
#                         articulo
#                     JOIN 
#                         favoritos ON articulo.id_articulo = favoritos.id_articulo
#                     LEFT JOIN 
#                         especificaciones ON articulo.id_articulo = especificaciones.id_articulo
#                     LEFT JOIN 
#                         images_articulo ON articulo.id_articulo = images_articulo.id_articulo
#                     WHERE 
#                         favoritos.id_usuario = %s
#                     ORDER BY 
#                         articulo.id_articulo
#                 """
#                 await cursor.execute(sql, (id_usuario,))
#                 autos_favoritos = await cursor.fetchall()
#                 if not autos_favoritos:
#                     return jsonify({"error": f"No se encontraron autos favoritos para el usuario con ID {id_usuario}"}), 404

#                 articulos_favoritos = [auto for auto in autos_favoritos if auto['favorite']]
#                 articulos_dict = {}
#                 processed_especificaciones = set()
#                 for row in articulos_favoritos:
                    
#                     id_articulo = row['id_articulo']
#                     id_especificacion = row.get('id_especificacion')
#                     print(id_especificacion)
#                     if id_especificacion and id_especificacion not in processed_especificaciones:
#                         processed_especificaciones.add(id_especificacion)

#                         sql_subespecificaciones = """
#                             SELECT * FROM subespecificaciones
#                             WHERE id_especificacion = %s
#                         """
#                         await cursor.execute(sql_subespecificaciones, (id_especificacion,))
#                         subespecificaciones_raw = await cursor.fetchall()
#                         print(subespecificaciones_raw)
#                         subespecificaciones = {sub['clave']: sub['valor'] for sub in subespecificaciones_raw}
#                         especificacion = {
#                             'tipo': row['tipo'],
#                             'subespecificaciones': subespecificaciones
#                         }
#                         row[id_articulo]['especificaciones'].append(articulos_dict)
               
#                 return jsonify({"success": True, "autos_favoritos": articulos_favoritos}), 200

#     except Exception as e:
#         return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    

# @usuario_fl2.route('/<string:id_usuario>/favoritos', methods=['GET'])
# async def obtener_autos_favoritos_usuario_firebase(id_usuario): 
#     try:
#         async with connect_to_database() as connection:
#             async with connection.cursor() as cursor:
#                 sql = """
#                     SELECT 
#                         articulo.*, 
#                         favoritos.enable as favorite,
#                         especificaciones.id_especificacion,
#                         especificaciones.tipo,
#                         images_articulo.url_image,
#                         images_articulo.descripcion as img_descripcion
#                     FROM 
#                         articulo
#                     JOIN 
#                         favoritos ON articulo.id_articulo = favoritos.id_articulo
#                     LEFT JOIN 
#                         especificaciones ON articulo.id_articulo = especificaciones.id_articulo
#                     LEFT JOIN 
#                         images_articulo ON articulo.id_articulo = images_articulo.id_articulo
#                     WHERE 
#                         favoritos.id_usuario = %s
#                     ORDER BY 
#                         articulo.id_articulo
#                 """
#                 await cursor.execute(sql, (id_usuario,))
#                 autos_favoritos = await cursor.fetchall()
#                 if not autos_favoritos:
#                     return jsonify({"error": f"No se encontraron autos favoritos para el usuario con ID {id_usuario}"}), 404

#                 articulos_dict = {}
#                 processed_especificaciones = set()
#                 for row in autos_favoritos:
#                     id_articulo = row['id_articulo']
#                     id_especificacion = row.get('id_especificacion')

#                     if id_articulo not in articulos_dict:
#                         articulos_dict[id_articulo] = row
#                         articulos_dict[id_articulo]['especificaciones'] = []
#                         articulos_dict[id_articulo]['imagenes'] = []

#                     if id_especificacion and id_especificacion not in processed_especificaciones:
#                         processed_especificaciones.add(id_especificacion)

#                         sql_subespecificaciones = """
#                             SELECT * FROM subespecificaciones
#                             WHERE id_especificacion = %s
#                         """
#                         await cursor.execute(sql_subespecificaciones, (id_especificacion,))
#                         subespecificaciones_raw = await cursor.fetchall()

#                         subespecificaciones = {sub['clave']: sub['valor'] for sub in subespecificaciones_raw}
#                         especificacion = {
#                             'tipo': row['tipo'],
#                             'subespecificaciones': subespecificaciones
#                         }
#                         articulos_dict[id_articulo]['especificaciones'].append(especificacion)

#                 articulos_favoritos = list(articulos_dict.values())
#                 return jsonify({"success": True, "autos_favoritos": articulos_favoritos}), 200

#     except Exception as e:
#         return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    
@usuario_fl2.route('/<int:id_usuario>/favoritos', methods=['GET'])
async def obtener_autos_favoritos_usuario(id_usuario): 
    try:
        async with connect_to_database() as connection:
            async with connection.cursor() as cursor:
                sql = """
                    SELECT 
                        articulo.*, 
                        favoritos.enable as favorite,
                        especificaciones.id_especificacion,
                        especificaciones.tipo,
                        images_articulo.url_image,
                        images_articulo.descripcion as img_descripcion
                    FROM 
                        articulo
                    JOIN 
                        favoritos ON articulo.id_articulo = favoritos.id_articulo
                    LEFT JOIN 
                        especificaciones ON articulo.id_articulo = especificaciones.id_articulo
                    LEFT JOIN 
                        images_articulo ON articulo.id_articulo = images_articulo.id_articulo
                    WHERE 
                        favoritos.id_usuario = %s
                    ORDER BY 
                        articulo.id_articulo
                """
                await cursor.execute(sql, (id_usuario,))
                autos_favoritos = await cursor.fetchall()
                if not autos_favoritos:
                    return jsonify({"error": f"No se encontraron autos favoritos para el usuario con ID {id_usuario}"}), 404

                articulos_dict = {}
                processed_especificaciones = set()
                for row in autos_favoritos:
                    id_articulo = row['id_articulo']
                    id_especificacion = row.get('id_especificacion')

                    if id_articulo not in articulos_dict:
                        articulos_dict[id_articulo] = row
                        articulos_dict[id_articulo]['especificaciones'] = []
                        articulos_dict[id_articulo]['imagenes'] = []

                    if id_especificacion and id_especificacion not in processed_especificaciones:
                        processed_especificaciones.add(id_especificacion)

                        sql_subespecificaciones = """
                            SELECT * FROM subespecificaciones
                            WHERE id_especificacion = %s
                        """
                        await cursor.execute(sql_subespecificaciones, (id_especificacion,))
                        subespecificaciones_raw = await cursor.fetchall()

                        subespecificaciones = {sub['clave']: sub['valor'] for sub in subespecificaciones_raw}
                        especificacion = {
                            'tipo': row['tipo'],
                            'subespecificaciones': subespecificaciones
                        }
                        articulos_dict[id_articulo]['especificaciones'].append(especificacion)

                articulos_favoritos = list(articulos_dict.values())
                return jsonify({"success": True, "autos_favoritos": articulos_favoritos}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
