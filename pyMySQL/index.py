from flask import Flask, jsonify
from flask_restful import Resource, abort, Api, reqparse
import connectDB

app = Flask(__name__)
api = Api(app)


class UserManger(Resource):
    def get(self, id):
        try:
            result = connectDB.getUser(id)
            if result is not None:
                return result, 200
            else:
                return 'No have user...', 404
        except Exception as err:
            print(err)

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args()

        new_id = args['id']
        password = args['password']
        email = args['email']

        try:
            result = connectDB.putUser(id, new_id, password, email)
            if result is not None:
                return result, 200
            else:
                return result, 202
        except Exception as err:
            print(err)

    def delete(self, id):
        try:
            result = connectDB.delUser(id)
            if result is not None:
                return result, 200
            else:
                return result, 202
        except Exception as err:
            print(err)


class UserMangers(Resource):
    def get(self):
        try:
            result = connectDB.getUsers()
            if result is not None:
                return result, 200
            else:
                return "Can't find user list", 500
        except Exception as err:
            print(err)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str)
        parser.add_argument('password', type=int)
        parser.add_argument('email', type=str)
        args = parser.parse_args()

        id = args['id']
        password = args['password']
        email = args['email']

        try:
            result = connectDB.postUser(
                id, password, email)
            if result == 'Done':
                return result, 200
            else:
                return result, 202
        except Exception as err:
            print(err)


api.add_resource(UserMangers, '/user')
api.add_resource(UserManger, '/user/<id>')
if __name__ == '__main__':
    app.run(debug=True)
