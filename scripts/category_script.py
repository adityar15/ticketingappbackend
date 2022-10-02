from models.Category import Category


def getCategoryByProject(db, projectID):
    return db.query(Category).filter(Category.project_id == projectID).all()

def addCategory(db, payload):
    category = Category(title=payload.title, color=payload.color, project_id = payload.project_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

