from flask_restful import Resource, Api, reqparse
from flask import current_app as app
from application.models import *

api = Api(app)

class feedAPI(Resource):

    def get(self, uid, pid):
        blog = db.session.query(Blogs).filter(Blogs.id == pid).first()
        if blog:
            followee = blog.user
            user = db.session.query(Users).filter(Users.id == uid).first()
            if followee in user.following:
                return blog.asd()
            else:
                return {'error': 'Blog not in User feed'}, 404
        else:
            return {'error': 'Blog not found'}, 404

    def post(self,uid,pid):
        blog = db.session.query(Blogs).filter(Blogs.id == pid).first()
        if blog:
            followee=blog.user
            user = db.session.query(Users).filter(Users.id == uid).first()
            user.following.append(followee)
            db.session.commit()
            return blog.asd()
        else:
            return {'error': 'Blog not found'}, 404

    def delete(self,uid,pid):
        blog = db.session.query(Blogs).filter(Blogs.id == pid).first()
        if blog:
            followee=blog.user
            user = db.session.query(Users).filter(Users.id == uid).first()
            user.following.remove(followee)
            db.session.commit()
            return blog.asd()
        else:
            return {'error': 'Blog not found'}, 404


api.add_resource(feedAPI, '/api/feed/<int:uid>/<int:pid>')
