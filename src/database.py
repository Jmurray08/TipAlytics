import psycopg

def get_connection():
    return psycopg.connect(
        dbname="postgres",
        user="postgres",
        password="BrodyAussie2020",
        host="localhost",
        port=5432
    )

def initialize_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Shift (
                    shift_id SERIAL PRIMARY KEY,
                    date DATE NOT NULL,
                    shift_type TEXT NOT NULL,
                    in_time TIME NOT NULL,
                    out_time TIME NOT NULL 
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS Weather (
                    weather_id SERIAL PRIMARY KEY,
                    shift_id INT REFERENCES Shift(shift_id) ON DELETE CASCADE,
                    low_temp INT,
                    high_temp INT,
                    condition TEXT
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS tips (
                    tip_id SERIAL PRIMARY KEY,
                    shift_id INT REFERENCES Shift(shift_id) ON DELETE CASCADE,
                    amount INT NOT NULL,
                    spent NUMERIC (4, 2) NOT NULL
                );
            """)

        conn.commit()
