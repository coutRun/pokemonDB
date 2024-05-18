# This python file simply tests your connection to the postgres database in the database docker container

import psycopg2
import os
from dotenv import load_dotenv

def connect():
    load_dotenv()
    connection = None
    try:
        # sensitive information is stored as environment variables
        connection = psycopg2.connect(
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=5432
        )
        crsr = connection.cursor()
        
        # runs simple psql statement to test connection
        crsr.execute('SELECT * FROM test;')
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