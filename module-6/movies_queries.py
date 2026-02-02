import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

# Load DB credentials from .env (must be in the same folder you run this from)
secrets = dotenv_values(".env")

config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

def print_section(title: str):
    print("\n" + title)
    print("-" * len(title))

def main():
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor()

        # 1) Select all fields from studio
        print_section("DISPLAYING Studio RECORDS")
        cursor.execute("SELECT * FROM studio;")
        for (studio_id, studio_name) in cursor.fetchall():
            print(f"Studio ID: {studio_id}")
            print(f"Studio Name: {studio_name}\n")

        # 2) Select all fields from genre
        print_section("DISPLAYING Genre RECORDS")
        cursor.execute("SELECT * FROM genre;")
        for (genre_id, genre_name) in cursor.fetchall():
            print(f"Genre ID: {genre_id}")
            print(f"Genre Name: {genre_name}\n")

        # 3) Movie names for movies with runtime < 2 hours (120 minutes)
        print_section("DISPLAYING Short Film RECORDS")
        cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120;")
        for (film_name, film_runtime) in cursor.fetchall():
            print(f"Film Name: {film_name}")
            print(f"Runtime: {film_runtime}\n")

        # 4) Film names and directors, grouped by director (printed in groups)
        print_section("DISPLAYING Director RECORDS")
        cursor.execute("SELECT film_director, film_name FROM film ORDER BY film_director, film_name;")
        rows = cursor.fetchall()

        current_director = None
        for (director, film_name) in rows:
            if director != current_director:
                current_director = director
                print(f"\nDirector: {current_director}")
            print(f"  Film Name: {film_name}")

        print()  # final newline for clean ending

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Database error: Access denied (check USER/PASSWORD in .env).")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database error: Database does not exist (check DATABASE in .env).")
        else:
            print(f"Database error: {err}")

    finally:
        try:
            cursor.close()
            db.close()
        except:
            pass

if __name__ == "__main__":
    main()
