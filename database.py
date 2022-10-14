from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# username = "root"
# password = "aditya1234"
# database = "ticketing_live"
# host = "ticketing-live.crwd16wegxtp.eu-west-2.rds.amazonaws.com"

# SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}/{database}"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)


# postgresql
username = "umktwejhlhkohq"
password = "54f1dfc1490268eba58bd8e52a49decf1c8a854279b9c8053d9c7f571709c5c3"
host = "ec2-54-217-203-52.eu-west-1.compute.amazonaws.com"
database = "d5lijenppt45bb"
SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@{host}:5432/{database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'sslmode':'require'})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()