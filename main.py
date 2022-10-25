from fastapi import FastAPI, Depends, Response, Request
from fastapi.responses import JSONResponse
from models import Card, User, Project, Category
from database import get_db, engine
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware
from cors import origins
from schemas import UserModels, CardModels, CategoryModels, ProjectModels
from scripts import user_script, card_script, category_script, project_script
from typing import List, Optional


from jwttoken import generate_new_accesstoken, hasValidToken, refreshAccessToken

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
    print(createdUser)
    return createdUser



# login user
@app.post("/login", status_code=200)
def login(user: UserModels.LoginRequestModel, db:Session=Depends(get_db)):
    loggedInUser = user_script.login(user, db)
    if "refresh_token" in loggedInUser:
        print("has rt")
        response = JSONResponse(content = loggedInUser)
        # expires in seconds
        response.set_cookie(key="refresh_token", value=loggedInUser["refresh_token"], secure=True, httponly=True, expires=30 * 24 * 60 * 60)
        response.set_cookie(key="access_token", value=loggedInUser["token"], secure=True, expires=10 * 60 * 60)
        return response
    return loggedInUser



# add new project
@app.post("/add_new_project", status_code=200, response_model=ProjectModels.ResponseModel)
def addNew(project: ProjectModels.RequestModel, db: Session = Depends(get_db)):
    return project_script.addNew(db, project)

# # get all projects with secure token
# @app.get("/get_projects/{user_id}", status_code=200, response_model=List[ProjectModels.ResponseModel], dependencies=[Depends(hasValidToken)])
# def getAll(user_id: int, db: Session = Depends(get_db)):
#     return project_script.getAllProjects(db, user_id)



@app.get("/get_projects/{user_id}", status_code=200, response_model=List[ProjectModels.ResponseModel])
def getAll(user_id: int, db: Session = Depends(get_db)):
    return project_script.getAllProjects(db, user_id)



# add new card
@app.post("/add_new_card", status_code=200, response_model=CardModels.ResponseModel)
def addCard(card: CardModels.RequestModel, db: Session=Depends(get_db)):
    return card_script.addCard(db, card)

# update card text
@app.post("/update_card_text", status_code=200)
def updateCardText(card:CardModels.UpdateTextModel, db: Session=Depends(get_db)):
    return card_script.updateCardText(db, card)

@app.post("/update_card_rank", status_code=200)
def updateCardRank(cards:CardModels.UpdateCardRankRequest, db: Session=Depends(get_db)):
    return card_script.updateCardRank(db, cards["cards"])

# delete card
@app.post("/delete_card", status_code=200)
def deleteCard(card: CardModels.DeleteModel, db: Session=Depends(get_db)):
    return card_script.removeCard(db, card.card_id)


# get categories with cards
@app.get("/categories/{project_id}", status_code=200, response_model=List[CategoryModels.ResponseModel])
def getAll(project_id: int, db: Session = Depends(get_db)):
    return category_script.getCategoryByProject(db, project_id)




# get new access token
@app.post("/generate_access_token", status_code=200)
def createNewAccessToken(request: Request, db: Session = Depends(get_db)):
    return generate_new_accesstoken(request.cookies["refresh_token"], db)


# refresh access token. This is to generate new access token behind the scene

@app.get('/refresh_access_token/{token}', status_code = 200)
def refresh(token : Optional[str], request : Request):
    check = refreshAccessToken(token, request.cookies["refresh_token"])
    if type(check) == dict and "access_token" in check:        
        response = Response()
        response.set_cookie(key="access_token", value=check["access_token"], secure=True, expires=10 * 60 * 60)
        return response 
    return check