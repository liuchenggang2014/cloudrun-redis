from flask import Flask
import redis
import os

redis_host = os.environ.get('REDIS_IP', 'localhost')
redis_port = 6379
redis_password = ""


app = Flask(__name__)
@app.route('/redis', methods=['GET', 'POST'])
def hello_redis():
    """Example Hello Redis Program"""
   
    # step 3: create the Redis Connection object
    try:
   
        # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
        # using the default encoding utf-8.  This is client specific.
        r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
   
        # step 4: Set the hello message in Redis
        r.set("msg:hello", "Hello Redis!!!")

        # step 5: Retrieve the hello message from Redis
        msg = r.get("msg:hello")
        print(msg+"\n")
        return msg        
   
    except Exception as e:
        print(e)
        return "redis error\n"

@app.route('/', methods=['GET', 'POST'])
def hello():
    return 'Welcome to My Watchlist11111!\n'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)



