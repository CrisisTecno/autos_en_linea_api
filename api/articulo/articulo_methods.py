from flask import Flask, request, jsonify
from flask import Blueprint
from config.database import connect_to_database
from utils.time import convert_milliseconds_to_datetime,unix_to_datetime,convert_milliseconds_to_time_string
from utils.coordenadas import obtener_sucursales_cercanas
from datetime import datetime
articulo_fl2 = Blueprint('articulo_post', __name__)
from utils.serializer import resultados_a_json, convertir_a_datetime


def get_default_expedition_date():
    now = datetime.now()
    timestamp_seconds = datetime.timestamp(now)
    timestamp_milliseconds = int(timestamp_seconds * 1000)
    return timestamp_milliseconds

@articulo_fl2.route('/articulo', methods=['POST'])
def crear_articulo():
    try:
        with connect_to_database() as connection:
            data = request.json
            expedition_date = data['expedition_date'] if 'expedition_date' in data else get_default_expedition_date()
            campos_requeridos = ['ano', 'categoria', 'color', 
                                 'descripcion', 'enable', 'mainImage', 'marca', 
                                 'modelo','precio','created',
                                 'lastUpdate','lastInventoryUpdate','kilometraje','sucursal_id','especificaciones','imagenes']   
            if not all(campo in data for campo in campos_requeridos):
                return jsonify({"error": "Faltan campos requeridos"}), 400
                
            with connection.cursor() as cursor:
                sql_articulo = """INSERT INTO articulo (
                                      ano, categoria, color, descripcion, [enable], mainImage, 
                                      marca, modelo, precio, espedition_date, 
                                      created, lastUpdate, lastInventoryUpdate, kilometraje
                                  ) OUTPUT INSERTED.id_articulo VALUES (?, ?, ?, ?, ?, ?, ?, ?,  ?, ?, ?, ?, ?, ?);
                                  """
                # print(sql_articulo)
                # print(unix_to_datetime(data['expedition_date']))
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
                    unix_to_datetime(data['expedition_date']),
                    unix_to_datetime(data['created']),
                    unix_to_datetime(data['lastUpdate']), 
                    unix_to_datetime(data['lastInventoryUpdate']), 
                    data['kilometraje']
                )
                # print(valores_articulo)
                cursor.execute(sql_articulo, valores_articulo)
                id_articulo = cursor.fetchone()[0]
                # print(id_articulo)
                if 'sucursal_id' in data:
                    sql_articulo_sucursal = """INSERT INTO articulo_sucursal (id_articulo, id_sucursal) VALUES (?, ?)"""
                    cursor.execute(sql_articulo_sucursal, (id_articulo, data['sucursal_id']))
                    
                if 'especificaciones' in data:
                    for especificacion in data['especificaciones']:
                        sql_especificaciones = """INSERT INTO especificaciones (tipo, id_articulo) 
                        OUTPUT INSERTED.id_especificacion VALUES (?, ?)"""
                        cursor.execute(sql_especificaciones, (especificacion['tipo'], id_articulo))
                        id_especificacion = cursor.fetchone()[0]

                        for clave, valor in especificacion['subespecificaciones'].items():
                            sql_subespecificaciones = """INSERT INTO subespecificaciones (clave, valor, id_especificacion) VALUES (?, ?, ?)"""
                            cursor.execute(sql_subespecificaciones, (clave, valor, id_especificacion))

                if 'imagenes' in data:
                    for imagen in data['imagenes']:
                        sql_images_articulo = """INSERT INTO images_articulo (url_image, descripcion, id_articulo) VALUES (?, ?, ?)"""
                        cursor.execute(sql_images_articulo, (imagen['url_image'], imagen['descripcion'], id_articulo))

                connection.commit()
            return jsonify({"success": True, "message": "Artículo creado exitosamente", "id_articulo": id_articulo}), 201

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    
@articulo_fl2.route('/especificaciones/<string:name_tipo>', methods=['GET'])
def get_subespecificaciones_por_tipo(name_tipo):
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_especificacion FROM especificaciones_adm WHERE tipo = ?", (name_tipo,))
                id_result = resultados_a_json(cursor, unico_resultado=True)
                
                if id_result:
                    id_especificacion = id_result['id_especificacion']
                    
                    cursor.execute("SELECT clave, valor FROM subespecificaciones_adm WHERE id_especificacion = ?", (id_especificacion,))
                    subespecificaciones_raw = resultados_a_json(cursor)
                    
                    subespecificaciones = {item['clave']: item['valor'] for item in subespecificaciones_raw}

                    respuesta = {
                        "especificaciones": [
                            {
                                "subespecificaciones": subespecificaciones,
                                "tipo": name_tipo
                            }
                        ]
                    }
                else:
                    respuesta = {"error": f"No se encontraron especificaciones para el tipo '{name_tipo}'"}
                    return jsonify(respuesta)
        return jsonify(respuesta)
    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


