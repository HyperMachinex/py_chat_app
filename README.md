To run system -> **`docker compose up --build`** \
To stop --> **`docker compose down -v`**

Python chat app written in fastapi. \
Messages and credentials are storing in mongodb. \
Celery task queue and jwt tokens are stored in REDIS. \
All messages are deleted in 30 seconds via Celery. \

# Useful Commands

Flower --> **`http://localhost:5555`**

fastapi container --> **`docker compose exec -it fastapi bash`**

redis container --> **`docker compose exec -it redis redis-cli`**

**`KEYS \*`** # Lists all keys \
**`GET my_key`** # Gets the value of a string key \
**`HGETALL user:123`** # Shows all fields in a hash \
**`LRANGE messages 0 -1`** # Gets all elements in a list \

**`GET celery-task-meta-e71d8922-6d2c-4dd9-80ff-02ef2092273a`** --> { \
"status": "SUCCESS", \
"result": "...",   \
 "traceback": null, \
"children": [] \
}

mongodb container --> **`docker exec -it chat_mongo mongosh`** \
mongodb test --> **`curl http://localhost:8000/mongo-test`** \

mongosh commands to see users -->   **`show dbs`** \
                                    **`use chat_app`** \
                                    **`show collections`** \
                                    **`db.users.find().pretty()`** \


