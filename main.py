from fastapi import FastAPI, Depends
from models import Card, User, Project, Category
from database import SessionLocal, engine
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware
from cors import origins
from schemas import UserModels
from scripts import user_script

app = FastAPI()

# migrating each table to db if it does not exist
User.Base.metadata.create_all(bind=engine)
Project.Base.metadata.create_all(bind=engine)
Category.Base.metadata.create_all(bind=engine)
Card.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def printMessage():
    return {"message": "Hello World"}


# register user
@app.post("/register", status_code=200, response_model=UserModels.ResponseModel)
def register(user: UserModels.RequestModel, db: Session = Depends(get_db)):
    createdUser = user_script.createUser(user, db)
    return createdUser



# login user

@app.post("/login", status_code=200)
def login(user: UserModels.LoginRequestModel, db:Session=Depends(get_db)):
    return user_script.login(user, db)