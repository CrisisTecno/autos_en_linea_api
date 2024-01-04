from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request
from .usuario_id import usuario_fl1
from .usuario_methods import usuario_fl2
import datetime

usuario_fl = Blueprint('usuario', __name__)
usuario_fl.register_blueprint(usuario_fl1,)
usuario_fl.register_blueprint(usuario_fl2,)

async def process_usuario(connection):
    try:
        async with connection.cursor() as cursor:
            sql_sucursal = """SELECT * FROM usuario;"""
            await cursor.execute(sql_sucursal)
            usuario_results = await cursor.fetchall()
            
            for usuario_record in usuario_results:
                for key, value in usuario_record.items():
                    if isinstance(value, datetime.datetime):
                        usuario_record[key] = int(value.timestamp() * 1000)
            return usuario_results
    finally:
        connection.close()

# @usuario_fl2.route('/favoritos/<int:id_usuario>', methods=['GET'])
# async def obtener_todos_autos_favoritos_usuario(id_usuario): 
#     try:
#         async with connect_to_database() as connection:
#             async with connection.cursor() as cursor:
#                 sql = """
#                     SELECT articulo.*, favoritos.enable as favorite FROM articulo
#                     JOIN favoritos ON articulo.id_articulo = favoritos.id_articulo
#                 """
#                 await cursor.execute(sql)
#                 autos_favoritos = await cursor.fetchall()
#                 if not autos_favoritos:
#                     return jsonify({"error": f"No se encontraron autos favoritos para el usuario con ID {id_usuario}"}), 404

#                 return jsonify({"success": True, "autos_favoritos": autos_favoritos}), 200

#     except Exception as e:
#         return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    
# @usuario_fl2.route('/favoritos/<int:id_usuario>', methods=['GET'])
# async def obtener_todos_autos_favoritos_usuario(id_usuario): 
#     try:
#         async with connect_to_database() as connection:
#             async with connection.cursor() as cursor:
#                 # Consultar todos los artículos y marcar los favoritos
#                 sql = """
#                     SELECT 
#                         articulo.*, 
#                         CASE WHEN fav.id_usuario IS NOT NULL THEN 1 ELSE 0 END as favorite
#                     FROM 
#                         articulo
#                     LEFT JOIN 
#                         (SELECT * FROM favoritos WHERE id_usuario = %s) as fav 
#                     ON articulo.id_articulo = fav.id_articulo
#                 """
#                 await cursor.execute(sql, (id_usuario,))
#                 autos = await cursor.fetchall()

#                 if not autos:
#                     return jsonify({"error": "No se encontraron autos"}), 404

#                 return jsonify({"success": True, "autos": autos}), 200

#     except Exception as e:
#         return jsonify({"error": f"Error en la base de datos: {e}"}), 500
@usuario_fl2.route('/favoritos/<int:id_usuario>', methods=['GET'])
async def obtener_todos_autos_favoritos_usuario(id_usuario): 
    try:
        async with connect_to_database() as connection:
            async with connection.cursor() as cursor:
                # Consultar todos los artículos y marcar los que son favoritos
                sql = """
                    SELECT 
                        a.*, 
                        CASE WHEN fav.id_articulo IS NOT NULL THEN 1 ELSE 0 END as favorite
                    FROM 
                        articulo a
                    LEFT JOIN 
                        (SELECT id_articulo FROM favoritos WHERE id_usuario = %s AND enable = 1) as fav 
                    ON a.id_articulo = fav.id_articulo
                """
                await cursor.execute(sql, (id_usuario,))
                autos_all = await cursor.fetchall()

                if not autos_all:
                    return jsonify({"error": "No se encontraron autos"}), 404

                autos = []
                for articulo in autos_all:
                    id_articulo = articulo['id_articulo']
                    sql_especificaciones = """
                        SELECT especificaciones.*, subespecificaciones.clave, subespecificaciones.valor
                        FROM especificaciones
                        LEFT JOIN subespecificaciones ON especificaciones.id_especificacion = subespecificaciones.id_especificacion
                        WHERE especificaciones.id_articulo = %s
                    """
                    await cursor.execute(sql_especificaciones, (id_articulo,))
                    especificaciones_raw = await cursor.fetchall()
                    
                    especificaciones = {}
                    for esp in especificaciones_raw:
                        id_esp = esp['id_especificacion']
                        if id_esp not in especificaciones:
                            especificaciones[id_esp] = {'tipo': esp['tipo'], 'subespecificaciones': {}}
                        especificaciones[id_esp]['subespecificaciones'][esp['clave']] = esp['valor']
                    sql_imagenes = """
                        SELECT url_image, descripcion
                        FROM images_articulo
                        WHERE id_articulo = %s
                    """
                    await cursor.execute(sql_imagenes, (id_articulo,))
                    imagenes = await cursor.fetchall()
                    articulo['especificaciones'] = list(especificaciones.values())
                    articulo['imagenes'] = imagenes
                    autos.append(articulo)

                return jsonify({"success": True, "autos_favoritos": autos}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500

    
@usuario_fl.route('/', methods=['GET'])
async def get_pedidos_proveedor():
    async with connect_to_database() as connection:
        try:
            usuarios = await process_usuario(connection)
            return jsonify({"success": True, "data": usuarios})
        except Exception as e:
            return jsonify({"error": "Database error: {}".format(e)}), 500