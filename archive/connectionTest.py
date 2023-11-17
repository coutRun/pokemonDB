# This python file simply tests your connection to the pokemondb database on localhost

import psycopg2
import os
def connect():
    connection = None
    try:
        # sensitive information is stored as environment variables
        connection = psycopg2.connect(
            host=os.getenv("PSQLPKMNHOST"),
            port=os.getenv("PSQLPKMNPORT"),
            database=os.getenv("PSQLPKMNDATABASE"),
            user=os.getenv("PSQLPKMNUSER"),
            password=os.getenv("PSQLPKMNPASSWORD")
        )
        crsr = connection.cursor()
        
        # runs simple psql statement to test connection
        crsr.execute('SELECT * FROM POKEDEX LIMIT 4;')
        output = crsr.fetchall()
        for i in output:
            print(i)
        
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print("Database connection terminated.")

# main
if __name__=="__main__":
    connect()