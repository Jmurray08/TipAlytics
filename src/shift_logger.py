from datetime import date
from .database import get_connection
from .utils import parse_time_input

def log_shift():

    date_input = input("Enter shift date (YYYY-MM-DD): ")
    shift_type = input("Enter shift type (AM, PM, OR DOUBLE): ")
    in_time_input = input("Enter clock-in time: ")
    out_time_input = input("Enter clock-out time: ")

    shift_date = date.fromisoformat(date_input)
    in_time = parse_time_input(in_time_input)
    out_time = parse_time_input(out_time_input)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO Shift (date, shift_type, in_time, out_time)
                VALUES (%s, %s, %s, %s)
                RETURNING shift_id;
            """, (shift_date, shift_type, in_time, out_time))
            shift_id = cur.fetchone()[0]

            low_temp = int(input("Enter low temperature of the day: "))
            high_temp = int(input("Enter high temperature of the day: "))
            conditions = input("Enter weather conditions (Sunny, Rainy, Cloudy): ")

            cur.execute("""
                INSERT INTO Weather (shift_id, low_temp, high_temp, condition)
                VALUES (%s, %s, %s, %s);
            """, (shift_id, low_temp, high_temp, conditions))

            amount = int(input("Enter the amount of tips you walked home with: "))
            spent = float(input("Enter amount spent on food/apparel/drinks(IF ANY): "))

            cur.execute("""
                INSERT INTO tips(shift_id, amount, spent)
                VALUES (%s, %s, %s);
            """, (shift_id, amount, spent))
            
        print(f"\n Shift {shift_id} logged successfully!")