@articulo_fl2.route('/options', methods=['GET'])
def options_filter():
    try:
        consulta1 = "SELECT DISTINCT ano FROM articulo ORDER BY ano"
        consulta2 = "SELECT DISTINCT categoria FROM articulo ORDER BY categoria"
        consulta3 = "SELECT DISTINCT marca FROM articulo ORDER BY marca"
        consulta4 = "SELECT DISTINCT modelo FROM articulo ORDER BY modelo"
        consulta5 = "SELECT DISTINCT color FROM articulo ORDER BY color"
        consulta6 = "SELECT DISTINCT kilometraje FROM articulo ORDER BY kilometraje"
        consulta7 = "SELECT DISTINCT precio FROM articulo ORDER BY precio"

        opciones = {'ano': [], 'categoria': [], 'marca': [], 'modelo': [], 'color': [], 'precio':[], 'kilometraje':[]}

        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                # Año
                cursor.execute(consulta1)
                resultados = resultados_a_json(cursor)
                opciones['ano'] = [ano['ano'] for ano in resultados if ano['ano'] is not None]

                # Categoría
                cursor.execute(consulta2)
                resultados = resultados_a_json(cursor)
                opciones['categoria'] = [categoria['categoria'] for categoria in resultados if categoria['categoria'] is not None]

                # Marca
                cursor.execute(consulta3)
                resultados = resultados_a_json(cursor)
                opciones['marca'] = [marca['marca'] for marca in resultados if marca['marca'] is not None]

                # Modelo
                cursor.execute(consulta4)
                resultados = resultados_a_json(cursor)
                opciones['modelo'] = [modelo['modelo'] for modelo in resultados if modelo['modelo'] is not None]

                # Color
                cursor.execute(consulta5)
                resultados = resultados_a_json(cursor)
                opciones['color'] = [color['color'] for color in resultados if color['color'] is not None]

                # Color
                cursor.execute(consulta6)
                resultados = resultados_a_json(cursor)
                opciones['kilometraje'] = [kilometraje['kilometraje'] for kilometraje in resultados if kilometraje['kilometraje'] is not None]

                # Color
                cursor.execute(consulta7)
                resultados = resultados_a_json(cursor)
                opciones['precio'] = [precio['precio'] for precio in resultados if precio['precio'] is not None]

        return jsonify(opciones)           

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
   
