from contextlib import asynccontextmanager
import pymysql
import aiomysql

@asynccontextmanager
async def connect_to_database():
    connection = await aiomysql.connect(
        # host='containers-us-west-24.railway.app',
        # port=5828,
        # user='root',
        # password='IJDLZQVMpvbnBAuOsGBg',
        # db='railway',
        # cursorclass=aiomysql.DictCursor
        host='viaduct.proxy.rlwy.net',
        port=44970,
        user='root',
        password='CG-AeB51DAfgCcb2A5-g32EabBcaEBAC',
        db='railway',
        cursorclass=aiomysql.DictCursor
        # host='127.0.0.1',
        # port=3306,
        # user='admin_autos',
        # password='zzE]vjfK[AzkAGXg',
        # db='autos_api',
        # cursorclass=aiomysql.DictCursor
    )
    try:
        yield connection
        print("Conexión establecida")
    finally:
        connection.close()
