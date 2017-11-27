from flask import Flask
from flask import make_response
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from flask import jsonify
import datetime
import logging
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://admin:admin123@chatbotnation.ccw2jw89y0nl.us-west-2.rds.amazonaws.com:3306/chatbot_nation"
engine = create_engine('mysql+pymysql://admin:admin123@chatbotnation.ccw2jw89y0nl.us-west-2.rds.amazonaws.com:3306/chatbot_nation', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
metadata = MetaData(bind=engine)
db = SQLAlchemy()
db.init_app(app)



# app.config['SQLALCHEMY_DATABASE_URI'] =
# db.init_app(app)


@app.route('/', methods=['POST'])
def chatbot_facade():
    req = request.get_json(silent=True, force=True)
    logger.info("Entry:Chatbot Facade")
    print("Input Json:")
    print(json.dumps(req, indent=4, sort_keys=True))

    if req.get("result").get("action") == "user_greet":
        new_facebook_id = req.get("originalRequest").get("data").get("sender").get("id")
        print(new_facebook_id)
        speech = user_greetings(new_facebook_id)
        res = {
            "speech": speech,
            "displayText": speech,
            "data": {"facebook": {
                "text": speech
            }},
            # "contextOut": [],
            "source": "Test"
        }
    else:
        res = {}


    if req.get("result").get("action") == "check_nick_name":
        parameters= req.get("result").get("parameters")
        name=parameters.get("given-name")
        print(name)
        speech = verify_nick_name(name)
        res = {
            "speech": speech,
            "displayText": speech,
            "data": {"facebook": {
                "text": speech
            }},
            # "contextOut": [],
            "source": "Test"
         }
    elif req.get("result").get("action") == "check_email":
        parameters = req.get("result").get("parameters")
        email = parameters.get("email")
        print(email)
        speech = verify_email_id(email)
        res = {
            "speech": speech,
            "displayText": speech,
            "data": {"facebook": {
                "text": speech
            }},
            # "contextOut": [],
            "source": "Test"
        }
    else :
        res = {}


    if req.get("result").get("action") == "final_step":
        facebook_id = req.get("originalRequest").get("data").get("sender").get("id")
        print(facebook_id)
        parameters = req.get("result").get("parameters")
        date = parameters.get("date")
        duration = parameters.get("duration")
        duration_amount = duration.get("amount")
        team_name = parameters.get("team-name")
        application = parameters.get("application")
        start_time = parameters.get("time1")
        print(start_time)
        speech = insert_into_schtable(date,facebook_id,duration_amount,team_name,application,start_time)
        res = {
            "speech": speech,
            "displayText": speech,
            "data": {"facebook": {
                "text": speech
            }},
            # "contextOut": [],
            "source": "Test"
        }
    else:
        res = {}



    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    logger.info("Exit:Chatbot Facade")
    return r



def verify_nick_name(name):
    logger.info("Entry:Verify Nick Name:")
    user_frnd_list = Table('user_frnd_list',metadata, autoload=True)
    s = user_frnd_list.select(user_frnd_list.c.nick_name==name)
    rs = s.execute()
    row= rs.fetchall()
    logger.info("Exit:Verify Nick Name")
    if len(row):
        return "Yes, User found in our system!"
    else:
        return "User not found!"


def verify_email_id(email):
    logger.info("Entry:Verify Email Id:")
    users = Table('user',metadata, autoload=True)
    s = users.select(users.c.email_id==email)
    rs = s.execute()
    row= rs.fetchall()
    print(row)
    logger.info("Exit:Verify Email Id")
    if len(row):
        return "Would you like to add this email id to your Friend List?"
    else:
        return "User not found!"


def insert_into_schtable(date,facebook_id,duration_amount,team_name,application,start_time):
    new_date = datetime.datetime.strptime(date , '%Y-%m-%d')
    new_facebook_id = int(facebook_id.replace(" ",""))
    logger.info("Entry:Insert params:")
    user_new = Table('user',metadata,autoload = True)
    s = user_new.select(user_new.c.facebook_id == new_facebook_id)
    rs = s.execute()
    rsx = rs.fetchall()

    if len(rsx) :
        con = engine.connect()
        u = select([user_new.c.usr_id]).where(user_new.c.facebook_id == new_facebook_id)
        rw = con.execute(u)
        row = rw.fetchall()
        user_schedule = Table('user_sch',metadata, autoload=True)
        user_team_new = Table('user_team', metadata, autoload=True)
        con = engine.connect()
        rs = con.execute(user_schedule.insert().values(sch_date=new_date, usr_id=row[0][0], sch_duration=duration_amount, application = application,sch_start_time = start_time))
        wk = con.execute(user_team_new.insert().values(leader_id = row[0][0],team_name = team_name ))
        logger.info("Exit:Insert params")
        if rs :
             return "Awesome you meeting has been scheduled!"
        else:
             return "Not Inserted!"
    else :
        return "No entry found in User Table"


def user_greetings(new_facebook_id):
    con = engine.connect()
    facebook_id = int(new_facebook_id.replace(" ", ""))
    logger.info("Entry:Greet User:")
    user_new = Table('user',metadata,autoload = True)
    u = select([user_new.c.first_name]).where(user_new.c.facebook_id == facebook_id)
    rw = con.execute(u)
    print(rw)
    row = rw.fetchall()
    value = row[0][0]
    print(value)
    if len(row) :
        return 'Hi'+ value
    else:
        return "No User"



if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=int(os.environ['PORT']))
    app.run()