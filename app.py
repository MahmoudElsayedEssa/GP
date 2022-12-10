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
data = SQLAlchemy(app)


# Initialize
# ma = Marshmallow(app)


# table user
class User(UserMixin, data.Model):
    user_id = data.Column(data.Integer, primary_key=True)
    name = data.Column(data.String(50), nullable=False)
    user_email = data.Column(data.String(60), nullable=False, unique=True)
    user_password = data.Column(data.String(250), nullable=False)
    is_admin = data.Column(data.Boolean, nullable=False, default=False)
    user_image = data.Column(data.String(250), nullable=False)
    user_birthdate = data.Column(data.String(50), nullable=True)
    lastLogin = data.Column(data.String(50), nullable=True, default=False)
    user_state = data.Column(data.String(50), nullable=False, default="Active")  # active, deactivate, blocked
    isOnline = data.Column(data.Boolean, nullable=False, default=False)
    user_video = data.relationship("Video", backref='user')

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


class Video(data.Model):
    video_id = data.Column(data.Integer, primary_key=True)
    video_title = data.Column(data.String(100), nullable=False)
    video_path = data.Column(data.String(255), nullable=False)
    video_subtitle = data.Column(data.String(255), nullable=False)
    # video_date = db.Column(db.String(250), nullable=False)
    user_id = data.Column(data.Integer, data.ForeignKey('user.user_id'))


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
    data.create_all()


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
    data.session.add(new_user)
    data.session.commit()

    return "Data added successfully!!!!!"


# Run server
if __name__ == '__main__':
    app.run(debug=True)