from flask import Flask, request, jsonify
from flask import Blueprint
from config.database import connect_to_database

auto_fl2 = Blueprint('auto_post', __name__)

@auto_fl2.route('/auto', methods=['POST'])
async def crear_auto():
    try:
        async with connect_to_database() as connection:
            data = request.json
            campos_requeridos = ['id_auto', 'nombre',
                                  'descripcion', 'disponibilidad', 'categoria_de_auto',
                                    'marca','modelo','anio','kilometraje','precio','especificaciones']
      
            if not all(campo in data for campo in campos_requeridos):
                return jsonify({"error": "Faltan campos requeridos"}), 400
                
            async with connection.cursor() as cursor:
                sql = """INSERT INTO auto (
                             id_auto, nombre, descripcion, disponibilidad, categoria_de_auto, 
                             marca, modelo, anio, kilometraje,precio,especificaciones
                         ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"""
                valores=(
                    data['id_auto'],
                    data['nombre'],
                    data['descripcion'],
                    data['disponibilidad'],
                    data['categoria_de_auto'],
                    data['marca'],
                    data['modelo'],
                    data['anio'],
                    data['kilometraje'],
                    data['precio'],
                    data['especificaciones']
                )
                await cursor.execute(sql, valores)
                await connection.commit()
                rows_affected = cursor.rowcount
                print(rows_affected)

            return jsonify({"success": True, "message": "auto creado exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
