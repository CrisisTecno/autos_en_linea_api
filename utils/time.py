
from datetime import datetime, time,timedelta,date

def timedelta_to_string(td):
    """Convierte un objeto timedelta a una cadena en formato HH:MM:SS."""
    if isinstance(td, timedelta):
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return None

# para convertir de int a date time
def unix_to_datetime(unix_timestamp):
        # Asumimos que un valor mayor a 1e12 (un número con más de 12 dígitos) está en milisegundos
    if unix_timestamp > 1e12:
        unix_timestamp /= 1000  # Convertir de milisegundos a segundos
    return datetime.utcfromtimestamp(unix_timestamp)

def timedelta_to_milliseconds(time_string):
    # hora =datetime.strptime(hora_str, '%H:%M:%S').time()
    # segundos_desde_medianoche = (hora.hour * 3600) + (hora.minute * 60) + hora.second
    # return segundos_desde_medianoche
    hours, minutes, seconds = map(int, time_string.split(':'))
    # Calcular el total de segundos
    total_seconds = hours * 3600 + minutes * 60 + seconds
    # Convertir segundos a milisegundos
    milliseconds = total_seconds * 1000
    
    return milliseconds
def convert_milliseconds_to_datetime(milliseconds):
    seconds = milliseconds / 1000.0
    return datetime.fromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S')

def convert_milliseconds_to_time_string(milliseconds):
    seconds = milliseconds // 1000
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"