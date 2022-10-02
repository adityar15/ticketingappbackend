from models.Project import Project
from models.Category import Category

def addNew(db, payload):
    project = Project(user_id=payload.user_id, title=payload.title)
    db.add(project)
    db.commit()
    db.refresh(project)

    categories = [
        Category(project_id=project.id, title="Backlog", color="bg-blue-600"),
        Category(project_id=project.id, title="To-Do", color="bg-orange-600"),
        Category(project_id=project.id, title="Doing", color="bg-orange-600"),
        Category(project_id=project.id, title="Code Review", color="bg-orange-600"),
        Category(project_id=project.id, title="Testing", color="bg-orange-600"),
        Category(project_id=project.id, title="Done", color="bg-green-600"),
    ]

    db.bulk_save_objects(categories)
    db.commit()

    return project


def getAllProjects(db, userID):
    return db.query(Project).filter(Project.user_id == userID).all()



