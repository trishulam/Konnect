from .database import db
from datetime import datetime
from pytz import timezone
from flask_login import UserMixin
circle = db.Table(
    "circle",
    db.metadata,
    db.Column("follower_id", db.Integer, db.ForeignKey("Users.id"), primary_key=True),
    db.Column("followee_id", db.Integer, db.ForeignKey("Users.id"), primary_key=True),
)

class Users(db.Model,UserMixin):
    __tablename__="Users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False,default="stock.jpeg")
    desc = db.Column(db.String,default="")
    blogs = db.relationship("Blogs", backref="user", cascade="all,delete")
    comments=db.relationship("comments",backref="user", cascade="all,delete")
    likes = db.relationship("likes", backref="user", cascade="all,delete")
    following = db.relationship(
        "Users",
        secondary=circle,
        primaryjoin=id == circle.c.follower_id,
        secondaryjoin=id == circle.c.followee_id,
        backref="followers")

    def asd(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'name': self.name
        }

class Blogs(db.Model):
    __tablename__="Blogs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    caption = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False, default="default.png")
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.now(timezone("Asia/Kolkata")))
    likes = db.relationship("likes", backref="blog", cascade="all,delete")
    comments= db.relationship("comments",backref="blog", cascade="all,delete")
    uid = db.Column(db.Integer, db.ForeignKey("Users.id"))

    def asd(self):
        return {
            'id': self.id,
            'title': self.title,
            'caption': self.caption,
            'created_at': self.created_at.strftime("%d/%m/%y (%I:%M %p)"),
            'user_id' : self.uid
        }

class likes(db.Model):
    __tablename__="likes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey("Users.id"))
    pid = db.Column(db.Integer, db.ForeignKey("Blogs.id"))

class comments(db.Model):
    __tablename__="comments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey("Users.id"))
    pid = db.Column(db.Integer, db.ForeignKey("Blogs.id"))
