import pyodbc

try:
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER=fwv.netsec.com.mx;DATABASE=autos_en_linea_services;UID=scaleflow;PWD=Sc4l3fl0w')
    # connection = pyodbc.connect('DRIVER={SQL Server};SERVER=USKOKRUM2010;DATABASE=django_api;Trusted_Connection=yes;')
    print("Conexión exitosa.")


except Exception as ex:
    print("Error durante la conexión: {}".format(ex))
finally:
    connection.close()  # Se cerró la conexión a la BD.
    print("La conexión ha finalizado.")


# @asynccontextmanager
# async def connect_to_database():
#     connection = await aiomysql.connect(


#         host=os.getenv('DB_HOST'),
#         port=int(os.getenv('DB_PORT')),  
#         user=os.getenv('DB_USER'),
#         password=os.getenv('DB_PASS'),
#         db=os.getenv('DB_NAME'),
#         cursorclass=aiomysql.DictCursor
#     )
#     try:
#         yield connection
#         print("Conexión establecida")
#     finally:
#         connection.close()