from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

app.debug = True

@app.route("/")
def hello():
    return "Hello World!"

app.run(host='0.0.0.0')