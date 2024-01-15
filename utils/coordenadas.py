from math import radians, sin, cos, sqrt, atan2

def obtener_sucursales_cercanas(latitud_usuario, longitud_usuario, radio, sucursales):
    sucursales_cercanas = []

    # Radio de la Tierra en kilómetros
    radio_tierra = 6371.0
  
    # Convertir las coordenadas del usuario a radianes
    latitud_usuario_rad = radians(float(latitud_usuario))
    longitud_usuario_rad = radians(float(longitud_usuario))
   
    for sucursal in sucursales:
        if ',' not in sucursal["coordenadas"]:
            continue
        # Obtener las coordenadas de la sucursal en la base de datos (en formato "latitud,longitud")
        coordenadas_sucursal = sucursal["coordenadas"].split(',')
        print(coordenadas_sucursal)
        latitud_sucursal_rad = radians(float(coordenadas_sucursal[0]))
        longitud_sucursal_rad = radians(float(coordenadas_sucursal[1]))
        
        # Calcular la diferencia de coordenadas entre el usuario y la sucursal
        d_latitud = latitud_sucursal_rad - latitud_usuario_rad
        d_longitud = longitud_sucursal_rad - longitud_usuario_rad
        # print(d_latitud)
        # print(d_longitud)
        # Calcular la distancia usando la fórmula de Haversine
        a = sin(d_latitud / 2)**2 + cos(latitud_usuario_rad) * cos(latitud_sucursal_rad) * sin(d_longitud / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distancia = radio_tierra * c
        print(distancia)
        # Verificar si la sucursal está dentro del radio especificado
        if distancia <= float(radio):
            sucursales_cercanas.append(sucursal)
    
    return sucursales_cercanas