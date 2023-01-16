from flask_restful import Resource, Api, reqparse
from flask import current_app as app
from application.models import *

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, type=str)
parser.add_argument('caption', required=True, type=str)

api = Api(app)

class BlogAPI(Resource):

    def get(self, id):
        blog = db.session.query(Blogs).filter(Blogs.id == id).first()
        if blog:
            return blog.asd()
        else:
            return {'error': 'Blog not found'}, 404

    def put(self, id):
        blog = db.session.query(Blogs).filter(Blogs.id == id).first()
        if blog:
            args = parser.parse_args()
            blog.title = args['title']
            blog.caption = args['caption']
            db.session.commit()
            return blog.asd()
        else:
            return {'error': 'Blog not found'}, 404

    def delete(self, id):
        blog = db.session.query(Blogs).filter(Blogs.id == id).first()
        if blog:
            db.session.delete(blog)
            db.session.commit()
            return {'message': 'Blog deleted'}
        else:
            return {'error': 'Blog not found'}, 404


class BlogListAPI(Resource):

    def get(self,id):
        user=db.session.query(Users).filter(Users.id == id).first()
        blogs = user.blogs
        return [blog.asd() for blog in blogs]

    def post(self,id):
        args = parser.parse_args()
        blog = Blogs(title=args['title'], caption=args["caption"],uid=id)
        db.session.add(blog)
        db.session.commit()
        return blog.asd()


api.add_resource(BlogAPI, '/api/blog/<int:id>')
api.add_resource(BlogListAPI, '/api/blogs/<int:id>')