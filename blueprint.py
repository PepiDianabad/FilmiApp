import azure.functions as func
import logging
import pyodbc

server = 'filmiapp-server.postgres.database.azure.com'
database = 'postgres'
username = 'pepkata'
password = 'Pe2006@@'
driver = '{ODBC Driver 17 for SQL Server}'

def add_review_to_db(title, opinion, rating, date_time, author):
    try:
        conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=5432;DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = conn.cursor()
        sql_query = "INSERT INTO Reviews (Title, Opinion, Rating, Date, Author) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sql_query, (title, opinion, rating, date_time, author))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return False
    finally:
        cursor.close()
        conn.close()

def funcTask2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    title = req_body.get('title')
    opinion = req_body.get('opinion')
    rating = req_body.get('rating')
    date_time = req_body.get('date_time')
    author = req_body.get('author')

    if title and opinion and rating and date_time and author:
        if add_review_to_db(title, opinion, rating, date_time, author):
            return func.HttpResponse("Review added successfully", status_code=200)
        else:
            return func.HttpResponse("Internal server error", status_code=500)
    else:
        return func.HttpResponse("Invalid request body", status_code=400)
