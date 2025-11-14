from datetime import datetime, date

def parse_time_input (time_str):
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return datetime.strptime(time_str, "%I:%M %p").time()