import azure.functions as func
import logging
import pyodbc
import json

server = 'filmiapp-server.postgres.database.azure.com'
database = 'postgres'
username = 'pepkata'
password = 'Pe2006@@'
driver = '{ODBC Driver 17 for SQL Server}'

def search_films_by_title(title):
    try:
        conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=5432;DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = conn.cursor()

        # Construct SQL query to search for films by title
        if title:
            sql_query = f"SELECT * FROM Films WHERE Title LIKE ?"
            cursor.execute(sql_query, ('%' + title + '%',))
        else:
            sql_query = "SELECT * FROM Films"
            cursor.execute(sql_query)

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Convert rows to list of dictionaries
        films = []
        for row in rows:
            film = {
                "id": row.Id,
                "title": row.Title,
                "year": row.Year,
                "genre": row.Genre,
                "description": row.Description,
                "director": row.Director,
                "actors": row.Actors
            }
            films.append(film)

        return films
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return []

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Get the movie title from the query parameters
        title = req.params.get('title')

        # Search for films by title
        films = search_films_by_title(title)

        # Return the list of films as JSON response
        return func.HttpResponse(json.dumps(films), mimetype="application/json", status_code=200)
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse("Internal server error", status_code=500)
