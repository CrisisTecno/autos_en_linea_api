from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request
from .articulo_id import articulo_fl1
from .articulo_methods import articulo_fl2
from .images_articulo.images_articulo import articulo_fl3
from utils.serializer import resultados_a_json, convertir_a_datetime





articulo_fl = Blueprint('articulo', __name__)

articulo_fl.register_blueprint(articulo_fl1,)
articulo_fl.register_blueprint(articulo_fl2,)
articulo_fl.register_blueprint(articulo_fl3,)

def get_articulos(connection):
    try:
        with connection.cursor() as cursor:
            sql_articulo =  """
            SELECT a.*, 
                e.id_especificacion, e.tipo, 
                img.url_image, img.descripcion as img_descripcion
            FROM articulo a
            LEFT JOIN especificaciones e ON a.id_articulo = e.id_articulo
            LEFT JOIN images_articulo img ON a.id_articulo = img.id_articulo
            ORDER BY a.id_articulo
        """
            cursor.execute(sql_articulo)
            raw_results = resultados_a_json(cursor)
            # print(raw_results)
            articulo_results = {}
            processed_especificaciones = set()
            for row in raw_results:
                id_articulo = row['id_articulo']
                # print(id_articulo)
                id_especificacion = row.get('id_especificacion')
                if id_articulo not in articulo_results:
                    articulo_results[id_articulo] = {
                        'id_articulo': id_articulo,
                        'marca': row['marca'],
                        'modelo': row['modelo'],
                        'categoria': row['categoria'],
                        'ano': row['ano'],
                        'precio': row['precio'],
                        'kilometraje': row['kilometraje'],
                        'created': row['created'],
                        'lastUpdate': row['lastUpdate'],
                        'lastInventoryUpdate': row['lastInventoryUpdate'],
                        'enable': row['enable'],
                        'descripcion': row['descripcion'],
                        'enable': row['enable'],
                        'color': row['color'],
                        'mainImage': row['mainImage'],
                        'especificaciones': [],
                        'imagenes': []
                    }

                if id_especificacion and id_especificacion not in processed_especificaciones:
                    processed_especificaciones.add(id_especificacion)

                    sql_subespecificaciones = """
                        SELECT * FROM subespecificaciones
                        WHERE id_especificacion = ?
                    """
                    cursor.execute(sql_subespecificaciones, (id_especificacion,))
                    subespecificaciones_raw = resultados_a_json(cursor)

                    subespecificaciones = {sub['clave']: sub['valor'] for sub in subespecificaciones_raw}
                    especificacion = {
                        'tipo': row['tipo'],
                        'subespecificaciones': subespecificaciones
                    }
                    articulo_results[id_articulo]['especificaciones'].append(especificacion)

                url_image = row.get('url_image')
                descripcion = row.get('descripcion')
                if url_image and not any(img['url_image'] == url_image for img in articulo_results[id_articulo]['imagenes']):
                    imagen = {
                            'url_image': url_image,
                            'descripcion': descripcion,
                    }
                    articulo_results[id_articulo]['imagenes'].append(imagen)

                sql_sucursales = """
                            SELECT id_sucursal FROM articulo_sucursal
                            WHERE id_articulo = ?
                        """
                cursor.execute(sql_sucursales, (id_articulo,))
                sucursales = resultados_a_json(cursor)
                
                id_sucursales = sucursales[0]['id_sucursal']

                sql_distribuidor = """
                    SELECT id_distribuidor
                    FROM distribuidor_sucursal
                    WHERE id_sucursal = ?
                """
                cursor.execute(sql_distribuidor, (id_sucursales,))
                resultados_distribuidor = resultados_a_json(cursor)

                if resultados_distribuidor:
                    id_distribuidor = resultados_distribuidor[0]['id_distribuidor']
                else:
                    id_distribuidor = 0

                sql_sucursal="""
                            SELECT direccion FROM sucursal WHERE id_sucursal =?
                    """
                cursor.execute(sql_sucursal, (id_sucursales,))
                sucursal_dir=resultados_a_json(cursor,unico_resultado=True)

                articulo_results[id_articulo]['direccion'] = sucursal_dir['direccion']
                articulo_results[id_articulo]['id_sucursal'] = id_sucursales
                articulo_results[id_articulo]['id_distribuidor'] = id_distribuidor
                
                    
            return list(articulo_results.values())
    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


    
@articulo_fl.route('/', methods=['GET'])
def get_articulos_all():
    try:
        with connect_to_database() as connection:
          
            articulo = get_articulos(connection)
            return jsonify({"success": True, "data": articulo})
    except Exception as e:
        return jsonify({"error": "Database error: {}".format(e)}), 500
        

