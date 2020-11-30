#Import flask dependency
from flask import Flask

#Create app instance
app = Flask(__name__)

#Create Flask routes
@app.route('/')
def hello_world():
    return 'Hello world'