from flask import Flask
from flask import make_response
from models.database import db
import os
import json

app = Flask(__name__)
app.config['DEBUG'] = True


# app.config['SQLALCHEMY_DATABASE_URI'] =
# db.init_app(app)

@app.route('/', methods=['POST'])
def hello_world():
    #data = {}
    #data['displayText'] = 'Hello World!'
    #data['speech']= 'Hello Hi World'
    #json_data = json.dumps(data)
    #return json_data
    speech = "Hi Peter, How are you?"
    res={
        "speech": speech,
        "displayText": speech,
        "data": {"facebook": "Hi Peter"},
        # "contextOut": [],
        "source": "Test"
    }
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    app.run()
