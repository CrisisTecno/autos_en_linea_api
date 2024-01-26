from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request
from utils.time import convert_milliseconds_to_datetime,convert_milliseconds_to_time_string
from utils.time import convert_milliseconds_to_datetime,convert_milliseconds_to_time_string,timedelta_to_milliseconds,unix_to_datetime
from utils.serializer import resultados_a_json, convertir_a_datetime

distribuidor_fl2=Blueprint('distribuidor_methods', __name__)

@distribuidor_fl2.route('/distribuidor', methods=['POST'])
def crear_distribuidor():
    try:
        with connect_to_database() as connection:
            data = request.json
            campos_requeridos = [
                'gerente', 'logo_image', 'coordenadas' ,'direccion',
                'nombre', 'url_paginaWeb', 'telefono', 'email', 'horarioAtencion','created','lastUpdate'
            ]

            if not all(campo in data for campo in campos_requeridos) or not all(dia in data['horarioAtencion'] for dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']):

                return jsonify({"error": "Faltan campos requeridos"}), 400

            with connection.cursor() as cursor:
                sql_distribuidor = """
                        INSERT INTO distribuidor (
                            gerente, logo_image, coordenadas, direccion,
                            nombre, url_paginaWeb, telefono, email, created, lastUpdate
                        )
                        OUTPUT INSERTED.id_distribuidor
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """
                valores_distribuidor = (
                    data['gerente'],
                    data['logo_image'],
                    data['coordenadas'],
                    data['direccion'],
                    data['nombre'],
                    data['url_paginaWeb'],
                    data['telefono'],
                    data['email'],
                    unix_to_datetime(data['created']),
                    unix_to_datetime(data['lastUpdate'])
                )
                cursor.execute(sql_distribuidor, valores_distribuidor)
                id_distribuidor = cursor.fetchone()[0]

                if 'sucursales' in data and isinstance(data['sucursales'], list):
                    for id_sucursal in data['sucursales']:
                        sql_distribuidor_sucursal = """INSERT INTO distribuidor_sucursal (id_distribuidor, id_sucursal)
                                                       VALUES (?, ?)"""
                        cursor.execute(sql_distribuidor_sucursal, (id_distribuidor, id_sucursal))

                if 'marcas' in data and isinstance(data['marcas'], list):
                    for marca in data['marcas']:
                        sql_marca_distribuidor = """INSERT INTO marcas_distribuidor (marca, id_distribuidor)
                                                    VALUES (?, ?)"""
                        cursor.execute(sql_marca_distribuidor, (marca, id_distribuidor))

                for dia, horarios in data['horarioAtencion'].items():
                    open_time = convert_milliseconds_to_time_string(horarios['open'])
                    close_time = convert_milliseconds_to_time_string(horarios['close'])
                    sql_horarios = """INSERT INTO horarios_distribuidor (id_distribuidor, day, [open], [close])
                                      VALUES (?, ?, ?, ?)"""
                    cursor.execute(sql_horarios, (id_distribuidor, dia, open_time, close_time))

                connection.commit()

            return jsonify({"success": True, "message": "Distribuidor creado exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
from flask import request, jsonify

# @distribuidor_fl2.route('/distribuidor/<int:id_distribuidor>', methods=['PUT'])
# def actualizar_distribuidor(id_distribuidor):
#     try:
#         with connect_to_database() as connection:
#             data = request.json
#             campos_permitidos = [
#                 'gerente', 'logo_image', 'coordenadas' ,'direccion',
#                 'nombre', 'url_paginaWeb', 'telefono', 'email', 'lastUpdate','horarioAtencion'
#             ]

#             if not any(campo in data for campo in campos_permitidos):
#                 return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400
            
#             # for dia, horarios in data['horarioAtencion'].items():
#             #             print(dia)
#             #             print(horarios)
#             #             print(horarios['open'])
#             #             print(type(horarios['open']))
#             with connection.cursor() as cursor:
#                 # Actualizar la información principal del distribuidor
#                 sql_update_distribuidor = """UPDATE distribuidor
#                                              SET gerente = ?, logo_image = ?, coordenadas = ?,
#                                                  direccion = ?, nombre = ?, url_paginaWeb = ?,
#                                                  telefono = ?, email = ?, lastUpdate = ?
#                                              WHERE id_distribuidor = ?"""
#                 valores_distribuidor = (
#                     data.get('gerente'),
#                     data.get('logo_image'),
#                     data.get('coordenadas'),
#                     data.get('direccion'),
#                     data.get('nombre'),
#                     data.get('url_paginaWeb'),
#                     data.get('telefono'),
#                     data.get('email'),
#                     unix_to_datetime(data.get('lastUpdate')),
#                     id_distribuidor
#                 )
#                 cursor.execute(sql_update_distribuidor, valores_distribuidor)

#                 # Actualizar la relación con sucursales
#                 if 'sucursales' in data and isinstance(data['sucursales'], list):
#                     # Eliminar las relaciones existentes
#                     sql_delete_relaciones_sucursal = "DELETE FROM distribuidor_sucursal WHERE id_distribuidor = ?"
#                     cursor.execute(sql_delete_relaciones_sucursal, (id_distribuidor,))
                    
#                     # Agregar las nuevas relaciones
#                     for id_sucursal in data['sucursales']:
#                         sql_distribuidor_sucursal = """INSERT INTO distribuidor_sucursal (id_distribuidor, id_sucursal)
#                                                        VALUES (?, ?)"""
#                         cursor.execute(sql_distribuidor_sucursal, (id_distribuidor, id_sucursal))

#                 # Actualizar la relación con marcas
#                 if 'marcas' in data and isinstance(data['marcas'], list):
#                     # Eliminar las relaciones existentes
#                     sql_delete_relaciones_marcas = "DELETE FROM marcas_distribuidor WHERE id_distribuidor = ?"
#                     cursor.execute(sql_delete_relaciones_marcas, (id_distribuidor,))
                    
#                     # Agregar las nuevas relaciones
#                     for marca in data['marcas']:
#                         sql_marca_distribuidor = """INSERT INTO marcas_distribuidor (marca, id_distribuidor)
#                                                     VALUES (?, ?)"""
#                         cursor.execute(sql_marca_distribuidor, (marca, id_distribuidor))

#                 # Actualizar los horarios de atención
#                 # if 'horarioAtencion' in data:
#                 #     for dia, horarios in data['horarioAtencion'].items():
#                 #         open_time = convert_milliseconds_to_time_string(horarios['open'])
#                 #         print(open_time)
#                 #         close_time = convert_milliseconds_to_time_string(horarios['close'])

#                 #         sql_update_horarios = """UPDATE horarios_distribuidor
#                 #                                  SET [open] = ?, [close] = ?
#                 #                                  WHERE id_distribuidor = ? AND day = ?"""
#                 #         cursor.execute(sql_update_horarios, (open_time, close_time, id_distribuidor, dia))
#                 if 'horarioAtencion' in data:
#                     print("entra aca we")
#                     for dia, horarios in data['horarioAtencion'].items():
#                         print(dia)
#                         print(horarios)
#                         print(horarios['open'])
#                         open_time = convert_milliseconds_to_time_string(horarios['open'])
#                         close_time = convert_milliseconds_to_time_string(horarios['close'])
#                         sql_update_horarios = """UPDATE horarios_distribuidor
#                                                 SET [open] = ?, [close] = ?
#                                                 WHERE id_distribuidor = ? AND day = ?"""
#                         cursor.execute(sql_update_horarios, (open_time, close_time, id_distribuidor, dia))

#                 # if 'horarioAtencion' in data:
#                 #     for dia, horarios in data['horarioAtencion'].items():
#                 #         open_time = convert_milliseconds_to_time_string(horarios.get('open', 0)) if 'open' in horarios else None
#                 #         close_time = convert_milliseconds_to_time_string(horarios.get('close', 0)) if 'close' in horarios else None
#                 #         if open_time is not None and close_time is not None:
#                 #             sql_update_horarios = """UPDATE horarios_distribuidor
#                 #                                     SET [open] = ?, [close] = ?
#                 #                                     WHERE id_distribuidor = ? AND day = ?"""
#                 #             cursor.execute(sql_update_horarios, (open_time, close_time, id_distribuidor, dia))


#                 connection.commit()

#             return jsonify({"success": True, "message": f"Distribuidor con ID {id_distribuidor} actualizado exitosamente"}), 200

#     except Exception as e:
#         return jsonify({"error": f"Error en la base de datos: {e}"}), 500

@distribuidor_fl2.route('/distribuidor/<int:id_distribuidor>', methods=['PUT'])
def actualizar_distribuidor(id_distribuidor):
    try:
        with connect_to_database() as connection:
            data = request.json
            campos_permitidos = [
                'gerente', 'logo_image', 'coordenadas', 'direccion',
                'nombre', 'url_paginaWeb', 'telefono', 'email', 'horarioAtencion','marcas','lastUpdate','created'
            ]

            if not any(campo in data for campo in campos_permitidos):
                return jsonify({"error": "Se requiere al menos un campo para actualizar"}), 400
            
            with connection.cursor() as cursor:
                sql_update = "UPDATE distribuidor SET "
                valores = []
                existee=False
                for campo in campos_permitidos:
                    if campo in data and campo!='horarioAtencion' and campo!='marcas':
                        valor = data[campo]
                        existee=True
                        if campo in ['created', 'lastUpdate']:
                            valor = unix_to_datetime(valor)
                        sql_update += f"{campo} = ?, "
                        valores.append(valor)

                if existee:
                    sql_update = sql_update.rstrip(', ')
                    sql_update += " WHERE id_distribuidor = ?"
                    valores.append(id_distribuidor)
                    cursor.execute(sql_update, valores)

                if 'marcas' in data:
                    print("osea sin entro we")
                    sql = "SELECT COUNT(*) as conteo FROM marcas_distribuidor WHERE id_distribuidor = ?;"
                    cursor.execute(sql, (id_distribuidor,))
                    result = resultados_a_json(cursor, unico_resultado=True)
                    
                    existe = result['conteo'] > 0
                    if existe:

                        sql_delete_relaciones_marcas = "DELETE FROM marcas_distribuidor WHERE id_distribuidor = ?;"
                        cursor.execute(sql_delete_relaciones_marcas, (id_distribuidor,))
                    
                    for marca in data['marcas']:
                        sql_marca_distribuidor = """INSERT INTO marcas_distribuidor (marca, id_distribuidor)
                                                    VALUES (?, ?);"""
                        cursor.execute(sql_marca_distribuidor, (marca, id_distribuidor))

                if 'horarioAtencion' in data:
                    for dia, horarios in data['horarioAtencion'].items():
                        
                        open_time = convert_milliseconds_to_time_string(horarios['open'])
                        close_time = convert_milliseconds_to_time_string(horarios['close'])
                        sql_update_horarios = """UPDATE horarios_distribuidor
                                                SET [open] = ?, [close] = ?
                                                WHERE id_distribuidor = ? AND day = ?"""
                        cursor.execute(sql_update_horarios, (open_time, close_time, id_distribuidor, dia))

                
                connection.commit()

            return jsonify({"success": True, "message": f"Distribuidor con ID {id_distribuidor} actualizado exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


@distribuidor_fl2.route('/distribuidor/<int:id_distribuidor>', methods=['DELETE'])
def eliminar_distribuidor(id_distribuidor):
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                # Eliminar relaciones en distribuidor_sucursal
                sql_delete_distribuidor_sucursal = "DELETE FROM distribuidor_sucursal WHERE id_distribuidor = ?"
                cursor.execute(sql_delete_distribuidor_sucursal, (id_distribuidor,))

                sql_delete_marcas_distribuidor = "DELETE FROM marcas_distribuidor WHERE id_distribuidor = ?"
                cursor.execute(sql_delete_marcas_distribuidor, (id_distribuidor,))

                sql_delete_horarios_distribuidor = "DELETE FROM horarios_distribuidor WHERE id_distribuidor = ?"
                cursor.execute(sql_delete_horarios_distribuidor, (id_distribuidor,))

                sql_delete_usuario_distribuidor = "DELETE FROM usuario_distribuidor WHERE id_distribuidor = ?"
                cursor.execute(sql_delete_usuario_distribuidor, (id_distribuidor,))

                sql_delete_distribuidor = "DELETE FROM distribuidor WHERE id_distribuidor = ?"
                cursor.execute(sql_delete_distribuidor, (id_distribuidor,))

                # Confirma todas las operaciones
                connection.commit()

            return jsonify({"success": True, "message": f"Distribuidor con ID {id_distribuidor} y registros relacionados eliminados exitosamente"}), 200

    except Exception as e:
        # En caso de un error, se hará rollback automáticamente si se está usando un gestor de transacciones
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


@distribuidor_fl2.route('/<int:id_distribuidor>/usuarios', methods=['GET'])
def obtener_usuarios_por_distribuidor(id_distribuidor):
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
            WHERE d.id_distribuidor = ?;"""
                # sql = """
                #     SELECT *  FROM usuario
                #     WHERE id_distribuidor = ?
                # """
                cursor.execute(sql, (id_distribuidor,))
                usuarios = resultados_a_json(cursor)


                if not usuarios:
                    return jsonify({"error": f"No se encontraron usuarios para el distribuidor con ID {id_distribuidor}"}), 404

                return jsonify({"success": True, "usuarios": usuarios}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


@distribuidor_fl2.route('/<int:id_distribuidor>/articulos', methods=['GET'])
def obtener_articulos_por_distribuidor(id_distribuidor):
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                sql_query = """
                    SELECT a.*, asu.id_sucursal
                    FROM articulo a
                    JOIN articulo_sucursal asu ON a.id_articulo = asu.id_articulo
                    JOIN distribuidor_sucursal ds ON asu.id_sucursal = ds.id_sucursal
                    WHERE ds.id_distribuidor = ?;
                """
                cursor.execute(sql_query, (id_distribuidor,))
                articulos = resultados_a_json(cursor)
            
                articulos_procesados = []
                for articulo_record in articulos:
                    articulo_procesado = procesar_articulo(cursor, articulo_record['id_articulo'])
                    articulos_procesados.append(articulo_procesado)

                return jsonify({"success": True, "articulos": articulos_procesados}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    
@distribuidor_fl2.route('/<int:id_distribuidor>/articulos/<int:id_usuario>', methods=['GET'])
def obtener_articulos_por_distribuidor_favoritos(id_distribuidor,id_usuario):
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                sql_query = """
                    SELECT a.*, asu.id_sucursal
                    FROM articulo a
                    JOIN articulo_sucursal asu ON a.id_articulo = asu.id_articulo
                    JOIN distribuidor_sucursal ds ON asu.id_sucursal = ds.id_sucursal
                    WHERE ds.id_distribuidor = ?;
                """
                cursor.execute(sql_query, (id_distribuidor,))
                articulos = resultados_a_json(cursor)
                print(articulos)
                articulos_procesados = []
                for articulo_record in articulos:
                    articulo_procesado = procesar_articulo_fav(cursor, articulo_record['id_articulo'],id_usuario)
                    articulos_procesados.append(articulo_procesado)

                return jsonify({"success": True, "articulos": articulos_procesados}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500

def procesar_articulo_fav(cursor, id_articulo,id_usuario):

    sql_articulo = """
    SELECT 
        a.*, 
        asu.id_sucursal,
        e.id_especificacion, 
        e.tipo, 
        img.url_image, 
        img.descripcion as img_descripcion,
        CAST(CASE WHEN fav.id_articulo IS NOT NULL THEN 1 ELSE 0 END AS INT) as favorito
    FROM 
        articulo a
    JOIN 
        articulo_sucursal asu ON a.id_articulo = asu.id_articulo
    LEFT JOIN 
        especificaciones e ON a.id_articulo = e.id_articulo
    LEFT JOIN 
        images_articulo img ON a.id_articulo = img.id_articulo
    LEFT JOIN 
        (SELECT id_articulo FROM favoritos WHERE id_usuario = ? AND enable = 1) as fav
    ON 
        a.id_articulo = fav.id_articulo
    WHERE 
        a.id_articulo = ?
"""

# Luego ejecutas la consulta pasando los parámetros necesarios
    cursor.execute(sql_articulo, (id_usuario, id_articulo))

    resultados_crudos = resultados_a_json(cursor)
    
    if not resultados_crudos:
        return None
    articulo_resultado = {
        'id_articulo': resultados_crudos[0]['id_articulo'],
        'favorite': resultados_crudos[0]['favorito'],
        'id_sucursal': resultados_crudos[0]['id_sucursal'],
        'marca': resultados_crudos[0]['marca'],
        'modelo': resultados_crudos[0]['modelo'],
        'categoria': resultados_crudos[0]['categoria'],
        'ano': resultados_crudos[0]['ano'],
        'precio': resultados_crudos[0]['precio'],
        'kilometraje': resultados_crudos[0]['kilometraje'],
        'created': resultados_crudos[0]['created'],
        'lastUpdate': resultados_crudos[0]['lastUpdate'],
        'lastInventoryUpdate': resultados_crudos[0]['lastInventoryUpdate'],
        'enable': resultados_crudos[0]['enable'],
        'descripcion': resultados_crudos[0]['descripcion'],
        'color': resultados_crudos[0]['color'],
        'mainImage': resultados_crudos[0]['mainImage'],
        'especificaciones': [],
        'imagenes': []
    }

    ids_especificaciones_procesadas = set()
    for fila in resultados_crudos:
        id_especificacion = fila.get('id_especificacion')
        if id_especificacion and id_especificacion not in ids_especificaciones_procesadas:
            ids_especificaciones_procesadas.add(id_especificacion)
            sql_subespecificaciones = """
                SELECT * FROM subespecificaciones
                WHERE id_especificacion = ?
            """
            cursor.execute(sql_subespecificaciones, (id_especificacion,))
            subespecificaciones_raw = resultados_a_json(cursor)
            subespecificaciones = {sub['clave']: sub['valor'] for sub in subespecificaciones_raw}

            especificacion = {
                'tipo': fila['tipo'],
                'subespecificaciones': subespecificaciones
            }
            articulo_resultado['especificaciones'].append(especificacion)

        if fila['url_image'] and not any(imagen['url_image'] == fila['url_image'] for imagen in articulo_resultado['imagenes']):
            imagen = {
                'url_image': fila['url_image'],
                'descripcion': fila['img_descripcion'],
            }
            articulo_resultado['imagenes'].append(imagen)
        sql_sucursal="""
                                SELECT direccion FROM sucursal WHERE id_sucursal =?
                        """
        cursor.execute(sql_sucursal, (resultados_crudos[0]['id_sucursal']))
        sucursal_dir=resultados_a_json(cursor,unico_resultado=True)
        articulo_resultado['direccion'] = sucursal_dir['direccion']
    return articulo_resultado

def procesar_articulo(cursor, id_articulo):
    sql_articulo = """
        SELECT a.*, asu.id_sucursal,
            e.id_especificacion, e.tipo,
            img.url_image, img.descripcion as img_descripcion
            
        FROM articulo a
        JOIN articulo_sucursal asu ON a.id_articulo = asu.id_articulo
        LEFT JOIN especificaciones e ON a.id_articulo = e.id_articulo
        LEFT JOIN images_articulo img ON a.id_articulo = img.id_articulo
        WHERE a.id_articulo = ?
    """
    cursor.execute(sql_articulo, (id_articulo,))
    resultados_crudos = resultados_a_json(cursor)
    if not resultados_crudos:
        return None
    articulo_resultado = {
        'id_articulo': resultados_crudos[0]['id_articulo'],
        'id_sucursal': resultados_crudos[0]['id_sucursal'],
        'marca': resultados_crudos[0]['marca'],
        'modelo': resultados_crudos[0]['modelo'],
        'categoria': resultados_crudos[0]['categoria'],
        'ano': resultados_crudos[0]['ano'],
        'precio': resultados_crudos[0]['precio'],
        'kilometraje': resultados_crudos[0]['kilometraje'],
        'created': resultados_crudos[0]['created'],
        'lastUpdate': resultados_crudos[0]['lastUpdate'],
        'lastInventoryUpdate': resultados_crudos[0]['lastInventoryUpdate'],
        'enable': resultados_crudos[0]['enable'],
        'descripcion': resultados_crudos[0]['descripcion'],
        'color': resultados_crudos[0]['color'],
        'mainImage': resultados_crudos[0]['mainImage'],
        'especificaciones': [],
        'imagenes': []
    }

    ids_especificaciones_procesadas = set()
    for fila in resultados_crudos:
        id_especificacion = fila.get('id_especificacion')
        if id_especificacion and id_especificacion not in ids_especificaciones_procesadas:
            ids_especificaciones_procesadas.add(id_especificacion)
            sql_subespecificaciones = """
                SELECT * FROM subespecificaciones
                WHERE id_especificacion = ?
            """
            cursor.execute(sql_subespecificaciones, (id_especificacion,))
            subespecificaciones_raw = resultados_a_json(cursor)
            subespecificaciones = {sub['clave']: sub['valor'] for sub in subespecificaciones_raw}

            especificacion = {
                'tipo': fila['tipo'],
                'subespecificaciones': subespecificaciones
            }
            articulo_resultado['especificaciones'].append(especificacion)

        if fila['url_image'] and not any(imagen['url_image'] == fila['url_image'] for imagen in articulo_resultado['imagenes']):
            imagen = {
                'url_image': fila['url_image'],
                'descripcion': fila['img_descripcion'],
            }
            articulo_resultado['imagenes'].append(imagen)

    return articulo_resultado

@distribuidor_fl2.route('/<int:id_distribuidor>/sucursales', methods=['GET'])
def obtener_sucursales_por_distribuidor(id_distribuidor):
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                sql_query = """
                    SELECT s.*
                    FROM distribuidor_sucursal ds
                    JOIN sucursal s ON ds.id_sucursal = s.id_sucursal
                    WHERE ds.id_distribuidor = ?;
                """
                cursor.execute(sql_query, (id_distribuidor,))
                sucursales_raw = resultados_a_json(cursor)

                sucursales_processed = []
                for sucursal_record in sucursales_raw:
                    id_sucursal = sucursal_record['id_sucursal']


                    sql_sucursales_imagenes = "SELECT * FROM images_sucursal WHERE id_sucursal = ?;"
                    cursor.execute(sql_sucursales_imagenes, (id_sucursal,))
                    sucursal_images = resultados_a_json(cursor)
                    sucursal_record['sucursal_images'] = sucursal_images

                    sql_articulos = """
                        SELECT articulo.* FROM articulo
                        JOIN articulo_sucursal ON articulo.id_articulo = articulo_sucursal.id_articulo
                        WHERE articulo_sucursal.id_sucursal = ?;
                    """
                    cursor.execute(sql_articulos, (id_sucursal,))
                    articulos_list = resultados_a_json(cursor)


                    sucursal_record['sucursal_articulos'] = articulos_list

                    sql_horarios_sucursal = "SELECT * FROM horarios_sucursal WHERE id_sucursal = ?"
                    cursor.execute(sql_horarios_sucursal, (id_sucursal,))
                    horarios_raw = resultados_a_json(cursor)
                    horarios_sucursal = {}
                    for horario in horarios_raw:
                        dia = horario['day']
                        horarios_sucursal[dia] = {
                            'open': timedelta_to_milliseconds(horario['open']),
                            'close':timedelta_to_milliseconds(horario['close'])
                        }

                    sucursal_record['horarios_sucursal'] = horarios_sucursal
                    sucursal_record['id_distribuidor']=id_distribuidor
                    sucursales_processed.append(sucursal_record)

            return jsonify(sucursales_processed)
    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


