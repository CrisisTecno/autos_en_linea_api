from flask import Flask, request, jsonify
from flask import Blueprint
from config.database import connect_to_database
from utils.serializer import resultados_a_json

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
                             coordenadas,  created, lastUpdate, id_usuario_firebase
                         ) OUTPUT INSERTED.id_usuario VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?)"""
                valores = (
                    data['rol'],
                    data['nombres'],
                    data['apellidos'],
                    data['correo_electronico'],
                    data['num_telefono'],
                    data.get('url_logo', ''),
                    data.get('coordenadas', ''),
                    data.get('id_usuario_firebase','')
                )
                cursor.execute(sql, valores)
                
                id_usuario_insertado  = cursor.fetchone()[0]

                sql_usuario_sucursal = """INSERT INTO usuario_sucursal (
                                        id_usuario, id_sucursal
                                    ) VALUES (?, ?)"""
                valores_usuario_sucursal = (id_usuario_insertado, data.get('id_sucursal'))
                cursor.execute(sql_usuario_sucursal, valores_usuario_sucursal)

                sql_usuario_distribuidor = """INSERT INTO usuario_distribuidor (
                                            id_usuario, id_distribuidor
                                        ) VALUES (?, ?)"""
                valores_usuario_distribuidor = (id_usuario_insertado, data.get('id_distribuidor'))
                cursor.execute(sql_usuario_distribuidor, valores_usuario_distribuidor)
                
                connection.commit()

            return jsonify({"success": True, "message": "Usuario creado exitosamente","id_usuario":id_usuario_insertado}), 201

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
            changes=True
            for campo in campos_permitidos:
                if campo in data:
                    if campo == 'id_distribuidor':
                        with connection.cursor() as cursor:
                            # Verificar si ya existe una relación para este usuario
                            cursor.execute("SELECT COUNT(*) as conteo FROM usuario_distribuidor WHERE id_usuario = ?", (id_usuario,))
                            result = resultados_a_json(cursor, unico_resultado=True)
                            existe = result['conteo'] > 0
                            if existe > 0:
                                # Actualizar la relación existente
                                sql_update_relacion_distribuidor = """
                                    UPDATE usuario_distribuidor SET id_distribuidor = ?
                                    WHERE id_usuario = ?;
                                """
                                valores_relacion_dis = (data['id_distribuidor'], id_usuario)
                                cursor.execute(sql_update_relacion_distribuidor, valores_relacion_dis)
                            else:
                                # Insertar nueva relación si no existe
                                sql_insert_relacion_distribuidor = """
                                    INSERT INTO usuario_distribuidor (id_distribuidor, id_usuario)
                                    VALUES (?, ?);
                                """
                                valores_relacion_dis = (data['id_distribuidor'], id_usuario)
                                cursor.execute(sql_insert_relacion_distribuidor, valores_relacion_dis)
                            connection.commit()
                        # sql_update_relacion_distribuidor = "UPDATE usuario_distribuidor SET id_distribuidor = ? WHERE id_usuario = ?;"
                        # valores_relacion_dis = (data['id_distribuidor'], id_usuario)
                        
                        changes=False
                        # with connection.cursor() as cursor_relacion:
                        #     cursor_relacion.execute(sql_update_relacion_distribuidor, valores_relacion_dis)
                        #     connection.commit()

                    elif campo == 'id_sucursal':
                        with connection.cursor() as cursor:
                            # Verificar si ya existe una relación para este usuario
                            cursor.execute("SELECT COUNT(*) as conteo FROM usuario_sucursal WHERE id_usuario = ?", (id_usuario,))
                            result = resultados_a_json(cursor, unico_resultado=True)
                            existe = result['conteo'] > 0
                            if existe > 0:
                                # Actualizar la relación existente
                                sql_update_relacion_sucursal = """
                                    UPDATE usuario_sucursal SET id_sucursal = ?
                                    WHERE id_usuario = ?;
                                """
                                valores_relacion_dis = (data['id_sucursal'], id_usuario)
                                cursor.execute(sql_update_relacion_sucursal, valores_relacion_dis)
                            else:
                                # Insertar nueva relación si no existe
                                sql_insert_relacion_sucursal = """
                                    INSERT INTO usuario_sucursal (id_sucursal, id_usuario)
                                    VALUES (?, ?);
                                """
                                valores_relacion_dis = (data['id_sucursal'], id_usuario)
                                cursor.execute(sql_insert_relacion_sucursal, valores_relacion_dis)
                            connection.commit()                       
                        changes=False
                        # sql_update_relacion_sucursal = "UPDATE usuario_sucursal SET id_sucursal = ? WHERE id_usuario = ?;"
                        # valores_relacion = (data['id_sucursal'], id_usuario)
                        # with connection.cursor() as cursor_relacion:
                        #     cursor_relacion.execute(sql_update_relacion_sucursal, valores_relacion)
                        #     connection.commit()
                    else:
                        cambios.append(f"{campo} = ?")
                        valores.append(data[campo])
                    

            if not cambios and changes:
                return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

            cambios.append("lastUpdate = CURRENT_TIMESTAMP")

            sql_update_usuario = "UPDATE usuario SET " + ", ".join(cambios) + " WHERE id_usuario = ?"
            valores.append(id_usuario)

            with connection.cursor() as cursor:
                cursor.execute(sql_update_usuario, valores)
                connection.commit()

            return jsonify({"success": True, "message": f"Usuario con ID {id_usuario} actualizado exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
  
# @usuario_fl2.route('/usuario/<int:id_usuario>', methods=['PUT'])
# def actualizar_usuario(id_usuario):
#     try:
#         with connect_to_database() as connection:
#             data = request.json
#             campos_permitidos = ['rol', 'nombres', 'apellidos', 'correo_electronico',
#                                  'num_telefono', 'url_logo', 'coordenadas', 
#                                  'id_sucursal', 'id_distribuidor', 'id_usuario_firebase']
#             cambios = []
#             valores = []
#             for campo in campos_permitidos:
#                 if campo in data:
#                     cambios.append(f"{campo} = ?")
#                     valores.append(data[campo])

#             if not cambios:
#                 return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

#             cambios.append("lastUpdate = CURRENT_TIMESTAMP")
            
#             sql_update = "UPDATE usuario SET " + ", ".join(cambios) + " WHERE id_usuario = ?"
#             valores.append(id_usuario)
            
#             with connection.cursor() as cursor:
#                 cursor.execute(sql_update, valores)
#                 connection.commit()
#                 if 'id_sucursal' in data:
#                     sql_update_sucursal = "UPDATE usuario_sucursal SET id_sucursal = ? WHERE id_usuario = ?"
#                     valores_sucursal = (data['id_sucursal'], id_usuario)
#                     cursor.execute(sql_update_sucursal, valores_sucursal)

#                 if 'id_distribuidor' in data:
#                     sql_update_distribuidor = "UPDATE usuario_distribuidor SET id_distribuidor = ? WHERE id_usuario = ?"
#                     valores_distribuidor = (data['id_distribuidor'], id_usuario)
#                     cursor.execute(sql_update_distribuidor, valores_distribuidor)

#             return jsonify({"success": True, "message": f"Usuario con ID {id_usuario} actualizado exitosamente"}), 200

#     except Exception as e:
#         return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    

@usuario_fl2.route('/usuario/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                sql_delete_actividades_usuario = "DELETE FROM registro_actividades_usuario WHERE id_usuario = ?"
                cursor.execute(sql_delete_actividades_usuario, (id_usuario,))

                sql_delete_favoritos = "DELETE FROM favoritos WHERE id_usuario = ?"
                cursor.execute(sql_delete_favoritos, (id_usuario,))

                sql_delete_usuario_sucursal = "DELETE FROM usuario_sucursal WHERE id_usuario = ?"
                cursor.execute(sql_delete_usuario_sucursal, (id_usuario,))

                sql_delete_usuario_distribuidor = "DELETE FROM usuario_distribuidor WHERE id_usuario = ?"
                cursor.execute(sql_delete_usuario_distribuidor, (id_usuario,))

                sql_delete_usuario = "DELETE FROM usuario WHERE id_usuario = ?"
                cursor.execute(sql_delete_usuario, (id_usuario,))
                
                connection.commit()

            return jsonify({"success": True, "message": f"Usuario con ID {id_usuario} y registros relacionados eliminados exitosamente"}), 200

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
               
                sql = "SELECT COUNT(*) as conteo FROM usuario WHERE num_telefono = ?"
                cursor.execute(sql, (num_telefono,))
                result = resultados_a_json(cursor, unico_resultado=True)
                
                existe = result['conteo'] > 0
                id_usuario = None
                if existe:
                    sql_firebase ="""SELECT 
                u.id_usuario, u.id_usuario_firebase, u.rol,
                u.nombres, u.apellidos, u.correo_electronico, u.num_telefono,
                u.url_logo, u.coordenadas, u.created, u.lastUpdate,
                s.id_sucursal, d.id_distribuidor
            FROM usuario u
            LEFT JOIN usuario_sucursal s ON u.id_usuario = s.id_usuario
            LEFT JOIN usuario_distribuidor d ON u.id_usuario = d.id_usuario 
            WHERE u.num_telefono = ?;"""
                    cursor.execute(sql_firebase, (num_telefono,))
                    result_firebase = resultados_a_json(cursor, unico_resultado=True)
                   
                    id_usuario = result_firebase['id_usuario'] if result_firebase else None
                    return jsonify({"existe": existe, "data": result_firebase}), 200
                else:
                    id_usuario="No Existe"
                    return jsonify({"existe": existe, "id_usuario": id_usuario}), 200
                
        
    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500

@usuario_fl2.route('/<int:id_usuario>/favoritos', methods=['GET'])
def obtener_autos_favoritos_usuario(id_usuario): 
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                # Obtener todos los artículos favoritos
                sql = """
                    SELECT 
                        articulo.*, 
                        CAST(favoritos.enable AS INT) as favorite
                    FROM 
                        articulo
                    JOIN 
                        favoritos ON articulo.id_articulo = favoritos.id_articulo
                    WHERE 
                        favoritos.enable = 1 AND favoritos.id_usuario = ? 
                    ORDER BY 
                        articulo.id_articulo
                """
                cursor.execute(sql, (id_usuario,))
                articulos_raw = resultados_a_json(cursor)
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
                        WHERE especificaciones.id_articulo = ?
                    """
                    cursor.execute(sql_especificaciones, (id_articulo,))
                    especificaciones_raw = resultados_a_json(cursor)
                    
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
                        WHERE id_articulo = ?
                    """
                    cursor.execute(sql_imagenes, (id_articulo,))
                    imagenes = resultados_a_json(cursor)

                    # Agregar datos al artículo
                    articulo['especificaciones'] = list(especificaciones.values())
                    articulo['imagenes'] = imagenes

                    sql_sucursales = """
                            SELECT id_sucursal FROM articulo_sucursal
                            WHERE id_articulo = ?
                        """
                    cursor.execute(sql_sucursales, (id_articulo,))
                    sucursales = resultados_a_json(cursor)
                    
                    id_sucursales = sucursales[0]['id_sucursal']
                    sql_sucursal="""
                                SELECT direccion FROM sucursal WHERE id_sucursal =?
                        """
                    cursor.execute(sql_sucursal, (id_sucursales,))
                    sucursal_dir=resultados_a_json(cursor,unico_resultado=True)
                    articulo['direccion'] = sucursal_dir['direccion']
                    articulo['id_sucursal'] = id_sucursales
                    articulos_favoritos.append(articulo)

                return jsonify({"success": True, "autos_favoritos": articulos_favoritos}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
