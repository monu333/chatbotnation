from flasksqlalchemy import create_engine
from flasksqlalchemy.ext.declarative import declarative_base
from flasksqlalchemy.orm import sessionmaker

Base = declarative_base()
sess = None


def connection():

    engine = create_engine(
        "mysql://admin:admin123@chatbotnation.ccw2jw89y0nl.us-west-2.rds.amazonaws.com:3306/chatbot_nation")

    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)
    sess = session()
    return session
