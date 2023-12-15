from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request

articulo_fl1=Blueprint('articulo_id', __name__)

async def get_articulo(connection, id_articulo):
    try:
        async with connection.cursor() as cursor:
            sql_articulo = """
                SELECT a.*, 
                       e.id_especificacion, e.tipo, e.nombre_especificacion, e.valor_especificacion,
                       img.url_image, img.descripcion as img_descripcion
                FROM articulo a
                LEFT JOIN especificaciones_articulo e ON a.id_articulo = e.id_articulo
                LEFT JOIN images_articulo img ON a.id_articulo = img.id_articulo
                WHERE a.id_articulo = %s
            """
            await cursor.execute(sql_articulo, (id_articulo,))
            raw_results = await cursor.fetchall()

            if not raw_results:
                return None  # No se encontró el artículo

            articulo_resultado = {
                'id_articulo': raw_results[0]['id_articulo'],
                'marca': raw_results[0]['marca'],
                'modelo': raw_results[0]['modelo'],
                'categoria': raw_results[0]['categoria'],
                'ano': raw_results[0]['ano'],
                'precio': raw_results[0]['precio'],
                'kilometraje': raw_results[0]['kilometraje'],
                'created': raw_results[0]['created'],
                'lastUpdate': raw_results[0]['lastUpdate'],
                'lastInventoryUpdate': raw_results[0]['lastInventoryUpdate'],
                'enable': raw_results[0]['enable'],
                'descripcion': raw_results[0]['descripcion'],
                'enable': raw_results[0]['enable'],
                'color': raw_results[0]['color'],        
                'especificaciones': [],
                'imagenes': []
            }

            for row in raw_results:
                if row['id_especificacion'] and not any(e['id_especificacion'] == row['id_especificacion'] for e in articulo_resultado['especificaciones']):
                    especificacion = {
                        'id_especificacion': row['id_especificacion'],
                        'nombre_especificacion': row['nombre_especificacion'],
                        'valor_especificacion': row['valor_especificacion'],
                    }
                    articulo_resultado['especificaciones'].append(especificacion)

                if row['url_image'] and not any(img['url_image'] == row['url_image'] for img in articulo_resultado['imagenes']):
                    imagen = {
                        'url_image': row['url_image'],
                        'descripcion': row['img_descripcion'],
                    }
                    articulo_resultado['imagenes'].append(imagen)

            return articulo_resultado
    finally:
        connection.close()

    
@articulo_fl1.route('/<int:articulo_id>', methods=['GET'])
async def get_articulo_by_id(articulo_id):
    async with connect_to_database() as con:
        try:
            articulo_by_id= await get_articulo(con,articulo_id)
            if articulo_by_id:
                return jsonify({"success": True, "data": articulo_by_id})
            else:
                return jsonify({"error": f"articulo with ID {articulo_id} not found"}), 404
        except Exception as e :
            return jsonify({"error":"Data Base erorr {}".format(e)})