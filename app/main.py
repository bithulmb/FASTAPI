import psycopg2
import time
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from . import  models
from .database import  engine
from .routers import post,users



app = FastAPI()


# Create tables automatically
models.Base.metadata.create_all(bind=engine)


while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

app.include_router(post.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Welcome to my api"}



