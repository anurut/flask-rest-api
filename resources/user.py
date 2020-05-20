import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    def post(self):
        request_data = self.parser.parse_args()

        if UserModel.find_by_username(request_data['username']):
            return {"message": f"Username {request_data['username']} already exists"}, 400

        new_user = UserModel(**request_data)
        new_user.save_to_db()

        return {"message": "User created successfully"}, 201
