from time import time
import psycopg2
from fastapi import FastAPI, Depends
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from moduls import models
from moduls.database import engine, get_db
from routrs import post
from users import user
from app import auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



my_post = [
    {'title': 'title of post 1', "content": "content of the post 1", "id": 1},
    {'title': 'title of post 2', "content": "content of the post 2", "id": 2}
]




def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# Ma'lumotlar bazasiga ulanish
try:
    conn = psycopg2.connect(
        host='localhost',
        database='fastapi',
        user='postgres',
        password='2309',
        cursor_factory=RealDictCursor,
        port='5432'
    )
    cursor = conn.cursor()
    print("Database connection was successful")
except Exception as error:
    print('Connection to database failed')
    print("Error:", error)
    time.sleep(5)


@app.get('/')
async def root():
    return {'message': 'Hello World'}



@app.get("/sqlalchemy/")
async def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return {"status": posts}





