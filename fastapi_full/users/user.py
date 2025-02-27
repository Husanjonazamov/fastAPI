from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from moduls import models, schemas
from moduls.database import get_db
from . import utils
app = FastAPI()

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)




@router.post('/users/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} not found')

    return user



