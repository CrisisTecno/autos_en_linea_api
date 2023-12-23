from flask import Blueprint, render_template
from config.database import connect_to_database
from flask import Flask, Response, jsonify, request
from utils.time import timedelta_to_string,timedelta_to_milliseconds
distribuidor_fl1=Blueprint('distribuidor_id', __name__)


async def process_distribuidor_por_id(connection, id_distribuidor):
    try:
        async with connection.cursor() as cursor:
            sql_distribuidor = "SELECT * FROM distribuidor WHERE id_distribuidor = %s"
            await cursor.execute(sql_distribuidor, (id_distribuidor,))
            distribuidor = await cursor.fetchone()
            if distribuidor:
                for key in ['created', 'lastUpdate']:
                    if distribuidor[key]:
                        distribuidor[key] = int(distribuidor[key].timestamp() * 1000)

                sql_sucursales = """
                    SELECT s.* FROM sucursal s
                    JOIN distribuidor_sucursal ds ON s.id_sucursal = ds.id_sucursal
                    WHERE ds.id_distribuidor = %s
                """
                await cursor.execute(sql_sucursales, (id_distribuidor,))
                sucursales = await cursor.fetchall()

                for sucursal in sucursales:
                    for key in ['created', 'lastUpdate']:
                        if sucursal[key]:
                            sucursal[key] = int(sucursal[key].timestamp() * 1000)

                distribuidor['sucursales'] = sucursales

                sql_horarios = "SELECT * FROM horarios_distribuidor WHERE id_distribuidor = %s"
                await cursor.execute(sql_horarios, (id_distribuidor,))

                horarios_raw = await cursor.fetchall()
                horarios_distribuidor= {}
                for horario in horarios_raw:
                    dia = horario['day']
                    horarios_distribuidor[dia] = {
                        'open': int(timedelta_to_milliseconds(horario['open'])),
                        'close': int(timedelta_to_milliseconds(horario['close']))
                    }

                distribuidor['horarios_distribuidor'] = horarios_distribuidor
                
                sql_marcas = "SELECT marca FROM marcas_distribuidor WHERE id_distribuidor = %s"
                await cursor.execute(sql_marcas, (id_distribuidor,))
                marcas_raw = await cursor.fetchall()
                marcas = [marca['marca'] for marca in marcas_raw]  

                distribuidor['marcas'] = marcas
            return distribuidor
    finally:
        connection.close()



    
@distribuidor_fl1.route('/<int:distribuidor_id>', methods=['GET'])
async def get_distribuidor_by_id(distribuidor_id):
    async with connect_to_database() as con:
        try:
            distribuidor_by_id= await process_distribuidor_por_id(con,distribuidor_id)
            if distribuidor_by_id:
                return jsonify({"success": True, "data": distribuidor_by_id})
            else:
                return jsonify({"error": f"distribuidor with ID {distribuidor_id} not found"}), 404
        except Exception as e :
            return jsonify({"error":"Data Base erorr {}".format(e)})