from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request

distribuidor_fl2=Blueprint('distribuidor_methods', __name__)



@distribuidor_fl2.route('/distribuidor', methods=['POST'])
async def crear_distribuidor():
    try:
        async with connect_to_database() as connection:
            data = request.json
            campos_requeridos = [
                'gerente', 'logo_image', 'coordenadas', 'direccion',
                'nombre', 'url_paginaWeb', 'telefono', 'email', 'horarioAtencion'
            ]
            
            if not all(campo in data for campo in campos_requeridos):
                return jsonify({"error": "Faltan campos requeridos"}), 400
                
            async with connection.cursor() as cursor:
                sql = """INSERT INTO distribuidor (
                             gerente, logo_image, coordenadas, direccion,
                             nombre, url_paginaWeb, telefono, email, horarioAtencion
                         ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                valores = (
                    data['gerente'],
                    data['logo_image'],
                    data['coordenadas'],
                    data['direccion'],
                    data['nombre'],
                    data['url_paginaWeb'],
                    data['telefono'],
                    data['email'],
                    data['horarioAtencion']
                )
                await cursor.execute(sql, valores)
                await connection.commit()

            return jsonify({"success": True, "message": "Distribuidor creado exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


@distribuidor_fl2.route('/distribuidor/<int:id_distribuidor>', methods=['PUT'])
async def actualizar_distribuidor(id_distribuidor):
    try:
        async with connect_to_database() as connection:
            data = request.json
            campos_permitidos = [
                'gerente', 'logo_image', 'coordenadas', 'direccion',
                'nombre', 'url_paginaWeb', 'telefono', 'email', 'horarioAtencion'
            ]

            if not any(campo in data for campo in campos_permitidos):
                return jsonify({"error": "Se requiere al menos un campo para actualizar"}), 400

            async with connection.cursor() as cursor:
                sql_update = "UPDATE distribuidor SET "
                valores = []

                for campo in campos_permitidos:
                    if campo in data:
                        sql_update += f"{campo} = %s, "
                        valores.append(data[campo])

                sql_update = sql_update.rstrip(', ')
                sql_update += " WHERE id_distribuidor = %s"
                valores.append(id_distribuidor)

                await cursor.execute(sql_update, valores)
                await connection.commit()

            return jsonify({"success": True, "message": f"Distribuidor con ID {id_distribuidor} actualizado exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500

    
@distribuidor_fl2.route('/distribuidor/<int:id_distribuidor>', methods=['DELETE'])
async def eliminar_distribuidor(id_distribuidor):
    try:
        async with connect_to_database() as connection:
            async with connection.cursor() as cursor:
                sql_delete = "DELETE FROM distribuidor WHERE id_distribuidor = %s"
                await cursor.execute(sql_delete, (id_distribuidor,))
                await connection.commit()

            return jsonify({"success": True, "message": f"Distribuidor con ID {id_distribuidor} eliminado exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
    
@distribuidor_fl2.route('/<int:id_distribuidor>/usuarios', methods=['GET'])
async def obtener_usuarios_por_distribuidor(id_distribuidor):
    try:
        async with connect_to_database() as connection:
            async with connection.cursor() as cursor:
              
                sql = """
                    SELECT * FROM usuario
                    WHERE id_distribuidor = %s
                """
                await cursor.execute(sql, (id_distribuidor,))
                usuarios = await cursor.fetchall()

                if not usuarios:
                    return jsonify({"error": f"No se encontraron usuarios para el distribuidor con ID {id_distribuidor}"}), 404

                return jsonify({"success": True, "usuarios": usuarios}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


@distribuidor_fl2.route('/<int:id_distribuidor>/articulos', methods=['GET'])
async def obtener_articulos_por_distribuidor(id_distribuidor):
    try:
        async with connect_to_database() as connection:
            async with connection.cursor() as cursor:
                sql = """
                    SELECT articulo.* FROM articulo
                    JOIN articulo_sucursal ON articulo.id_articulo = articulo_sucursal.id_articulo
                    JOIN distribuidor_sucursal ON articulo_sucursal.id_sucursal = distribuidor_sucursal.id_sucursal
                    WHERE distribuidor_sucursal.id_distribuidor = %s
                """
                await cursor.execute(sql, (id_distribuidor,))
                articulos = await cursor.fetchall()

                if not articulos:
                    return jsonify({"error": f"No se encontraron artículos para el distribuidor con ID {id_distribuidor}"}), 404

                return jsonify({"success": True, "articulos": articulos}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500



@distribuidor_fl2.route('/<int:id_distribuidor>/sucursales', methods=['GET'])
async def obtener_sucursales_por_distribuidor(id_distribuidor):
    try:
        async with connect_to_database() as connection:
            async with connection.cursor() as cursor:
                sql = """
                    SELECT sucursal.* FROM sucursal
                    JOIN distribuidor_sucursal ON sucursal.id_sucursal = distribuidor_sucursal.id_sucursal
                    WHERE distribuidor_sucursal.id_distribuidor = %s
                """
                await cursor.execute(sql, (id_distribuidor,))
                sucursales = await cursor.fetchall()

                if not sucursales:
                    return jsonify({"error": f"No se encontraron sucursales para el distribuidor con ID {id_distribuidor}"}), 404

                return jsonify({"success": True, "sucursales": sucursales}), 200

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500
