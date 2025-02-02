from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request
from .usuario_id import usuario_fl1
from .usuario_methods import usuario_fl2
import datetime

from utils.serializer import resultados_a_json, convertir_a_datetime

usuario_fl = Blueprint('usuario', __name__)
usuario_fl.register_blueprint(usuario_fl1,)
usuario_fl.register_blueprint(usuario_fl2,)


def process_usuario(connection):
    try:
        with connection.cursor() as cursor:
            sql_usuario = """SELECT 
                u.id_usuario, u.id_usuario_firebase, u.rol,
                u.nombres, u.apellidos, u.correo_electronico, u.num_telefono,
                u.url_logo, u.coordenadas, u.created, u.lastUpdate,
                s.id_sucursal, d.id_distribuidor
            FROM usuario u
            LEFT JOIN usuario_sucursal s ON u.id_usuario = s.id_usuario
            LEFT JOIN usuario_distribuidor d ON u.id_usuario = d.id_usuario;"""
            cursor.execute(sql_usuario)
            usuario_results = resultados_a_json(cursor)
            

            
            return usuario_results
    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


@usuario_fl2.route('/favoritos/<int:id_usuario>', methods=['GET'])
def obtener_todos_autos_favoritos_usuario(id_usuario): 
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                # Consultar todos los artículos y marcar los que son favoritos
                sql = """
                    SELECT 
                        a.*, 
                        CASE WHEN fav.id_articulo IS NOT NULL THEN 1 ELSE 0 END as favorite
                    FROM 
                        articulo a
                    LEFT JOIN 
                        (SELECT id_articulo FROM favoritos WHERE id_usuario = ? AND enable = 1) as fav 
                    ON a.id_articulo = fav.id_articulo
                """
                cursor.execute(sql, (id_usuario,))
                autos_all = resultados_a_json(cursor)
                print(autos_all)
                if not autos_all:
                    return jsonify({"error": "No se encontraron autos favoritos"}), 404

                autos = []
                for articulo in autos_all:
                    id_articulo = articulo['id_articulo']
                    sql_especificaciones = """
                        SELECT especificaciones.*, subespecificaciones.clave, subespecificaciones.valor
                        FROM especificaciones
                        LEFT JOIN subespecificaciones ON especificaciones.id_especificacion = subespecificaciones.id_especificacion
                        WHERE especificaciones.id_articulo = ?
                    """
                    cursor.execute(sql_especificaciones, (id_articulo,))
                    especificaciones_raw = resultados_a_json(cursor)
                    
                    especificaciones = {}
                    for esp in especificaciones_raw:
                        id_esp = esp['id_especificacion']
                        if id_esp not in especificaciones:
                            especificaciones[id_esp] = {'tipo': esp['tipo'], 'subespecificaciones': {}}
                        especificaciones[id_esp]['subespecificaciones'][esp['clave']] = esp['valor']
                    sql_imagenes = """
                        SELECT url_image, descripcion
                        FROM images_articulo
                        WHERE id_articulo = ?
                    """
                    cursor.execute(sql_imagenes, (id_articulo,))
                    imagenes = resultados_a_json(cursor)
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
                    autos.append(articulo)

                return jsonify({"success": True, "autos_favoritos": autos}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500

    
@usuario_fl.route('/', methods=['GET'])
def get_pedidos_proveedor():
    with connect_to_database() as connection:
        try:
            usuarios = process_usuario(connection)
            return jsonify({"success": True, "data": usuarios})
        except Exception as e:
            return jsonify({"error": "Database error: {}".format(e)}), 500