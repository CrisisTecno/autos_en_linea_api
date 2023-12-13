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

@auto_fl2.route('/auto/<int:id_auto>', methods=['PUT'])
async def actualizar_auto(id_auto):
    try:
        async with connect_to_database() as connection:
            data = request.json
            campos_permitidos = ['nombre', 'descripcion', 'disponibilidad', 'categoria_de_auto',
                                 'marca', 'modelo', 'anio', 'kilometraje', 'precio', 'especificaciones']
            
            if not any(campo in data for campo in campos_permitidos):
                return jsonify({"error": "Se requiere al menos un campo para actualizar"}), 400
                
            async with connection.cursor() as cursor:
                sql_update = "UPDATE auto SET "
                valores = []

                for campo in campos_permitidos:
                    if campo in data:
                        sql_update += f"{campo} = %s, "
                        valores.append(data[campo])

                sql_update = sql_update.rstrip(', ')

                sql_update += " WHERE id_auto = %s"
                valores.append(id_auto)

                await cursor.execute(sql_update, valores)
                await connection.commit()

            return jsonify({"success": True, "message": f"Auto con ID {id_auto} actualizado exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


@auto_fl2.route('/auto/<int:id_auto>', methods=['DELETE'])
async def eliminar_auto(id_auto):
    try:
        async with connect_to_database() as connection:
            async with connection.cursor() as cursor:
                sql_delete = "DELETE FROM auto WHERE id_auto = %s"
                await cursor.execute(sql_delete, (id_auto,))
                await connection.commit()

            return jsonify({"success": True, "message": f"Auto con ID {id_auto} eliminado exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
