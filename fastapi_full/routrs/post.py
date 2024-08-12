from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.sql.functions import current_user

from app import oauth2
from moduls.schemas import Post
from sqlalchemy.orm import Session
from moduls import models
from app.oauth2 import get_current_user
from moduls import schemas
from moduls.database import get_db
from typing import List
router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)

# postlarni olish
@router.get('/posts/', response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                    limit: int = 10, skip: int = 0):
    # cursor.execute("""SELECT * FROM posts""")
    # records = cursor.fetchall()
    posts = db.query(models.Posts).limit(limit).all()
    return posts


# yangi post yaratish


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int =
    Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #     (post.title, post.content, post.published)
    # )
    # new_post = cursor.fetchone()  # Yaratilgan postni olish
    # conn.commit()  # O‘zgarishlarni ma'lumotlar bazasiga saqlash

    if current_user:
        print(current_user)
    else:
        print("none")
    new_post = models.Posts(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



# bitta postni olish
@router.get('/{id}')
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authentication to perform requested action")

    return post




# postni o'chirish
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    deleted_post = db.query(models.Posts).filter(models.Posts.id == id).first()

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




# postni yangilash
@router.put('/{id}', status_code=status.HTTP_200_OK)
async def update_post(id: int, post: Post,  db: Session = Depends(get_db)):
    # cursor.execute(
    #     "UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *",
    #     (post.title, post.content, str(id))
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    post_query.update(post.dict(), synchronize_session=False)

    db.commit()
    return post