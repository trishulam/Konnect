from flask_restful import Resource, Api, reqparse
from flask import current_app as app
from application.models import *
from flask_bcrypt import Bcrypt
# Parse the request arguments
parser = reqparse.RequestParser()
parser.add_argument('username', required=True, type=str)
parser.add_argument('password', required=True, type=str)

api=Api(app)
class UserAPI(Resource):

    def get(self, id):
        user = db.session.query(Users).filter(Users.id == id).first()
        if user:
            return user.asd()
        else:
            return {'error': 'User not found'}, 404

    def put(self, id):
        user = db.session.query(Users).filter(Users.id == id).first()
        if user:
            args = parser.parse_args()
            b=Bcrypt()
            pa=b.generate_password_hash(args['password']).decode('utf-8')
            user.username = args['username']
            user.password = pa
            db.session.commit()
            return user.asd()
        else:
            return {'error': 'User not found'}, 404

    def delete(self, id):
        user = db.session.query(Users).filter(Users.id == id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted'}
        else:
            return {'error': 'User not found'}, 404


class UserListAPI(Resource):

    def get(self):
        users = Users.query.all()
        return [user.asd() for user in users]

    def post(self):
        args = parser.parse_args()
        b=Bcrypt()
        pa=b.generate_password_hash(args['password']).decode('utf-8')
        user = Users(username=args['username'],
                    password=pa)
        db.session.add(user)
        db.session.commit()
        return user.asd()


api.add_resource(UserAPI, '/api/users/<int:id>')
api.add_resource(UserListAPI, '/api/users')