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
    print("Just inside hello world:")
    print("Input Json:")
    print(json.dumps(req, indent=4, sort_keys=True))



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
    elif req.get("result").get("action") == "check_nick_name":
        parameters= req.get("result").get("parameters")
        name=parameters.get("given-name")

        speech3=verify_nick_name(name)
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


def verify_nick_name(name):
    user_frnd_list = Table('user_frnd_list',metadata, autoload=True)
    s = user_frnd_list.select(user_frnd_list.c.first_name==name)
    rs = s.execute()
    row= rs.fetchall()
    if row!="":
        return "Yes, User found in our system!"
    else:
        return "User not found!"
    print("searched result:")
    print(row)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ['PORT']))
#app.run()
