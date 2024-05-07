import azure.functions as func
import logging
import psycopg2

server = 'filmiapp-server.postgres.database.azure.com'
database = 'postgres'
username = 'pepkata'
password = 'Pe2006@@'

def add_film_to_db(title, year, genre, description, director, actors):
    try:
        conn = psycopg2.connect(
            dbname=database,
            user=username,
            password=password,
            host=server
        )
        cursor = conn.cursor()
        sql_query = "INSERT INTO Films (Title, Year, Genre, Description, Director, Actors) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql_query, (title, year, genre, description, director, actors))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return False
    finally:
        cursor.close()
        conn.close()

def funcTask1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    title = req_body.get('title')
    year = req_body.get('year')
    genre = req_body.get('genre')
    description = req_body.get('description')
    director = req_body.get('director')
    actors = req_body.get('actors')

    if title and year and genre and description and director and actors:
        if add_film_to_db(title, year, genre, description, director, actors):
            return func.HttpResponse("Film information saved successfully", status_code=200)
        else:
            return func.HttpResponse("Internal server error", status_code=500)
    else:
        return func.HttpResponse("Invalid request body", status_code=400)

# Registering the function with HTTP trigger
funcTask1 = func.HttpTrigger(funcTask1)

# Creating the Azure Function app
app = func.FunctionApp(functions=[funcTask1])
