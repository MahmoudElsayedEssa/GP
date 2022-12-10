from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow  # integrate with sql alchemy
import os

from sqlalchemy import PrimaryKeyConstraint  # python module file paths

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# Initialize app
app = Flask(__name__)

# take the path of the project
basedir = os.path.abspath(os.path.dirname(__file__))

# what database to connect with alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)


# Initialize
# ma = Marshmallow(app)


# table user
class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(60), nullable=False, unique=True)
    user_password = db.Column(db.String(250), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    user_image = db.Column(db.String(250), nullable=False)
    user_birthdate = db.Column(db.String(50), nullable=True)
    lastLogin = db.Column(db.String(50), nullable=True, default=False)
    user_state = db.Column(db.String(50), nullable=False, default="Active")  # active, deactivate, blocked
    isOnline = db.Column(db.Boolean, nullable=False, default=False)
    user_video = db.relationship("Video", backref='user')

    # constructor to initialize the data
    def __init__(self, user_name, user_email, user_password, user_image, user_birthdate):
        self.name = user_name
        self.user_email = user_email
        self.user_password = user_password
        self.user_image = user_image
        self.user_birthdate = user_birthdate

    # #method to add video
    # def addVideo(self, video_id):
    #     addVideo = Video(video_id=video_id, uid=self.id)
    #     db.session.add(addVideo)
    #     db.session.commit()

    # def remove_video(self, itemid):
    #     video_to_remove = Video.query.filter_by(itemid=itemid, uid=self.id).first()
    #     db.session.delete(video_to_remove)
    #     db.session.commit()


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    video_title = db.Column(db.String(100), nullable=False)
    video_path = db.Column(db.String(255), nullable=False)
    video_subtitle = db.Column(db.String(255), nullable=False)
    # video_date = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))


# Product Schema
# class UserSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'username', 'password')

# Initialize schema
# user_schema = UserSchema()
# users_schema = UserSchema(many = True)


# Create Database
with app.app_context():
    # db.drop_all()
    db.create_all()


# #Create user
# @app.route('/register', methods = ['POST'])
# def create_user():
#     username = request.json['username']
#     password = request.json['password']

#     new_user = User(username, password)
#     db.session.add(new_user)
#     db.session.commit()

#     return user_schema.jsonify(new_user)


@app.route('/register', methods=['POST'])
def register():
    _json = request.json
    _username = _json['username']
    _email = _json['email']
    _password = _json['password']
    _user_image = _json['userImage']
    _user_birthdate = _json['userBirthDate']

    new_user = User(_username, _email, _password, _user_image, _user_birthdate)
    db.session.add(new_user)
    db.session.commit()

    return "Data added successfully mahmoud"


# Run server
if __name__ == '__main__':
    app.run(debug=True)