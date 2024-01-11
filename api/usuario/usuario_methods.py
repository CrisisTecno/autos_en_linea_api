from flask import Flask, request, jsonify
from flask import Blueprint
from config.database import connect_to_database

usuario_fl2 = Blueprint('usuario_post', __name__)

@usuario_fl2.route('/usuario', methods=['POST'])
def crear_usuario():
    try:
        with connect_to_database() as connection:
            data = request.json
            campos_requeridos = [
                                 'rol', 'nombres', 'apellidos',
                                   'correo_electronico', 'num_telefono']
            
            if not all(campo in data for campo in campos_requeridos):
                return jsonify({"error": "Faltan campos requeridos"}), 400
                
            with connection.cursor() as cursor:
                sql = """INSERT INTO usuario (
                             rol, nombres, apellidos, 
                             correo_electronico, num_telefono, url_logo, 
                             coordenadas, id_sucursal, id_distribuidor, created, lastUpdate, id_usuario_firebase
                         ) VALUES (, , , , , , , , , CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, )"""
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
                cursor.execute(sql, valores)
                connection.commit()

            return jsonify({"success": True, "message": "Usuario creado exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    
@usuario_fl2.route('/usuario/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    try:
        with connect_to_database() as connection:
            data = request.json
            campos_permitidos = ['rol', 'nombres', 'apellidos', 'correo_electronico',
                                 'num_telefono', 'url_logo', 'coordenadas', 
                                 'id_sucursal', 'id_distribuidor', 'id_usuario_firebase']
            
            cambios = []
            valores = []
            for campo in campos_permitidos:
                if campo in data:
                    cambios.append(f"{campo} = ")
                    valores.append(data[campo])

            if not cambios:
                return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

            cambios.append("lastUpdate = CURRENT_TIMESTAMP")
            
            sql_update = "UPDATE usuario SET " + ", ".join(cambios) + " WHERE id_usuario = "
            valores.append(id_usuario)
            
            with connection.cursor() as cursor:
                cursor.execute(sql_update, valores)
                connection.commit()

            return jsonify({"success": True, "message": f"Usuario con ID {id_usuario} actualizado exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    
# @usuario_fl2.route('/usuario/<string:id_usuario>', methods=['PUT'])
# def actualizar_usuario(id_usuario):
#     try:
#         with connect_to_database() as connection:
#             data = request.json
#             campos_permitidos = ['rol', 'nombres', 'apellidos', 'correo_electronico',
#                                  'num_telefono', 'url_logo', 'coordenadas', 'id_sucursal', 'id_distribuidor']
            
#             if not any(campo in data for campo in campos_permitidos):
#                 return jsonify({"error": "Se requiere al menos un campo para actualizar"}), 400
                
#             with connection.cursor() as cursor:
#                 sql_update = "UPDATE usuario SET "
#                 valores = []

#                 for campo in campos_permitidos:
#                     if campo in data:
#                         sql_update += f"{campo} = , "
#                         valores.append(data[campo])

#                 sql_update = sql_update.rstrip(', ')
#                 sql_update += " WHERE id_usuario = "
#                 valores.append(id_usuario)
                
#                 cursor.execute(sql_update, valores)
#                 connection.commit()

#             return jsonify({"success": True, "message": f"Usuario con ID {id_usuario} actualizado exitosamente"}), 200

#     except Exception as e:
#         return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    

@usuario_fl2.route('/usuario/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                sql_delete = "DELETE FROM usuario WHERE id_usuario = "
                cursor.execute(sql_delete, (id_usuario,))
                connection.commit()

            return jsonify({"success": True, "message": f"Usuario con ID {id_usuario} eliminado exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


@usuario_fl2.route('/usuario_existe', methods=['GET'])
def usuario_existe_por_telefono():
    num_telefono = request.args.get('num_telefono')
    if not num_telefono:
        return jsonify({"error": "Número de teléfono requerido"}), 400
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                print(num_telefono)
                sql = "SELECT COUNT(*) FROM usuario WHERE num_telefono = "
                cursor.execute(sql, (num_telefono,))
                result = cursor.fetchone()
                print(result)
                existe = result['COUNT(*)'] > 0
                id_usuario = None
                if existe:
                    sql_firebase = "SELECT * FROM usuario WHERE num_telefono = "
                    cursor.execute(sql_firebase, (num_telefono,))
                    result_firebase = cursor.fetchone()
                    id_usuario = result_firebase['id_usuario'] if result_firebase else None
                    return jsonify({"existe": existe, "data": result_firebase}), 200
                else:
                    id_usuario="No Existe"
                    return jsonify({"existe": existe, "id_usuario": id_usuario}), 200
                
        
    except Exception as e:
        print(e)
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


# @usuario_fl2.route('/<string:id_usuario>/favoritos', methods=['GET'])
# def obtener_autos_favoritos_usuario(id_usuario): 
#     try:
#         with connect_to_database() as connection:
#             with connection.cursor() as cursor:
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
#                         favoritos.id_usuario = 
#                     ORDER BY 
#                         articulo.id_articulo
#                 """
#                 cursor.execute(sql, (id_usuario,))
#                 autos_favoritos = cursor.fetchall()
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
#                             WHERE id_especificacion = 
#                         """
#                         cursor.execute(sql_subespecificaciones, (id_especificacion,))
#                         subespecificaciones_raw = cursor.fetchall()
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
# def obtener_autos_favoritos_usuario_firebase(id_usuario): 
#     try:
#         with connect_to_database() as connection:
#             with connection.cursor() as cursor:
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
#                         favoritos.id_usuario = 
#                     ORDER BY 
#                         articulo.id_articulo
#                 """
#                 cursor.execute(sql, (id_usuario,))
#                 autos_favoritos = cursor.fetchall()
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
#                             WHERE id_especificacion = 
#                         """
#                         cursor.execute(sql_subespecificaciones, (id_especificacion,))
#                         subespecificaciones_raw = cursor.fetchall()

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
    
# @usuario_fl2.route('/<int:id_usuario>/favoritos', methods=['GET'])
# def obtener_autos_favoritos_usuario(id_usuario): 
#     try:
#         with connect_to_database() as connection:
#             with connection.cursor() as cursor:
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
#                         favoritos.enable = 1 AND favoritos.id_usuario =  
#                     ORDER BY 
#                         articulo.id_articulo
#                 """
#                 cursor.execute(sql, (id_usuario,))
#                 autos_favoritos = cursor.fetchall()
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
#                             WHERE id_especificacion = 
#                         """
#                         cursor.execute(sql_subespecificaciones, (id_especificacion,))
#                         subespecificaciones_raw = cursor.fetchall()

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
def obtener_autos_favoritos_usuario(id_usuario): 
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                # Obtener todos los artículos favoritos
                sql = """
                    SELECT 
                        articulo.*, 
                        favoritos.enable as favorite
                    FROM 
                        articulo
                    JOIN 
                        favoritos ON articulo.id_articulo = favoritos.id_articulo
                    WHERE 
                        favoritos.enable = 1 AND favoritos.id_usuario =  
                    ORDER BY 
                        articulo.id_articulo
                """
                cursor.execute(sql, (id_usuario,))
                articulos_raw = cursor.fetchall()
                if not articulos_raw:
                    return jsonify({"error": f"No se encontraron autos favoritos para el usuario con ID {id_usuario}"}), 404
                
                # Procesar cada artículo
                articulos_favoritos = []
                for articulo in articulos_raw:
                    id_articulo = articulo['id_articulo']
                    # Obtener especificaciones para el artículo
                    sql_especificaciones = """
                        SELECT especificaciones.*, subespecificaciones.clave, subespecificaciones.valor
                        FROM especificaciones
                        LEFT JOIN subespecificaciones ON especificaciones.id_especificacion = subespecificaciones.id_especificacion
                        WHERE especificaciones.id_articulo = 
                    """
                    cursor.execute(sql_especificaciones, (id_articulo,))
                    especificaciones_raw = cursor.fetchall()
                    
                    # Agrupar subespecificaciones por especificación
                    especificaciones = {}
                    for esp in especificaciones_raw:
                        id_esp = esp['id_especificacion']
                        if id_esp not in especificaciones:
                            especificaciones[id_esp] = {'tipo': esp['tipo'], 'subespecificaciones': {}}
                        especificaciones[id_esp]['subespecificaciones'][esp['clave']] = esp['valor']

                    # Obtener imágenes para el artículo
                    sql_imagenes = """
                        SELECT url_image, descripcion
                        FROM images_articulo
                        WHERE id_articulo = 
                    """
                    cursor.execute(sql_imagenes, (id_articulo,))
                    imagenes = cursor.fetchall()

                    # Agregar datos al artículo
                    articulo['especificaciones'] = list(especificaciones.values())
                    articulo['imagenes'] = imagenes
                    articulos_favoritos.append(articulo)

                return jsonify({"success": True, "autos_favoritos": articulos_favoritos}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
