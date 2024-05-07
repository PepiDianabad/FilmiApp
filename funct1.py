import azure.functions as func
import logging
import pyodbc

server = 'filmiapp-server.postgres.database.azure.com'
database = 'postgres'
username = 'pepkata'
password = 'Pe2006@@'
driver = '{ODBC Driver 17 for SQL Server}'


@app.route(route="InsertFileInfo")
def add_film_to_db(title, year, genre, description, director, actors):
    try:
        conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=5432;DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = conn.cursor()
        sql_query = "INSERT INTO Films (Title, Year, Genre, Description, Director, Actors) VALUES (?, ?, ?, ?, ?, ?)"
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

    # Получаване на данните за филма от заявката
    req_body = req.get_json()
    title = req_body.get('title')
    year = req_body.get('year')
    genre = req_body.get('genre')
    description = req_body.get('description')
    director = req_body.get('director')
    actors = req_body.get('actors')

    # Проверка дали всички данни за филма са налични
    if title and year and genre and description and director and actors:
        # Запазване на информацията за филма в базата данни
        if add_film_to_db(title, year, genre, description, director, actors):
            return func.HttpResponse("Film information saved successfully", status_code=200)
        else:
            return func.HttpResponse("Internal server error", status_code=500)
    else:
        return func.HttpResponse("Invalid request body", status_code=400)

# Регистриране на функцията като HTTP trigger
funcTask1 = func.HttpTrigger(funcTask1)

# Регистриране на функцията във функционалния пакет
app = func.FunctionApp(functions=[funcTask1])