#FALTA DOCUMENTAR
@articulo_fl2.route('/filtersfav', methods=['GET'])
def buscar_articulos_fav():
    try:
        anos = request.args.getlist('ano')  
        categorias = request.args.getlist('categoria')
        marcas = request.args.getlist('marca')
        modelos = request.args.getlist('modelo')
        colores = request.args.getlist('color')
        preciomin = request.args.getlist('pricemin')
        preciomax = request.args.getlist('pricemax')
        latitud_usuario = request.args.get('latitud')
        longitud_usuario = request.args.get('longitud')
        radio = request.args.get('radio')
        distribuidor_id = request.args.get('distribuidor_id')
        sucursal_id = request.args.get('sucursal_id')
        usuario_id = request.args.get('usuario_id')

        consulta = """
    SELECT 
        articulo.*, 
        sucursal.direccion, 
        sucursal.coordenadas,
        e.id_especificacion, 
        e.tipo, 
        img.url_image, 
        img.descripcion as img_descripcion,
        CAST(CASE WHEN fav.id_articulo IS NOT NULL THEN 1 ELSE 0 END AS INT) as favorite
    FROM 
        articulo
    LEFT JOIN 
        especificaciones e ON articulo.id_articulo = e.id_articulo
    LEFT JOIN 
        images_articulo img ON articulo.id_articulo = img.id_articulo
    JOIN 
        articulo_sucursal ON articulo.id_articulo = articulo_sucursal.id_articulo
    LEFT JOIN 
        (SELECT id_articulo FROM favoritos WHERE id_usuario = ? AND enable = 1) as fav
    ON 
        articulo.id_articulo = fav.id_articulo
    LEFT JOIN 
        favoritos ON articulo.id_articulo = favoritos.id_articulo
    JOIN 
        sucursal ON articulo_sucursal.id_sucursal = sucursal.id_sucursal
    JOIN 
        distribuidor_sucursal ON sucursal.id_sucursal = distribuidor_sucursal.id_sucursal
"""

        parametros = [usuario_id]
        distancias_sucursal=[]

        if distribuidor_id:
            consulta += " AND distribuidor_sucursal.id_distribuidor = ?"
            parametros.append(int(distribuidor_id))

        if sucursal_id:
            consulta += " AND sucursal.id_sucursal = ?"
            parametros.append(int(sucursal_id))
        if anos:
            consulta += f" AND ano IN ({','.join(['?'] * len(anos))})"
            parametros.extend(anos)
        if categorias:
            consulta += f" AND categoria IN ({','.join(['?'] * len(categorias))})"
            parametros.extend(categorias)
        if marcas:
            consulta += f" AND marca IN ({','.join(['?'] * len(marcas))})"
            parametros.extend(marcas)
        if modelos:
            consulta += f" AND modelo IN ({','.join(['?'] * len(modelos))})"
            parametros.extend(modelos)
        if colores:
            consulta += f" AND color IN ({','.join(['?'] * len(colores))})"
            parametros.extend(colores)
        if preciomin:
            consulta += " AND precio >= ?"
            parametros.extend([float(p) for p in preciomin])
        if preciomax:
            consulta += " AND precio <= ?"
            parametros.extend([float(p) for p in preciomax])

        if latitud_usuario and longitud_usuario and radio: 
            with connect_to_database() as connection: 
                with connection.cursor() as cursor:       
           
                    sql_sucursal = """SELECT * FROM sucursal;"""
                    cursor.execute(sql_sucursal)
                    sucursal_results = resultados_a_json(cursor)
                    sucursales_cercanas, distancias_sucursal=obtener_sucursales_cercanas(latitud_usuario,longitud_usuario,radio,sucursal_results)
                    ids_sucursales_cercanas = [sucursal["id_sucursal"] for sucursal in sucursales_cercanas]
                    
                    if sucursales_cercanas!=[]:
                        consulta += f" AND articulo_sucursal.id_sucursal IN ({','.join(['?'] * len(ids_sucursales_cercanas))})"
                        parametros.extend(ids_sucursales_cercanas)


        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute(consulta, parametros)
                raw_results = resultados_a_json(cursor)
                
                articulo_results = {}
                processed_especificaciones = set()
                for row in raw_results:
                    id_articulo = row['id_articulo']
                    print(id_articulo)
                    id_especificacion = row.get('id_especificacion')
                    if id_articulo not in articulo_results:
                        articulo_results[id_articulo] = {
                            'id_articulo': id_articulo,
                            'marca': row['marca'],
                            'favorite': row['favorite'],
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

                distancias_sucursal = [round(distancia, 3) for distancia in distancias_sucursal]
                print(processed_especificaciones)
                if latitud_usuario and longitud_usuario and radio:
                    sucursal_distancia_map = {suc['id_sucursal']: dist for suc, dist in zip(sucursales_cercanas, distancias_sucursal)}

                    for articulo in articulo_results.values():
                        id_sucursal_articulo = articulo['id_sucursal']
                        # Asignar la distancia si la sucursal del artículo está en las sucursales cercanas
                        if id_sucursal_articulo in sucursal_distancia_map:
                            articulo['distancia'] = sucursal_distancia_map[id_sucursal_articulo]

                        # id_articulo = row['id_articulo']
                        
                        # if distancias_sucursal:
                        #     articulo_results[id_articulo]['distancia'] = distancias_sucursal[index]

                return list(articulo_results.values())
                
    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    
@articulo_fl2.route('/filters', methods=['GET'])
def buscar_articulos():

    try:
        anos = request.args.getlist('ano')  
        categorias = request.args.getlist('categoria')
        marcas = request.args.getlist('marca')
        modelos = request.args.getlist('modelo')
        colores = request.args.getlist('color')
        preciomin = request.args.getlist('pricemin')
        preciomax = request.args.getlist('pricemax')
        latitud_usuario = request.args.get('latitud')
        longitud_usuario = request.args.get('longitud')
        radio = request.args.get('radio')
        distribuidor_id = request.args.get('distribuidor_id')
        sucursal_id = request.args.get('sucursal_id')
        usuario_id = request.args.get('usuario_id')

        # consulta = "SELECT articulo.*, sucursal.coordenadas FROM articulo " \
        #            "JOIN articulo_sucursal ON articulo.id_articulo = articulo_sucursal.id_articulo " \
        #            "JOIN sucursal ON articulo_sucursal.id_sucursal = sucursal.id_sucursal " \
        #            "WHERE 1=1"
        # consulta = "SELECT a.*, s.coordenadas FROM articulo a " \
        #    "JOIN articulo_sucursal asu ON a.id_articulo = asu.id_articulo " \
        #    "JOIN sucursal s ON asu.id_sucursal = s.id_sucursal " \
        #    "JOIN distribuidor_sucursal sd ON s.id_sucursal = sd.id_sucursal " \
        #    "WHERE 1=1"
        #    "ORDER BY articulo.id_articulo" \
        consulta = "SELECT articulo.*,sucursal.direccion, sucursal.coordenadas,e.id_especificacion, e.tipo, img.url_image, img.descripcion as img_descripcion FROM articulo " \
           "LEFT JOIN especificaciones e ON articulo.id_articulo = e.id_articulo " \
           "LEFT JOIN images_articulo img ON articulo.id_articulo = img.id_articulo " \
           "JOIN articulo_sucursal ON articulo.id_articulo = articulo_sucursal.id_articulo " \
           "JOIN sucursal ON articulo_sucursal.id_sucursal = sucursal.id_sucursal " \
           "JOIN distribuidor_sucursal ON sucursal.id_sucursal = distribuidor_sucursal.id_sucursal " \
           "WHERE 1=1"
        sql="""
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
        parametros = []
        if distribuidor_id:
            consulta += " AND distribuidor_sucursal.id_distribuidor = ?"
            parametros.append(int(distribuidor_id))

        if sucursal_id:
            consulta += " AND sucursal.id_sucursal = ?"
            parametros.append(int(sucursal_id))
        if anos:
            consulta += f" AND ano IN ({','.join(['?'] * len(anos))})"
            parametros.extend(anos)
        if categorias:
            consulta += f" AND categoria IN ({','.join(['?'] * len(categorias))})"
            parametros.extend(categorias)
        if marcas:
            consulta += f" AND marca IN ({','.join(['?'] * len(marcas))})"
            parametros.extend(marcas)
        if modelos:
            consulta += f" AND modelo IN ({','.join(['?'] * len(modelos))})"
            parametros.extend(modelos)
        if colores:
            consulta += f" AND color IN ({','.join(['?'] * len(colores))})"
            parametros.extend(colores)
        if preciomin:
            consulta += " AND precio <= ?"
            parametros.extend([float(p) for p in preciomin])
        if preciomax:
            consulta += " AND precio >= ?"
            parametros.extend([float(p) for p in preciomax])

        if latitud_usuario and longitud_usuario and radio: 
            with connect_to_database() as connection:
                with connection.cursor() as cursor:       
           
                    sql_sucursal = """SELECT * FROM sucursal;"""
                    cursor.execute(sql_sucursal)
                    sucursal_results = resultados_a_json(cursor)
                    sucursales_cercanas, distancias_sucursal=obtener_sucursales_cercanas(latitud_usuario,longitud_usuario,radio,sucursal_results)
                    ids_sucursales_cercanas = [sucursal["id_sucursal"] for sucursal in sucursales_cercanas]
                    
                    if sucursales_cercanas!=[]:
                        consulta += f" AND articulo_sucursal.id_sucursal IN ({','.join(['?'] * len(ids_sucursales_cercanas))})"
                        parametros.extend(ids_sucursales_cercanas)


        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute(consulta, parametros)
                raw_results = resultados_a_json(cursor)
                articulo_results = {}
                processed_especificaciones = set()
              
                for index, row in enumerate(raw_results):
                   

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
                    sql_sucursal="""
                                SELECT direccion FROM sucursal WHERE id_sucursal =?
                        """
                    cursor.execute(sql_sucursal, (id_sucursales,))
                    sucursal_dir=resultados_a_json(cursor,unico_resultado=True)
                    articulo_results[id_articulo]['direccion'] = sucursal_dir['direccion']
                    articulo_results[id_articulo]['id_sucursal'] = id_sucursales 

               
                

               
                return list(articulo_results.values())
                
    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500

@articulo_fl2.route('/subespecificaciones', methods=['GET'])
def get_tipos_sub_especificaciones():
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT DISTINCT clave FROM subespecificaciones")
                subespecificaciones_raw = resultados_a_json(cursor)
                if subespecificaciones_raw:
                    subespecificaciones = [registro['clave'] for registro in subespecificaciones_raw]
                return jsonify({"especificaciones": subespecificaciones})
    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    
@articulo_fl2.route('/especificaciones', methods=['POST'])
def post_especificaciones():
    data = request.json
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                for especificacion in data['especificaciones']:
                    sql_especificaciones = """INSERT INTO especificaciones_adm (tipo) OUTPUT INSERTED.id_especificacion VALUES  (?)"""
                    cursor.execute(sql_especificaciones, (especificacion['tipo'],))
                    id_especificacion = cursor.fetchone()[0]

                    for clave, valor in especificacion['subespecificaciones'].items():
                        sql_subespecificaciones = """INSERT INTO subespecificaciones_adm (clave, valor, id_especificacion) VALUES (?, ?, ?)"""
                        cursor.execute(sql_subespecificaciones, (clave, valor, id_especificacion))

                    for marca in especificacion.get('marcas', []):
                        sql_marcas = """INSERT INTO marcas_adm (marca, id_especificacion) VALUES (?, ?)"""
                        cursor.execute(sql_marcas, (marca, id_especificacion))

                    connection.commit()

            return jsonify({"success": True, "message": "Especificacion creado exitosamente" ,"id_especificacion": id_especificacion}), 201

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    
@articulo_fl2.route('/especificaciones', methods=['GET'])
def get_todas_especificaciones():
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                # Obtener todas las especificaciones
                cursor.execute("SELECT * FROM especificaciones_adm")
                todas_especificaciones_raw = resultados_a_json(cursor)
                
                especificaciones = []
                for espec in todas_especificaciones_raw:
                    id_especificacion = espec['id_especificacion']
                    tipo = espec['tipo']

                    # Obtener subespecificaciones
                    cursor.execute("SELECT clave, valor FROM subespecificaciones_adm WHERE id_especificacion = ?", (id_especificacion,))
                    subespecificaciones_raw = resultados_a_json(cursor)
                    subespecificaciones = {registro['clave']: registro['valor'] for registro in subespecificaciones_raw}

                    # Obtener marcas
                    cursor.execute("SELECT marca FROM marcas_adm WHERE id_especificacion = ?", (id_especificacion,))
                    marcas_raw = resultados_a_json(cursor)
                    marcas = [registro['marca'] for registro in marcas_raw]

                    especificaciones.append({
                        "id_especificacion":id_especificacion,
                        "tipo": tipo,
                        "subespecificaciones": subespecificaciones,
                        "marcas": marcas
                    })

                return jsonify({"especificaciones": especificaciones})
    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500

@articulo_fl2.route('/especificaciones/<int:id_especificacion>', methods=['PUT'])
def actualizar_especificacion(id_especificacion):
    try:
        
        datos = request.get_json()

        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                if 'tipo' in datos:
                    cursor.execute("UPDATE especificaciones_adm SET tipo = ? WHERE id_especificacion = ?", (datos['tipo'], id_especificacion))

                if 'subespecificaciones' in datos:
                    for clave, valor in datos['subespecificaciones'].items():
                        cursor.execute("UPDATE subespecificaciones_adm SET valor = ? WHERE id_especificacion = ? AND clave = ?", (valor, id_especificacion, clave))
              
                if 'marcas' in datos:
                    cursor.execute("DELETE FROM marcas_adm WHERE id_especificacion = ?", (id_especificacion,))
                    # Luego, insertar nuevas marcas
                    for marca in datos['marcas']:
                        cursor.execute("INSERT INTO marcas_adm (id_especificacion, marca) VALUES (?, ?)", (id_especificacion, marca))

            connection.commit()

        return jsonify({"success": "Especificación actualizada correctamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar la especificación: {e}"}), 500
   


@articulo_fl2.route('/especificaciones/<int:id>', methods=['GET'])
def get_especificacion_por_id(id):
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT * FROM especificaciones_adm WHERE id_especificacion = ?", (id,))
                especificacion_raw = resultados_a_json(cursor)

                if not especificacion_raw:
                    return jsonify({"error": "Especificación no encontrada"}), 404

                espec = especificacion_raw[0]
                id_especificacion = espec['id_especificacion']
                tipo = espec['tipo']

                # Obtener subespecificaciones
                cursor.execute("SELECT clave, valor FROM subespecificaciones_adm WHERE id_especificacion = ?", (id_especificacion,))
                subespecificaciones_raw = resultados_a_json(cursor)
                subespecificaciones = {registro['clave']: registro['valor'] for registro in subespecificaciones_raw}

                # Obtener marcas
                cursor.execute("SELECT marca FROM marcas_adm WHERE id_especificacion = ?", (id_especificacion,))
                marcas_raw = resultados_a_json(cursor)
                marcas = [registro['marca'] for registro in marcas_raw]

                return jsonify({
                    "id_especificacion": id_especificacion,
                    "tipo": tipo,
                    "subespecificaciones": subespecificaciones,
                    "marcas": marcas
                })
    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500



##FALTA DOCUMENTAR
@articulo_fl2.route('/articulo/<int:id_articulo>', methods=['PUT'])
def actualizar_articulo(id_articulo):
    try:
        with connect_to_database() as connection:
            data = request.json
            campos_permitidos = ['ano', 'categoria', 'color', 
                                 'descripcion', 'enable','id_sucursal', 'mainImage', 'marca', 'expedition_date',
                                 'modelo', 'precio', 'lastInventoryUpdate', 'kilometraje','imagenes','especificaciones']
            cambios = []
            valores = []
            changes=True
            for campo in campos_permitidos:
                if campo in data:
                    # if campo == 'id_distribuidor':
                       
                    #     sql_update_relacion_distribuidor = "UPDATE usuario_distribuidor SET id_distribuidor = ? WHERE id_usuario = ?;"
                    #     valores_relacion_dis = (data['id_distribuidor'], id_articulo)
                        
                    #     changes=False
                    #     with connection.cursor() as cursor_relacion:
                    #         cursor_relacion.execute(sql_update_relacion_distribuidor, valores_relacion_dis)
                    #         connection.commit()

                    if campo == 'id_sucursal':

                        changes=False
                        sql_update_relacion_sucursal = "UPDATE articulo_sucursal SET id_sucursal = ? WHERE id_articulo = ?;"
                        valores_relacion = (data['id_sucursal'], id_articulo)
                        with connection.cursor() as cursor_relacion:
                            cursor_relacion.execute(sql_update_relacion_sucursal, valores_relacion)
                            connection.commit()
                    elif campo == 'imagenes':

                        changes=False
                        for imagen in data['imagenes']:
                            with connection.cursor() as cursor:
                                if 'id_imagen' in imagen:
                                    sql_update_imagen = """UPDATE images_articulo SET url_image = ?, descripcion = ? WHERE id_images_articulo = ? AND id_articulo = ?"""
                                    cursor.execute(sql_update_imagen, (imagen['url_image'], imagen['descripcion'], imagen['id_imagen'], id_articulo))
                                else:
                                    sql_insert_imagen = """INSERT INTO images_articulo (url_image, descripcion, id_articulo) VALUES (?, ?, ?)"""
                                    cursor.execute(sql_insert_imagen, (imagen['url_image'], imagen['descripcion'], id_articulo))

                    elif campo == 'especificaciones':
                        changes=False

                        for especificacion in data['especificaciones']:
                            with connection.cursor() as cursor:
                                cursor.execute("SELECT id_especificacion FROM especificaciones WHERE id_articulo = ?", (id_articulo))
                                
                                result = resultados_a_json(cursor, unico_resultado=True)
                                id_especificacion=result['id_especificacion']
                                
                                subespecificacionessc=especificacion['subespecificaciones']
                               
                                for subespecificacion in especificacion.get('subespecificaciones', []):
                                    # print(subespecificacion_value)
                                   
                                    if 'id_subespecificacion' in subespecificacion:
                                        # Actualizar subespecificación existente
                                        sql_update_subespecificacion = """UPDATE subespecificaciones SET clave = ?, valor = ? WHERE id_subespecificacion = ? AND id_especificacion = ?"""
                                        cursor.execute(sql_update_subespecificacion, (subespecificacion['clave'], subespecificacion['valor'], subespecificacion['id_subespecificacion'], id_especificacion))
                                    else:
                                        # Insertar nueva subespecificación
                                        sql_insert_subespecificacion = """INSERT INTO subespecificaciones (clave, valor, id_especificacion) VALUES (?, ?, ?)"""
                                        cursor.execute(sql_insert_subespecificacion, (subespecificacion, str(subespecificacionessc[subespecificacion]), id_especificacion))
                            # if 'id_especificacion' in especificacion:
                            #     # Actualizar especificación existente
                            #     sql_update_especificacion = """UPDATE especificaciones SET tipo = ? WHERE id_especificacion = ? AND id_articulo = ?"""
                            #     cursor.execute(sql_update_especificacion, (especificacion['tipo'], especificacion['id_especificacion'], id_articulo))
                            # else:
                            #     # Insertar nueva especificación
                            #     sql_insert_especificacion = """INSERT INTO especificaciones (tipo, id_articulo) VALUES (?, ?)"""
                            #     cursor.execute(sql_insert_especificacion, (especificacion['tipo'], id_articulo))
                            #     id_especificacion = cursor.lastrowid

                            # for subespecificacion in especificacion.get('subespecificaciones', []):
                            #     if 'id_subespecificacion' in subespecificacion:
                            #         # Actualizar subespecificación existente
                            #         sql_update_subespecificacion = """UPDATE subespecificaciones SET clave = ?, valor = ? WHERE id_subespecificacion = ? AND id_especificacion = ?"""
                            #         cursor.execute(sql_update_subespecificacion, (subespecificacion['clave'], subespecificacion['valor'], subespecificacion['id_subespecificacion'], id_especificacion))
                            #     else:
                            #         # Insertar nueva subespecificación
                            #         sql_insert_subespecificacion = """INSERT INTO subespecificaciones (clave, valor, id_especificacion) VALUES (?, ?, ?)"""
                            #         cursor.execute(sql_insert_subespecificacion, (subespecificacion['clave'], subespecificacion['valor'], id_especificacion))
                    
                            # for clave, valor in especificacion['subespecificaciones'].items():
                            #     Aquí, asumo que no tienes IDs para subespecificaciones individuales,
                            #     por lo que siempre las insertarás como nuevas.
                            #     Necesitarías ajustar esto si también necesitas actualizarlas.
                            #     sql_insert_subespecificaciones = """INSERT INTO subespecificaciones (clave, valor, id_especificacion) VALUES (?, ?, ?)"""
                            #     cursor.execute(sql_insert_subespecificaciones, (clave, valor, id_especificacion))

                    else:
                        if campo == 'lastInventoryUpdate':
                            valor = unix_to_datetime(data['lastInventoryUpdate'])
                            cambios.append(f"{campo} = ?")
                            valores.append(valor) 
                        else:
                            cambios.append(f"{campo} = ?")
                            valores.append(data[campo])

                

            if not cambios and changes:
                return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

            # Agregar actualización de lastUpdate
            cambios.append("lastUpdate = CURRENT_TIMESTAMP")
            
            sql_update_articulo = "UPDATE articulo SET " + ", ".join(cambios) + " WHERE id_articulo = ?"
            valores.append(id_articulo)
            
            with connection.cursor() as cursor:
                cursor.execute(sql_update_articulo, valores)

                # Actualizar o insertar especificaciones
                # if 'especificaciones' in data:
                #     for especificacion in data['especificaciones']:
                #         if 'id_especificacion' in especificacion:
                #             # Actualizar especificación existente
                #             sql_update_especificacion = """UPDATE especificaciones SET tipo = ? WHERE id_especificacion = ? AND id_articulo = ?"""
                #             cursor.execute(sql_update_especificacion, (especificacion['tipo'], especificacion['id_especificacion'], id_articulo))
                #         else:
                #             # Insertar nueva especificación
                #             sql_insert_especificacion = """INSERT INTO especificaciones (tipo, id_articulo) VALUES (?, ?)"""
                #             cursor.execute(sql_insert_especificacion, (especificacion['tipo'], id_articulo))
                #             id_especificacion = cursor.lastrowid

                #         # Actualizar o insertar subespecificaciones
                #         # for subespecificacion in especificacion.get('subespecificaciones', []):
                #         #     if 'id_subespecificacion' in subespecificacion:
                #         #         # Actualizar subespecificación existente
                #         #         sql_update_subespecificacion = """UPDATE subespecificaciones SET clave = ?, valor = ? WHERE id_subespecificacion = ? AND id_especificacion = ?"""
                #         #         cursor.execute(sql_update_subespecificacion, (subespecificacion['clave'], subespecificacion['valor'], subespecificacion['id_subespecificacion'], id_especificacion))
                #         #     else:
                #         #         # Insertar nueva subespecificación
                #         #         sql_insert_subespecificacion = """INSERT INTO subespecificaciones (clave, valor, id_especificacion) VALUES (?, ?, ?)"""
                #         #         cursor.execute(sql_insert_subespecificacion, (subespecificacion['clave'], subespecificacion['valor'], id_especificacion))
                #         for clave, valor in especificacion['subespecificaciones'].items():
                #             # Aquí, asumo que no tienes IDs para subespecificaciones individuales,
                #             # por lo que siempre las insertarás como nuevas.
                #             # Necesitarías ajustar esto si también necesitas actualizarlas.
                #             sql_insert_subespecificaciones = """INSERT INTO subespecificaciones (clave, valor, id_especificacion) VALUES (?, ?, ?)"""
                #             cursor.execute(sql_insert_subespecificaciones, (clave, valor, id_especificacion))


                
                connection.commit()

            return jsonify({"success": True, "message": f"Artículo con ID {id_articulo} actualizado exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


# especificaciones,articulo_sucursal,favoritos,images_articulo
@articulo_fl2.route('/articulo/<int:id_articulo>', methods=['DELETE'])
def eliminar_articulo(id_articulo):
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:

                sql_select_especificaciones = "SELECT id_especificacion FROM especificaciones WHERE id_articulo = ?"
                cursor.execute(sql_select_especificaciones, (id_articulo,))
                especificaciones = resultados_a_json(cursor)
                # print(especificaciones)
                # Eliminar subespecificaciones relacionadas con cada especificación
                for espec in especificaciones:
                    sql_delete_subespecificaciones = "DELETE FROM subespecificaciones WHERE id_especificacion = ?"
                    cursor.execute(sql_delete_subespecificaciones, (espec['id_especificacion'],))

                # Eliminar registros de especificaciones
                sql_delete_especificaciones = "DELETE FROM especificaciones WHERE id_articulo = ?"
                cursor.execute(sql_delete_especificaciones, (id_articulo,))

                # Eliminar registros de articulo_sucursal
                sql_delete_articulo_sucursal = "DELETE FROM articulo_sucursal WHERE id_articulo = ?"
                cursor.execute(sql_delete_articulo_sucursal, (id_articulo,))

                # Eliminar registros de favoritos
                sql_delete_favoritos = "DELETE FROM favoritos WHERE id_articulo = ?"
                cursor.execute(sql_delete_favoritos, (id_articulo,))

                # Eliminar registros de images_articulo
                sql_delete_images_articulo = "DELETE FROM images_articulo WHERE id_articulo = ?"
                cursor.execute(sql_delete_images_articulo, (id_articulo,))

                # Finalmente, eliminar el artículo
                sql_delete_articulo = "DELETE FROM articulo WHERE id_articulo = ?"
                cursor.execute(sql_delete_articulo, (id_articulo,))

                # Confirma todas las operaciones
                connection.commit()

            return jsonify({"success": True, "message": f"Artículo con ID {id_articulo} y registros relacionados eliminados exitosamente"}), 200

    except Exception as e:
        # En caso de un error, se hará rollback automáticamente si se está usando un gestor de transacciones
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


# @articulo_fl2.route('/<str:id_usuario>/<int:id_articulo>', methods=['POST'])
# def aritulo_favorito(id_articulo,id_usuario):
# {
#   "especificaciones": [
#     "Motor":"motor1",
#     "Motor":"motor2",
#     "Motor":"algunmotor",
#     "Potencia",
#     "Asientos",
#     "Interior",
#     "Transmisión",
#     "Tracción",
#     "Capacidad de carga",
#     "Altura del suelo",
#     "esecificaion1",
#     "esecificaion2",
#     "Software"
#   ]
# }
@articulo_fl2.route('/<int:id_articulo>/<int:id_usuario>', methods=['POST'])
def articulo_favorito(id_usuario, id_articulo):
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                sql_check = """SELECT enable FROM favoritos WHERE id_usuario = ? AND id_articulo = ?"""
                cursor.execute(sql_check, (id_usuario, id_articulo))
                result = resultados_a_json(cursor, unico_resultado=True)

                if result:
                    new_enable_status = not result['enable']
                    sql_update = """UPDATE favoritos SET enable =
                      ? WHERE id_usuario = ? AND id_articulo = ?"""
                    cursor.execute(sql_update, (new_enable_status, id_usuario, id_articulo))
                else:
                    sql_insert = """INSERT INTO favoritos (id_usuario, id_articulo, fecha_agregado, [enable]) 
                    VALUES (?, ?, ?, ?)"""
                    fecha_agregado = datetime.now()
                    cursor.execute(sql_insert, (id_usuario, id_articulo, fecha_agregado, 1))

                connection.commit()
            return jsonify({"success": True, "message": "Estado de favorito actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    
@articulo_fl2.route('/<int:id_articulo>/referencia', methods=['GET'])
def articulo_referencia(id_articulo):
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                sql = """SELECT s.* FROM sucursal s
                         INNER JOIN articulo_sucursal a_s ON s.id_sucursal = a_s.id_sucursal
                         WHERE a_s.id_articulo = ?"""
                cursor.execute(sql, (id_articulo,))
                sucursales_raw = resultados_a_json(cursor)
                
                if not sucursales_raw:
                    return jsonify({"error": "No se encontraron sucursales para el artículo"}), 404

                sucursales = [dict(sucursal) for sucursal in sucursales_raw]

                return jsonify(sucursales)
    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
