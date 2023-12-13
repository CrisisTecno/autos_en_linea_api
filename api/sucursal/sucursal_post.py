from flask import Flask, request, jsonify
from flask import Blueprint
from config.database import connect_to_database

sucursal_fl2 = Blueprint('sucursal_post', __name__)

@sucursal_fl2.route('/sucursal', methods=['POST'])
async def crear_sucursal():
    try:
        async with connect_to_database() as connection:
            data = request.json
            campos_requeridos = [ 'id_sucursal','direccion',
                                  'telefono', 'nombre', 'gerente',
                                    'contacto','correo_electronico','url_logo','coordenadas','horarios_de_atencion']
            print(data)
            if not all(campo in data for campo in campos_requeridos):
                return jsonify({"error": "Faltan campos requeridos"}), 400
                
            async with connection.cursor() as cursor:
                sql = """INSERT INTO sucursal (
             id_sucursal, direccion,
             telefono, nombre, gerente,
             contacto, correo_electronico, url_logo,
             coordenadas, horarios_de_atencion, created, lastUpdate
         ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,
         CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"""

                valores=(
                    data['id_sucursal'],
                    data['direccion'],
                    data['telefono'],
                    data['nombre'],
                    data['gerente'],
                    data['contacto'],
                    data['correo_electronico'],
                    data['url_logo'],
                    data['coordenadas'],
                    data['horarios_de_atencion'],
                )
                await cursor.execute(sql, valores)
                await connection.commit()

            return jsonify({"success": True, "message": "sucursal creado exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
