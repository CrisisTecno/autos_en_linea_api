
from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request

sucursal_fl1=Blueprint('sucursal_id', __name__)

async def get_sucursal_basic(connection, sucursal_id):
    try:
        async with connection.cursor() as cursor:
            sql_sucursal = """SELECT * FROM sucursal WHERE id_sucursal = %s"""
            await cursor.execute(sql_sucursal, (sucursal_id,))
            sucursal_info = await cursor.fetchone()
            return sucursal_info
    except Exception as e:
        print(f"Error obtaining sucursal info for ID {sucursal_id}: {e}")
        return None

async def get_sucursal_detail(connection, id_sucursal):
    try:
        async with connection.cursor() as cursor:
            sql_sucursal = """SELECT id_sucursal, id_usuario,
                              direccion, telefono, gerente, contacto, 
                              correo_electronico, created, lastUpdate, url_logo, nombre,
                              coordenadas, horarios_de_atencion
                           FROM sucursal
                           WHERE id_sucursal = %s;"""
            await cursor.execute(sql_sucursal, (id_sucursal,))
            sucursal_info = await cursor.fetchone()

            if sucursal_info:
                sql_sucursales = """SELECT * FROM images_sucursal
                                    WHERE id_sucursal = %s;"""
                await cursor.execute(sql_sucursales, (id_sucursal,))
                sucursal_images = await cursor.fetchall()
                sql_distribuidor = """SELECT usuario.*
                                      FROM usuario
                                      JOIN distribuidor_sucursal ON usuario.id_usuario = distribuidor_sucursal.id_usuario
                                      WHERE usuario.rol = 'distribuidor' 
                                      AND distribuidor_sucursal.id_sucursal = %s;"""
                await cursor.execute(sql_distribuidor, (id_sucursal,))
                distribuidor_list = await cursor.fetchall()
                sucursal_info['sucursal_images'] = sucursal_images
                sucursal_info['sucursal_distribuidores'] = distribuidor_list

            return sucursal_info
    except Exception as e:
        print(f"Error obtaining detailed sucursal info for ID {id_sucursal}: {e}")
        return None
    finally:
        connection.close()


@sucursal_fl1.route('/<int:sucursal_id>', methods=['GET'])
async def get_sucursal_by_id(sucursal_id):
    async with connect_to_database() as con:
        try:
            sucursal_info = await get_sucursal_detail(con, sucursal_id)
            if sucursal_info:
                return jsonify({"success": True, "data": sucursal_info})
            else:
                return jsonify({"error": f"sucursal with ID {sucursal_id} not found"}), 404
        except Exception as e :
            return jsonify({"error":"Data Base erorr {}".format(e)})