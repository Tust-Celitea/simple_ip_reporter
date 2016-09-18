#!/usr/bin/python
import flask
import os
import requests
from . import config
from app.model import User
from flask_sqlalchemy import SQLAlchemy
app=flask.Flask(__name__)
path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///{}".format(path)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)

def is_same_person(face_id,person_id):
    query="https://apicn.faceplusplus.com/v2/recognition/verify?api_secret={}&face_id={}&api_key={}&person_id={}"
    query=query.format(config.API_SECRET,face_id,config.API_KEY,person_id)
    request=requests.get(query)
    result=request.json()
    print(result)
    if 'error' in result:
        return result
    else:
        return {'status':0,'is_same_person':result['is_same_person']}


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
def check(face_id):
    users={user.person_id:user.username for user in User.query.all()}
    data={}
    for person_id in users:
        query=is_same_person(face_id,person_id)
        if 'status' in query:
            if query['is_same_person']:
                data['same_person']=person_id
            else:
                data['same_person']=None     
        data.update(query)
    print(data)
    return flask.jsonify(data)
if __name__=="__main__":
    app.run(debug=True)
