from flask import Flask
import redis
import os
from google.cloud.sql.connector import connector
import sqlalchemy
import pymysql
import logging
from mongoengine import connect
from mongoengine import Document, ListField, StringField, URLField

redis_host = os.environ.get('REDIS_IP', 'localhost')
redis_port = 6379
redis_password = ""

cloudsql_conn_name = os.environ.get('CLOUDSQL_CONN_NAME')
cloudsql_user = os.environ.get('CLOUDSQL_USER')
cloudsql_password = os.environ.get('CLOUDSQL_PW')
cloudsql_dbname = os.environ.get('CLOUDSQL_DB')


app = Flask(__name__)

# mysql-step1: create the pymysql connection

def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        cloudsql_conn_name,
        "pymysql",
        user=cloudsql_user,
        password=cloudsql_password,
        db=cloudsql_dbname
    )
    return conn

# mysql-step2: create the connection pool 
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# mongo community is install on devhk(10.170.0.7)
conn = connect(db="mongo-cliu", host="10.170.0.7", port=27017)


class Tutorial(Document):
    title = StringField(required=True, max_length=70)
    author = StringField(required=True, max_length=20)
    contributors = ListField(StringField(max_length=20))
    url = URLField(required=True)

@app.route('/redis', methods=['GET', 'POST'])
def hello_redis():
    """Example Hello Redis Program"""
   
    # redis-step 1: create the Redis Connection object
    try:
   
        # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
        # using the default encoding utf-8.  This is client specific.
        r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
   
        # redis-step 2: Set the hello message in Redis
        r.set("msg:hello", "Hello Redis!!!")

        # redis-step 3: Retrieve the hello message from Redis
        msg = r.get("msg:hello")
        print(msg+"\n")
        return msg        
   
    except Exception as e:
        print(e)
        return "redis error\n"

@app.route('/', methods=['GET', 'POST'])
def hello():
    return 'Welcome to My Watchlist11111!\n'



@app.route('/mysql', methods=['GET', 'POST'])
def hello_mysql():
    try:
        # mysql-step3: run some sql statement 
        # insert statement
        insert_stmt = sqlalchemy.text(
            "INSERT INTO Persons (ID, Name) VALUES (:id,:name);")

        with pool.connect() as db_conn:
            # insert into database
            db_conn.execute(insert_stmt, id=1, name="Will Smith")

            # query database
            result = db_conn.execute("SELECT * from Persons").fetchall()

            # Do something with the results
            for row in result:
                print(row)
            
            return str(result[1])
        
    except Exception as e:
        print(e)
        return "mysql error\n"

@app.route('/mongo', methods=['GET', 'POST'])
def hello_mongo():
    try:
        tutorial1 = Tutorial(
            title="Beautiful Soup: Build a Web Scraper With Python",
            author="Martin",
            contributors=["Aldren", "Geir Arne", "Jaya", "Joanna", "Mike"],
            url="https://realpython.com/beautiful-soup-web-scraper-python/"
        )
        tutorial1.save()


        for doc in Tutorial.objects(author="Jon"):
            print(str(doc.to_json()))
            return str(doc.to_json()) 
    except Exception as e:
        print(e)
        return "mongo error"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)



