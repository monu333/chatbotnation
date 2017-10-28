from flask import Flask
from models.database import db
import os
import json

app = Flask(__name__)
app.config['DEBUG'] = True


# app.config['SQLALCHEMY_DATABASE_URI'] =
# db.init_app(app)

@app.route('/', methods=['POST'])
def hello_world():
    data = {}
    data['displayText'] = 'Hello World!'
    json_data = json.dumps(data)
    return json_data

if __name__ == '__main__':
    app.run(app.run(host='0.0.0.0', port=int(os.environ['PORT'])))
