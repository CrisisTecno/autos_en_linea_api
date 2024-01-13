
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
    return datetime.utcfromtimestamp(unix_timestamp)

def timedelta_to_milliseconds(hora_str):
    hora =datetime.strptime(hora_str, '%H:%M:%S').time()
    segundos_desde_medianoche = (hora.hour * 3600) + (hora.minute * 60) + hora.second
    return segundos_desde_medianoche

def convert_milliseconds_to_datetime(milliseconds):
    seconds = milliseconds / 1000.0
    return datetime.fromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S')

def convert_milliseconds_to_time_string(milliseconds):
    seconds = milliseconds // 1000
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"