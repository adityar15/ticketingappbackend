from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


username = "root"
password = "aditya1234"
database = "ticketing_live"
host = "ticketing-live.crwd16wegxtp.eu-west-2.rds.amazonaws.com"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}/{database}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()