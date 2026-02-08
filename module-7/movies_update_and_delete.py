"""
CSD 310 - Module 7
movies_update_and_delete.py

.env (in module-7) uses:
USER=root
PASSWORD=
HOST=localhost
DATABASE=movies
"""

import os
from pathlib import Path

import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv



env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)


def show_films(cursor, title):
    """Display films with joined genre and studio names."""
    print("\n  -- {} --".format(title))

    query = """
        SELECT
            film_name AS Name,
            film_director AS Director,
            genre_name AS Genre,
            studio_name AS Studio
        FROM film
        INNER JOIN genre ON film.genre_id = genre.genre_id
        INNER JOIN studio ON film.studio_id = studio.studio_id
        ORDER BY film_id;
    """

    cursor.execute(query)
    films = cursor.fetchall()

    for film in films:
        print("  Film Name: {}".format(film[0]))
        print("  Director: {}".format(film[1]))
        print("  Genre: {}".format(film[2]))
        print("  Studio: {}\n".format(film[3]))


def get_genre_id(cursor, genre_name):
    cursor.execute("SELECT genre_id FROM genre WHERE genre_name = %s;", (genre_name,))
    row = cursor.fetchone()
    return row[0] if row else None


def get_any_genre_id(cursor):
    cursor.execute("SELECT genre_id FROM genre ORDER BY genre_id LIMIT 1;")
    row = cursor.fetchone()
    return row[0] if row else None


def get_any_studio_id(cursor):
    cursor.execute("SELECT studio_id FROM studio ORDER BY studio_id LIMIT 1;")
    row = cursor.fetchone()
    return row[0] if row else None


def main():

    db_user = os.getenv("USER")
    db_password = os.getenv("PASSWORD")  
    db_host = os.getenv("HOST", "localhost")
    db_name = os.getenv("DATABASE", "movies")


    if not db_user:
        print("ERROR: Missing USER in .env")
        print("Expected .env keys: USER, PASSWORD, HOST, DATABASE")
        return

    config = {
        "host": db_host,
        "user": db_user,
        "password": db_password if db_password is not None else "",
        "database": db_name,
        "raise_on_warnings": True,
    }

    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor()


        show_films(cursor, "DISPLAYING FILMS")


        studio_id = get_any_studio_id(cursor)
        if studio_id is None:
            print("ERROR: No studios found in studio table.")
            return


        genre_id = get_genre_id(cursor, "Sci-Fi")
        if genre_id is None:
            genre_id = get_genre_id(cursor, "Science Fiction")
        if genre_id is None:
            genre_id = get_any_genre_id(cursor)

        if genre_id is None:
            print("ERROR: No genres found in genre table.")
            return

 
        insert_sql = """
            INSERT INTO film
                (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
            VALUES
                (%s, %s, %s, %s, %s, %s);
        """

        new_film = ("The Prestige", 2006, 130, "Christopher Nolan", studio_id, genre_id)
        cursor.execute(insert_sql, new_film)
        db.commit()

        show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

        # 3) UPDATE Alien to Horror
        horror_id = get_genre_id(cursor, "Horror")
        if horror_id is None:
            print("ERROR: Could not find genre_name = 'Horror' in genre table.")
            print("Run: SELECT genre_id, genre_name FROM genre; and confirm the exact spelling.")
        else:
            update_sql = "UPDATE film SET genre_id = %s WHERE film_name = %s;"
            cursor.execute(update_sql, (horror_id, "Alien"))
            db.commit()

            show_films(cursor, "DISPLAYING FILMS AFTER UPDATE - CHANGED ALIEN TO HORROR")

        # 4) DELETE Gladiator
        delete_sql = "DELETE FROM film WHERE film_name = %s;"
        cursor.execute(delete_sql, ("Gladiator",))
        db.commit()

        show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

        cursor.close()
        db.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ERROR: Access denied (check USER/PASSWORD in .env).")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("ERROR: Database does not exist (check DATABASE in .env).")
        else:
            print("ERROR:", err)


if __name__ == "__main__":
    main()
