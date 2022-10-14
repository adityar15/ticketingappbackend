from schemas import UserModels
from models.User import User
from fastapi import HTTPException


from passlib.context import CryptContext
from jwttoken import create_access_token, create_refresh_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def getUserByEmail(db, email):
    return db.query(User).filter(User.email == email).first()

def createUser(user: UserModels.RequestModel, db):

    if getUserByEmail(db, user.email):
        raise HTTPException(status_code=409, detail="User already exists") 

    password = pwd_context.hash(user.password)
    registered_user = User(name=user.name, email=user.email, is_active=True, password=password)
    db.add(registered_user)
    db.commit()
    db.refresh(registered_user)
    return registered_user
    

def login(user: UserModels.LoginRequestModel, db):

    existingUser = getUserByEmail(db, user.email)
    if not existingUser:
        raise HTTPException(status_code=404, detail="User does not exist") 

    elif existingUser and pwd_context.verify(user.password, existingUser.password):
        token = create_access_token({"email": existingUser.email, "id": existingUser.id})
        refreshToken = create_refresh_token({"email": existingUser.email, "id": existingUser.id})
        return {
            "token": token,
            "email": existingUser.email,
            "name": existingUser.name,
            "id": existingUser.id,
            "refresh_token": refreshToken,
        }
    else:
        raise HTTPException(status_code=401, detail="Incorrect credentials")