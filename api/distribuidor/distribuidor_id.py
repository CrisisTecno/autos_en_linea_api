from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request

distribuidor_fl1=Blueprint('distribuidor_id', __name__)


async def get_distribuidor_detail(connection, id_usuario):
    try:
        async with connection.cursor() as cursor:
            sql_distribuidor = """SELECT id_usuario,
                                  nombres, apellidos, direccion, gerente, url_logo, url_link_web, direccion,
                                  num_telefono, created, lastUpdate,
                                  id_sucursal, correo_electronico
                               FROM usuario
                               WHERE id_usuario = %s AND rol = 'Distribuidor';"""
            await cursor.execute(sql_distribuidor, (id_usuario,))
            distribuidor_info = await cursor.fetchone()

            if distribuidor_info:
                sql_sucursales = """SELECT sucursal.*
                                    FROM sucursal
                                    JOIN distribuidor_sucursal ON sucursal.id_sucursal = distribuidor_sucursal.id_sucursal
                                    WHERE distribuidor_sucursal.id_usuario = %s"""
                await cursor.execute(sql_sucursales, (id_usuario,))
                sucursal_list = await cursor.fetchall()
                distribuidor_info['sucursal_list'] = sucursal_list

            return distribuidor_info
    except Exception as e:
        print(f"Error obtaining detailed distribuidor info for ID {id_usuario}: {e}")
        return None
    finally:
        connection.close()


    
@distribuidor_fl1.route('/<int:distribuidor_id>', methods=['GET'])
async def get_distribuidor_by_id(distribuidor_id):
    async with connect_to_database() as con:
        try:
            distribuidor_by_id= await get_distribuidor_detail(con,distribuidor_id)
            if distribuidor_by_id:
                return jsonify({"success": True, "data": distribuidor_by_id})
            else:
                return jsonify({"error": f"distribuidor with ID {distribuidor_id} not found"}), 404
        except Exception as e :
            return jsonify({"error":"Data Base erorr {}".format(e)})