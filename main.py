from fastapi import FastAPI, Depends
from models import Card, User, Project, Category
from database import get_db, engine
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware
from cors import origins
from schemas import UserModels, CardModels, CategoryModels, ProjectModels
from scripts import user_script, card_script, category_script, project_script
from typing import List

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



# add new project
@app.post("/add_new_project", status_code=200, response_model=ProjectModels.ResponseModel)
def addNew(project: ProjectModels.RequestModel, db: Session = Depends(get_db)):
    return project_script.addNew(db, project)

# get all projects
@app.get("/get_projects/{user_id}", status_code=200, response_model=List[ProjectModels.ResponseModel])
def getAll(user_id: int, db: Session = Depends(get_db)):
    return project_script.getAllProjects(db, user_id)


# add new card
@app.post("/add_new_card", status_code=200, response_model=CardModels.ResponseModel)
def addCard(card: CardModels.RequestModel, db: Session=Depends(get_db)):
    return card_script.addCard(db, card)

# update card
@app.post("/update_card", status_code=200)
def updateCard(card:CardModels.UpdateModel, db: Session=Depends(get_db)):
    return card_script.updateCard(db, card)

# delete card
@app.post("/delete_card", status_code=200)
def deleteCard(card: CardModels.DeleteModel, db: Session=Depends(get_db)):
    return card_script.removeCard(db, card.card_id)


# get categories with cards
@app.get("/categories/{project_id}", status_code=200, response_model=List[CategoryModels.ResponseModel])
def getAll(project_id: int, db: Session = Depends(get_db)):
    return category_script.getCategoryByProject(db, project_id)