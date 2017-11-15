from flask import Flask
from flask import make_response
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
import json
import os


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
def hello_world():
    #data = {}
    #data['displayText'] = 'Hello World!'
    #data['speech']= 'Hello Hi World'
    #json_data = json.dumps(data)
    #return json_data
    req = request.get_json(silent=True, force=True)
    speech = "Hi Peter, How are you?"
    speech2 = "Hi Natasha! Whats up?"



    if req.get("result").get("action") == "action_one":
        res = {
            "speech": speech,
            "displayText": speech,
            "data": {"facebook": {
                "text": "Hi Peter"
            }},
            # "contextOut": [],
            "source": "Test"
        }

    elif req.get("result").get("action") == "action_two":
        res = {
            "speech": speech2,
            "displayText": speech2,
            "data": {"facebook": {
                "text": "Hi Natasha!"
            }},
            # "contextOut": [],
            "source": "Test"
         }
    elif req.get("result").get("action") == "check_name":
        parameters= req.get("result").get("parameters")
        name=parameters.get("given-name")
        speech3=db_test(name)
        res = {
            "speech": speech3,
            "displayText": speech3,
            "data": {"facebook": {
                "text": speech3
            }},
            # "contextOut": [],
            "source": "Test"
         }
    else:
        res={}

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def db_test(name):
    users = Table('user',metadata, autoload=True)
    #s = users.select()
    #rs = s.execute()
    #row = rs.fetchall()
    #print(row)
    print(name)
    s1= users.select(users.c.first_name==name)
    rs1= s1.execute()
    print(rs1)
    row1= rs1.fetchall()
    print(row1)
    if row1!="":
        return "Yes, User found in our system!"
    else:
        return "User not found!"
    print("searched result:")
    print(row1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ['PORT']))
#app.run()
