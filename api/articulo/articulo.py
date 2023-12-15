from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request
from .articulo_id import articulo_fl1
from .articulo_methods import articulo_fl2
from .images_articulo.images_articulo import articulo_fl3


articulo_fl = Blueprint('articulo', __name__)

articulo_fl.register_blueprint(articulo_fl1,)
articulo_fl.register_blueprint(articulo_fl2,)
articulo_fl.register_blueprint(articulo_fl3,)

async def get_articulos(connection):
    try:
        async with connection.cursor() as cursor:
            sql_articulo =  """
        SELECT a.*, 
               e.id_especificacion, e.tipo, e.nombre_especificacion, e.valor_especificacion,
               img.url_image, img.descripcion as img_descripcion
        FROM articulo a
        LEFT JOIN especificaciones_articulo e ON a.id_articulo = e.id_articulo
        LEFT JOIN images_articulo img ON a.id_articulo = img.id_articulo
        ORDER BY a.id_articulo
    """
            await cursor.execute(sql_articulo)
            raw_results = await cursor.fetchall()
            articulo_results = {}
            for row in raw_results:
                id_articulo = row['id_articulo']
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
                        'especificaciones': [],
                        'imagenes': []
                    }

                id_especificacion = row.get('id_especificacion')
                nombre_especificacion = row.get('nombre_especificacion')
                valor_especificacion = row.get('valor_especificacion')
                if id_especificacion and not any(e['id_especificacion'] == id_especificacion for e in articulo_results[id_articulo]['especificaciones']):
                    especificacion = {
                        'id_especificacion': id_especificacion,
                        'nombre_especificacion': nombre_especificacion,
                        'valor_especificacion': valor_especificacion,
                    }
                    articulo_results[id_articulo]['especificaciones'].append(especificacion)

                # Procesar imágenes
                url_image = row.get('url_image')
                descripcion = row.get('descripcion')
                if url_image and not any(img['url_image'] == url_image for img in articulo_results[id_articulo]['imagenes']):
                    imagen = {
                        'url_image': url_image,
                        'descripcion': descripcion,
                    }
                    articulo_results[id_articulo]['imagenes'].append(imagen)
            return list(articulo_results.values())
    finally:
        connection.close()


    
@articulo_fl.route('/', methods=['GET'])
async def get_articulos_all():
    async with connect_to_database() as connection:
        try:
            # Obtener información de los pedidos del proveedor
            articulo = await get_articulos(connection)
            return jsonify({"success": True, "data": articulo})
        except Exception as e:
            return jsonify({"error": "Database error: {}".format(e)}), 500