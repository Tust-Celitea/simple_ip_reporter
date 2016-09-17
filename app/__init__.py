#!/usr/bin/python
import flask
import os
import requests
from app.model import User
from flask_sqlalchemy import SQLAlchemy
app=flask.Flask(__name__)
path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///{}".format(path)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)

def get_or_post(method):
    """GET or POST method?"""
    return {'GET':flask.request.args,'POST':flask.request.form}[method]

@app.route("/",methods=['GET'])
def index():
    return "Just a too simple and sometimes naïve noter."

@app.route("/register/<username>",methods=['POST','GET'])
def register(username):
    try:
        users=[i.username for i in User.query.filter_by(username=username).all()] or []
        print(users)
        if username in users:
            raise NameError("This user is registered.")
        else:
            data={i:get_or_post(flask.request.method)[i] for i in get_or_post(flask.request.method)}
            user=User(username=username,person_id=data["person_id"])
            db.session.add(user)
    except Exception as err:
        data={"status":-1,
              "error":str(err)}
    else:
        data['status']=0
        data['username']=username
    finally:
        print(data)          
        return flask.jsonify(data)

@app.route("/info/<username>",methods=['GET'])
def info(username):
    try:
        users=[i.username for i in User.query.filter_by(username=username).all()] or []
        print(users)
        if not username in users:
            raise NameError("This user is not registered.")
        else:
            data=User.query.filter_by(username=username).all()[0].jsonify()
    except Exception as err:
        data={"status":-1,
              "error":str(err)}
    else:
        data['status']=0
    finally:
        print(data)          
        return flask.jsonify(data)

@app.route("/users",methods=['GET'])
def users():
    try:
        users=User.query.all()
        data={}
    except Exception as err:
        data={"status":-1,
              "error":str(err)}
    else:
        data['status']=0
        data['data']={}
        for user in users:
            data['data'][user.id]=user.jsonify()
    finally:
        print(data)          
        return flask.jsonify(data)

@app.route("/check/<face_id>",methods=['POST','GET'])
def check(username):
    print(flask.request.form)
    return flask.jsonify(**flask.request.form)

if __name__=="__main__":
    app.run(debug=True)
