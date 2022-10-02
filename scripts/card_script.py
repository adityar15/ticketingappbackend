from models.Card import Card


def getCardsByCategory(db, categoryID):
    return db.query(Card).filter(Card.category_id == categoryID).all()


def addCard(db, payload):

    # cards = getCardsByCategory(db, payload.category_id)


    # rank = max(cards, key=lambda x : x["rank"]) if len(cards) + 1 > 0 else 1

    card = Card(text=payload.text, rank=payload.rank, category_id = payload.category_id)
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


def removeCard(db, cardID):
    db.query(Card).filter(Card.id == cardID).delete()
    db.commit()
    return True



def updateCard(db, payload):
    
    # to update card's category and rank when dragged from one category to other
    if "category_id" in payload and "rank" in payload:
        db.query(Card).filter(Card.id == payload.card_id).update({
            "rank": payload.rank,
            "category_id": payload.category
        })
    
    elif "rank" in payload and not "category_id" in payload:
        db.query(Card).filter(Card.id == payload.card_id).update({
            "rank": payload.rank
        })
    
    elif payload.text != "":
        db.query(Card).filter(Card.id == payload.card_id).update({
            "text": payload.text
        })
    
    else: 
        return False

    db.commit()

    return True

