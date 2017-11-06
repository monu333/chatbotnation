from flask import Flask
from flask import make_response
from flask import request
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
    else:
        res={}

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ['PORT']))
