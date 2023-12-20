
from datetime import datetime, time,timedelta

def timedelta_to_string(td):
    """Convierte un objeto timedelta a una cadena en formato HH:MM:SS."""
    if isinstance(td, timedelta):
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return None

def timedelta_to_milliseconds(td):
    """Convierte un objeto timedelta a milisegundos."""
    if isinstance(td, timedelta):
        return int(td.total_seconds() * 1000)
    return 0

def convert_milliseconds_to_datetime(milliseconds):
    seconds = milliseconds / 1000.0
    return datetime.fromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S')

def convert_milliseconds_to_time_string(milliseconds):
    seconds = milliseconds // 1000
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"