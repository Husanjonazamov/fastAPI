from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from moduls import database, schemas, models
from users import utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from . import oauth2


router = APIRouter(
    tags=["Authentication"],
)


@router.post("/login")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    # create token

    # return token
    access_token = oauth2.create_access_token(data = {'user_id': user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}