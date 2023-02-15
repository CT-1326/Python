from flask import Flask, jsonify
from flask_restful import Resource, abort, Api, reqparse
import connectDB

app = Flask(__name__)
api = Api(app)


class UserManger(Resource):
    def get(self, name):
        try:
            result = connectDB.getUser(name)
            if result is not None:
                return result, 200
            else:
                return 'No have user...', 404
        except Exception as err:
            print(err)

    # def put(self, name):
    #     try:
    #     except Exception as err:
    #         print(err)

    # def delete(self, name):
    #     try:
    #     except Exception as err:
    #         print(err)


class UserMangers(Resource):
    def get(self):
        result = connectDB.get()
        if result is not None:
            return result, 200
        else:
            return "Can't find user list", 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str)
        parser.add_argument('password', type=str)
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
api.add_resource(UserManger, '/user/<name>')
if __name__ == '__main__':
    app.run(debug=True)
