from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(24))
    person_id=db.Column(db.String(32))

    def jsonify(self):
        return {"username":self.username,
                "person_id":self.person_id}
                
    def __repr__ (self):
        return "<{}>:{}".format(self.username,self.person_id)
